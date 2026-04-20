"""
Serial communication module for the Truck Scale Weighing System.
Handles all serial port operations including main scale connection, emulator,
and big display communication.
"""

import serial
import serial.tools.list_ports
import threading
import time
import re
import logging
from datetime import datetime
from typing import Optional, Callable, List, Dict, Any

from config import (
    PREDEFINED_REGEXES, REQUIRED_WEIGHT_STABILITY, 
    MAX_WEIGHT_DEVIATION, DEFAULT_BAUD_RATE, DEFAULT_READ_INTERVAL_MS
)


class SerialManager:
    """Manages all serial communication for the weighing scale application."""
    
    def __init__(self, msg_box=None, update_callback: Optional[Callable] = None):
        """
        Initialize the serial manager.
        
        Args:
            msg_box: Message box instance for error reporting
            update_callback: Callback function for UI updates
        """
        self.msg_box = msg_box
        self.update_callback = update_callback
        
        # Main scale connection
        self.serial_port: Optional[serial.Serial] = None
        self.serial_running = False
        self.serial_thread: Optional[threading.Thread] = None
        self.last_serial_line = ""
        self.regex_fail_count = 0
        
        # Emulator connection
        self.emulator_serial_port: Optional[serial.Serial] = None
        self.emulator_sending_data = False
        self.emulator_send_thread: Optional[threading.Thread] = None
        
        # Big display connection
        self.big_display_serial_port: Optional[serial.Serial] = None
        self.big_display_connected = False
        self.big_display_send_thread: Optional[threading.Thread] = None
        self.last_sent_weight: Optional[float] = None
        
        # Configuration variables (will be set by the main application)
        self.data_format_regex = PREDEFINED_REGEXES[5]  # Default regex
        self.decimal_places = 0
        self.read_loop_interval_ms = DEFAULT_READ_INTERVAL_MS
        self.max_weight_deviation = MAX_WEIGHT_DEVIATION
        
        # Callbacks for weight updates
        self.weight_update_callback: Optional[Callable[[float], None]] = None
        self.status_update_callback: Optional[Callable[[str, str], None]] = None
        self.big_display_callback: Optional[Callable[[float, str, str], None]] = None

    def get_available_ports(self) -> List[str]:
        """
        Returns a list of available serial port names.
        
        Returns:
            List of available serial port device names
        """
        try:
            return [port.device for port in serial.tools.list_ports.comports()]
        except Exception as e:
            logging.error(f"Error getting serial ports: {e}")
            return []

    def start_main_scale_connection(self, port: str, baud_rate: int) -> bool:
        """
        Starts the main scale serial connection and reading thread.
        
        Args:
            port: Serial port name
            baud_rate: Baud rate for communication
            
        Returns:
            True if connection successful, False otherwise
        """
        if self.emulator_sending_data:
            self.stop_emulator_connection()
            if self.msg_box:
                self.msg_box.showinfo("Info", "Emulator sending stopped to allow Main Scale connection.")

        if self.serial_running:
            self.stop_main_scale_connection()

        try:
            self.serial_port = serial.Serial(port, baudrate=baud_rate, timeout=0.01)
            self.serial_running = True
            self.serial_thread = threading.Thread(
                target=self._read_main_scale_data,
                daemon=True
            )
            self.serial_thread.start()
            
            # Notify successful connection
            if self.status_update_callback:
                self.status_update_callback("Live Scale", "green")
            
            logging.info(f"Successfully connected to main scale on {port} at {baud_rate} baud")
            return True
            
        except serial.SerialException as e:
            error_msg = f"Could not open main serial port {port}: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Serial Error", error_msg)
            if self.status_update_callback:
                self.status_update_callback("Error", "red")
            return False
        except Exception as e:
            error_msg = f"An unexpected error occurred: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Serial Error", error_msg)
            if self.status_update_callback:
                self.status_update_callback("Error", "red")
            return False

    def stop_main_scale_connection(self):
        """Stops the main scale serial connection and cleans up resources."""
        self.serial_running = False
        
        if self.serial_thread and self.serial_thread.is_alive():
            self.serial_thread.join(timeout=2)
        
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
            except Exception as e:
                logging.error(f"Error closing main serial port: {e}")
        
        self.serial_port = None
        
        # Notify disconnection
        if self.status_update_callback:
            self.status_update_callback("Disconnected", "gray")
        
        logging.info("Main scale connection stopped")

    def _read_main_scale_data(self):
        """
        Main loop for reading data from the main scale serial port.
        Handles data parsing, stability checking, and callbacks.
        """
        current_stable_weight: Optional[float] = None
        stability_count = 0

        while self.serial_running:
            try:
                if not self.serial_port or not self.serial_port.is_open:
                    if self.status_update_callback:
                        self.status_update_callback("Disconnected", "gray")
                    time.sleep(2)
                    continue

                line = self.serial_port.readline().decode(errors='ignore').strip()
                self.last_serial_line = line

                if line:
                    match = re.search(self.data_format_regex, line)
                    if match:
                        self.regex_fail_count = 0
                        try:
                            extracted_weight = float(match.group(1))

                            # Update weight display via callback
                            if self.weight_update_callback:
                                format_string = f"%.{self.decimal_places}f"
                                self.weight_update_callback(extracted_weight)

                            # Update status if not in special modes
                            if self.status_update_callback:
                                current_status = getattr(self, '_current_status', '')
                                if "Loaded Gross" not in current_status and \
                                   "Editing ID" not in current_status and \
                                   "EXPIRED" not in current_status:
                                    self.status_update_callback("Live Scale", "green")

                            # Check for weight stability
                            if current_stable_weight is None or abs(current_stable_weight - extracted_weight) >= 0.01:
                                current_stable_weight = extracted_weight
                                stability_count = 1
                            else:
                                stability_count += 1

                            # Send stable weight to big display
                            if stability_count >= REQUIRED_WEIGHT_STABILITY:
                                if self.big_display_callback:
                                    self.big_display_callback(extracted_weight, "N/A", "N/A")

                        except (ValueError, IndexError):
                            self.regex_fail_count += 1
                            logging.warning(f"Failed to parse weight from: {line}")
                    else:
                        self.regex_fail_count += 1
                        
                        if self.regex_fail_count > 3:
                            if self.status_update_callback:
                                self.status_update_callback("No Match", "orange")

                        if self.regex_fail_count > 10:
                            # Auto-detect if enabled (implementation depends on main app)
                            if hasattr(self, '_auto_detect_regex_enabled') and self._auto_detect_regex_enabled:
                                new_regex = self._auto_detect_regex(line)
                                if new_regex:
                                    self.data_format_regex = new_regex
                                    logging.info(f"Auto-detected regex: {new_regex}")

                time.sleep(self.read_loop_interval_ms / 1000.0)

            except serial.SerialException as e:
                logging.error(f"Serial communication error: {e}")
                if self.status_update_callback:
                    self.status_update_callback("Error", "red")
                time.sleep(1)
            except Exception as e:
                logging.error(f"Unexpected error in serial reading: {e}")
                time.sleep(1)

    def start_emulator_connection(self, port: str, baud_rate: int) -> bool:
        """
        Starts the emulator serial connection.
        
        Args:
            port: Serial port name
            baud_rate: Baud rate for communication
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.emulator_serial_port = serial.Serial(port, baudrate=baud_rate, timeout=1)
            logging.info(f"Emulator connected on {port} at {baud_rate} baud")
            return True
        except serial.SerialException as e:
            error_msg = f"Could not open emulator serial port {port}: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Emulator Error", error_msg)
            return False

    def stop_emulator_connection(self):
        """Stops the emulator connection and data sending."""
        self.emulator_sending_data = False
        
        if self.emulator_send_thread and self.emulator_send_thread.is_alive():
            self.emulator_send_thread.join(timeout=2)
        
        if self.emulator_serial_port and self.emulator_serial_port.is_open:
            try:
                self.emulator_serial_port.close()
            except Exception as e:
                logging.error(f"Error closing emulator serial port: {e}")
        
        self.emulator_serial_port = None
        logging.info("Emulator connection stopped")

    def start_emulator_data_sending(self, weight: float, interval: float):
        """
        Starts sending weight data through the emulator port.
        
        Args:
            weight: Weight value to send
            interval: Send interval in seconds
        """
        if not self.emulator_serial_port or not self.emulator_serial_port.is_open:
            if self.msg_box:
                self.msg_box.showerror("Emulator Error", "Emulator not connected")
            return

        self.emulator_sending_data = True
        self.emulator_send_thread = threading.Thread(
            target=self._send_emulator_data,
            args=(weight, interval),
            daemon=True
        )
        self.emulator_send_thread.start()

    def _send_emulator_data(self, weight: float, interval: float):
        """
        Thread function to send emulator data.
        
        Args:
            weight: Weight value to send
            interval: Send interval in seconds
        """
        while self.emulator_sending_data:
            try:
                if self.emulator_serial_port and self.emulator_serial_port.is_open:
                    # Send weight in the expected format
                    data = f"ww{int(weight * 1000):08d}\r\n"
                    self.emulator_serial_port.write(data.encode())
                    logging.debug(f"Sent emulator data: {data.strip()}")
                time.sleep(interval)
            except Exception as e:
                logging.error(f"Error sending emulator data: {e}")
                break

    def connect_big_display(self, port: str, baud_rate: int) -> bool:
        """
        Connects to the big display serial port.
        
        Args:
            port: Serial port name
            baud_rate: Baud rate for communication
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.big_display_serial_port = serial.Serial(port, baudrate=baud_rate, timeout=1)
            self.big_display_connected = True
            logging.info(f"Big display connected on {port} at {baud_rate} baud")
            return True
        except serial.SerialException as e:
            error_msg = f"Could not open big display serial port {port}: {e}"
            logging.error(error_msg)
            if self.msg_box:
                self.msg_box.showerror("Big Display Error", error_msg)
            return False

    def disconnect_big_display(self):
        """Disconnects from the big display."""
        self.big_display_connected = False
        
        if self.big_display_serial_port and self.big_display_serial_port.is_open:
            try:
                self.big_display_serial_port.close()
            except Exception as e:
                logging.error(f"Error closing big display serial port: {e}")
        
        self.big_display_serial_port = None
        logging.info("Big display disconnected")

    def send_weight_to_big_display(self, weight: float, date: str, time: str):
        """
        Sends weight data to the big display.
        
        Args:
            weight: Weight value to display
            date: Date string
            time: Time string
        """
        if not self.big_display_connected or not self.big_display_serial_port:
            return
        
        # Avoid sending the same weight repeatedly
        if self.last_sent_weight is not None and abs(self.last_sent_weight - weight) < 0.01:
            return
        
        try:
            # Format the data for the big display
            format_string = f"%.{self.decimal_places}f"
            weight_str = format_string % weight
            data = f"{weight_str} {date} {time}\r\n"
            
            self.big_display_serial_port.write(data.encode())
            self.last_sent_weight = weight
            logging.debug(f"Sent to big display: {data.strip()}")
        except Exception as e:
            logging.error(f"Error sending to big display: {e}")

    def set_configuration(self, config: Dict[str, Any]):
        """
        Update configuration parameters.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.data_format_regex = config.get('data_format_regex', self.data_format_regex)
        self.decimal_places = config.get('decimal_places', self.decimal_places)
        self.read_loop_interval_ms = config.get('read_loop_interval_ms', self.read_loop_interval_ms)
        self.max_weight_deviation = config.get('max_weight_deviation', self.max_weight_deviation)
        self._auto_detect_regex_enabled = config.get('auto_detect_regex_enabled', False)

    def _auto_detect_regex(self, line: str) -> Optional[str]:
        """
        Attempts to automatically detect a matching regex from the predefined list
        for a given line of serial data.
        
        Args:
            line: A line of serial data to analyze
            
        Returns:
            A matching regex pattern, or None if no match found
        """
        for regex_pattern in PREDEFINED_REGEXES:
            if regex_pattern == "Custom":
                continue
            try:
                match = re.search(regex_pattern, line)
                if match and match.group(1):
                    # Verify the matched group can be converted to a float
                    float(match.group(1))
                    return regex_pattern
            except (ValueError, IndexError, re.error):
                continue
        return None

    def cleanup(self):
        """Clean up all serial connections and threads."""
        self.stop_main_scale_connection()
        self.stop_emulator_connection()
        self.disconnect_big_display()
        logging.info("Serial manager cleanup completed")
