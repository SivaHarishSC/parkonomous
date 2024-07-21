"""
app.py
Main application file for handling web and ROS functionalities.
"""

import logging
import threading
import subprocess
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool

# Create a logger instance
LOGGER = logging.getLogger(__name__)

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask application
APP = Flask(__name__)
APP.secret_key = 'supersecretkey'  # Needed for flash messaging

# Initialize SocketIO for real-time communication
SOCKETIO = SocketIO(APP)

class ROSNode(Node):
    """
    ROS Node class for handling ROS operations.
    """
    def __init__(self):
        super().__init__('web_ros_node')
        self.create_subscription(PoseStamped, '/ego_vehicle_pose', self.pose_callback, 10)
        self.create_subscription(PoseStamped, '/user_pose', self.user_callback, 10)
        self.create_subscription(Bool, '/destination_reached', self.destination_callback, 10)

    @staticmethod
    def pose_callback(msg):
        """
        Callback function for handling pose updates.
        """
        xpos = round(msg.pose.position.x, 3)
        ypos = round(msg.pose.position.y, 3)
        SOCKETIO.emit('pose_update', {'x': xpos, 'y': ypos})

    @staticmethod
    def user_callback(msg):
        """
        Callback function for handling user pose updates.
        """
        xpos = round(msg.pose.position.x, 3)
        ypos = round(msg.pose.position.y, 3)
        SOCKETIO.emit('user_update', {'x': xpos, 'y': ypos})

    @staticmethod
    def destination_callback(msg):
        """
        Callback function for handling destination reached updates.
        """
        SOCKETIO.emit('destination_reached', {'reached': msg.data})

def ros_thread():
    """
    Function to run the ROS node in a separate thread.
    """
    rclpy.init()
    ros_node = ROSNode()
    rclpy.spin(ros_node)
    ros_node.destroy_node()
    rclpy.shutdown()

def start_ros_node():
    """
    Function to start the ROS node.
    """
    if not rclpy.ok():
        threading.Thread(target=ros_thread, daemon=True).start()

def get_db_connection():
    """
    Function to establish a SQLite database connection.
    """
    return sqlite3.connect("server.db")

@APP.route('/')
def index():
    """
    Route for the index page.
    """
    return render_template('index.html')

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login handling.
    """
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM customer WHERE name=? AND password=?", (name, password))
        data = cur.fetchone()
        con.close()
        if data:
            session['name'] = data[0]
            session['password'] = data[1]
            flash('Login successful!', 'success')
            LOGGER.info('Login successful for user %s', name)
            return redirect(url_for('home'))
        flash('Username and Password Mismatch', 'danger')
        LOGGER.warning('Username and Password Mismatch for user %s', name)
    return redirect(url_for('index'))

@APP.route('/home', methods=['GET', 'POST'])
def home():
    """
    Route for the home page.
    """
    return render_template('home.html')

@APP.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registration handling.
    """
    if request.method == 'POST':
        try:
            name = request.form['name']
            password = request.form['password']
            mobile_number = int(request.form['contact'])
            vehicle_id = int(request.form['vehicle_id'])
            con = get_db_connection()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO customer(name, password, mobile_number, vehicle_id) VALUES (?,?,?,?)",
                (name, password, mobile_number, vehicle_id),
            )
            con.commit()
            con.close()
            flash('Record Added Successfully', 'success')
            LOGGER.info('Record Added Successfully for user %s', name)
        except (ValueError, sqlite3.Error) as exc:
            flash(f"Error in Insert Operation: {str(exc)}", 'danger')
            LOGGER.error("Error in Insert Operation for user %s: %s", name, str(exc))
        return redirect(url_for('login'))
    return render_template('register.html')

@APP.route('/logout')
def logout():
    """
    Route for user logout.
    """
    session.clear()
    return redirect(url_for('index'))

@APP.route("/run_ros2_node", methods=["POST"])
def run_ros2_node():
    """
    Route for starting the ROS2 node via POST request.
    """
    try:
        command = "source /opt/ros/foxy/setup.bash && ros2 run park park"
        subprocess.Popen(command, shell=True, executable='/bin/bash')
        flash("ROS2 Node Started Successfully", "success")
        LOGGER.info("ROS2 Node Started Successfully")
    except subprocess.SubprocessError as exc:
        flash(f"Error in starting ROS2 node: {str(exc)}", "danger")
        LOGGER.error("Error in starting ROS2 node: %s", str(exc))
    return render_template("home.html")

@APP.route('/about', methods=['GET', 'POST'])
def about():
    """
    Route for rendering the about page.
    """
    LOGGER.info('About page requested')
    return render_template('about.html')

@APP.route('/service', methods=['GET', 'POST'])
def service():
    """
    Route for rendering the service page and starting the ROS node.
    """
    start_ros_node()
    return render_template('service.html')

if __name__ == '__main__':
    # Initialize SocketIO for Flask application
    SOCKETIO.init_app(APP)
    # Run the Flask application with SocketIO
    SOCKETIO.run(APP, host='0.0.0.0', port=5000, debug=True)
