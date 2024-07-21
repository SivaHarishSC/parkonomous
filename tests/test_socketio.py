"""
This module contains tests for Socket.IO communication with the Flask application.
"""

import unittest
import asyncio
import threading
import logging
import socketio
from app import app  # Adjust the import based on your project structure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

def start_flask_app():
    """Start the Flask application in a separate thread."""
    LOGGER.info("Starting Flask application")
    app.run(host='0.0.0.0', port=5000, debug=False)

class TestSocketIOCommunication(unittest.TestCase):
    """Test case for Socket.IO communication."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        LOGGER.info("Setting up test class")
        cls.thread = threading.Thread(target=start_flask_app)
        cls.thread.daemon = True
        cls.thread.start()
        LOGGER.info("Flask application thread started")

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class."""
        LOGGER.info("Tearing down test class")
        cls.thread.join(timeout=1)
        LOGGER.info("Flask application thread joined")

    def setUp(self):
        """Set up each test case."""
        LOGGER.info("Setting up test case")
        self.sio = socketio.AsyncClient()

        async def connect():
            LOGGER.info('Socket.IO connection established')

        async def connect_error(data):
            LOGGER.error('Socket.IO connection failed: %s', data)

        async def disconnect():
            LOGGER.info('Disconnected from Socket.IO server')

        self.sio.on('connect', connect)
        self.sio.on('connect_error', connect_error)
        self.sio.on('disconnect', disconnect)

    async def tearDown(self):
        """Tear down each test case."""
        LOGGER.info("Tearing down test case")
        await self.sio.disconnect()
        LOGGER.info("Socket.IO client disconnected")

    async def test_socketio_communication(self):
        """Test Socket.IO communication."""
        LOGGER.info("Starting Socket.IO communication test")

        try:
            await self.sio.connect('http://localhost:5000')
            LOGGER.info("Connected to Socket.IO server")
            await asyncio.sleep(1)

            LOGGER.info("Testing 'pose_update' event")
            await self.sio.emit('pose_update', {'x': 1.0, 'y': 2.0})
            await asyncio.sleep(1)
            LOGGER.info("'pose_update' event emitted successfully")

            LOGGER.info("Testing 'user_update' event")
            await self.sio.emit('user_update', {'x': 3.0, 'y': 4.0})
            await asyncio.sleep(1)
            LOGGER.info("'user_update' event emitted successfully")

            LOGGER.info("Testing 'destination_reached' event")
            await self.sio.emit('destination_reached', {'reached': True})
            await asyncio.sleep(1)
            LOGGER.info("'destination_reached' event emitted successfully")

            self.assertFalse(self.sio.connected, "Expected Socket.IO client to be disconnected")
            LOGGER.info("Socket.IO client is disconnected as expected")

        except Exception as error:
            LOGGER.error("An error occurred during the test: %s", str(error))
            raise

        LOGGER.info("Socket.IO communication test completed successfully")

if __name__ == '__main__':
    LOGGER.info("Starting test suite")
    unittest.main()
