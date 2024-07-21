import tkinter as tk
import subprocess

def run_ros2_and_script():
    command = """
    cd /home/af/siva &&
    . install/setup.bash &&
    cd park_app &&
    python3 app.py; bash
    """
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])

def ego_local():
    command = """
    cd /home/af/siva &&
    . install/setup.bash &&
    ros2 run ego_localization ego_localization; bash
    """
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])

root = tk.Tk()
root.title("ROS2 Script Runner")

# Button for running the mobile interface script
mobile_interface_button = tk.Button(root, text="Mobile Interface", command=run_ros2_and_script)
mobile_interface_button.pack(padx=20, pady=20)

# Button for running the ego localization script
ego_loc_button = tk.Button(root, text="Ego Localization", command=ego_local)
ego_loc_button.pack(padx=20, pady=20)

root.mainloop()
