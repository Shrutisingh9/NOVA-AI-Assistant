"""
System Controls Module for Nova AI Assistant
Handles system operations like shutdown, restart, volume control, and screenshots
"""

import os
import subprocess
import platform
import pyautogui
import psutil
from datetime import datetime
from typing import Optional, Tuple
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class SystemControls:
    """Handles system control operations for Nova AI Assistant"""
    
    def __init__(self):
        """Initialize system controls"""
        self.system = platform.system().lower()
        self.volume_controller = None
        self._setup_volume_control()
    
    def _setup_volume_control(self):
        """Setup volume control for Windows"""
        try:
            if self.system == "windows":
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume_controller = cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            print(f"Warning: Could not setup volume control: {e}")
            self.volume_controller = None
    
    def open_application(self, app_name: str) -> bool:
        """
        Open a specified application
        
        Args:
            app_name: Name of the application to open
            
        Returns:
            True if successful, False otherwise
        """
        try:
            app_name = app_name.lower()
            
            # Common Windows applications
            app_mappings = {
                'chrome': 'chrome.exe',
                'google chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe',
                'notepad': 'notepad.exe',
                'wordpad': 'wordpad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'spotify': 'spotify.exe',
                'discord': 'discord.exe',
                'steam': 'steam.exe',
                'vscode': 'code.exe',
                'visual studio code': 'code.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe',
                'outlook': 'outlook.exe',
                'teams': 'teams.exe',
                'zoom': 'zoom.exe',
                'skype': 'skype.exe'
            }
            
            # Check if app name is in our mappings
            if app_name in app_mappings:
                executable = app_mappings[app_name]
                subprocess.Popen(executable, shell=True)
                return True
            
            # Try to find the app in common locations
            common_paths = [
                os.path.expanduser("~\\AppData\\Local\\Programs"),
                os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"),
                "C:\\Program Files",
                "C:\\Program Files (x86)"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.lower().startswith(app_name) and file.lower().endswith('.exe'):
                                full_path = os.path.join(root, file)
                                subprocess.Popen(full_path, shell=True)
                                return True
            
            # Try using start command for Windows
            if self.system == "windows":
                subprocess.run(['start', app_name], shell=True, check=True)
                return True
                
        except Exception as e:
            print(f"Error opening application {app_name}: {e}")
            return False
        
        return False
    
    def take_screenshot(self, save_path: Optional[str] = None) -> Optional[str]:
        """
        Take a screenshot of the current screen
        
        Args:
            save_path: Optional path to save the screenshot
            
        Returns:
            Path to saved screenshot or None if failed
        """
        try:
            if save_path is None:
                # Create default path with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = f"screenshot_{timestamp}.png"
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            
            print(f"📸 Screenshot saved to: {save_path}")
            return save_path
            
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def get_system_info(self) -> dict:
        """
        Get basic system information
        
        Returns:
            Dictionary containing system information
        """
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'hostname': platform.node(),
                'cpu_count': psutil.cpu_count(),
                'memory_total': f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
                'memory_available': f"{psutil.virtual_memory().available / (1024**3):.1f} GB",
                'disk_usage': {}
            }
            
            # Get disk usage for main drives
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info['disk_usage'][partition.device] = {
                        'total': f"{usage.total / (1024**3):.1f} GB",
                        'used': f"{usage.used / (1024**3):.1f} GB",
                        'free': f"{usage.free / (1024**3):.1f} GB",
                        'percent': f"{usage.percent:.1f}%"
                    }
                except:
                    continue
            
            return info
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {}
    
    def get_volume_level(self) -> Optional[int]:
        """
        Get current system volume level
        
        Returns:
            Volume level (0-100) or None if failed
        """
        try:
            if self.volume_controller:
                volume = self.volume_controller.GetMasterVolumeLevelScalar()
                return int(volume * 100)
            else:
                # Fallback method using PowerShell
                result = subprocess.run(
                    ['powershell', '-Command', '(Get-AudioDevice -Playback).Volume'],
                    capture_output=True, text=True, shell=True
                )
                if result.returncode == 0:
                    return int(result.stdout.strip())
        except Exception as e:
            print(f"Error getting volume level: {e}")
        
        return None
    
    def set_volume(self, level: int) -> bool:
        """
        Set system volume level
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure level is within bounds
            level = max(0, min(100, level))
            
            if self.volume_controller:
                # Convert percentage to scalar (0.0 to 1.0)
                scalar = level / 100.0
                self.volume_controller.SetMasterVolumeLevelScalar(scalar, None)
                return True
            else:
                # Fallback method using PowerShell
                result = subprocess.run(
                    ['powershell', '-Command', f'(Get-AudioDevice -Playback).Volume = {level}'],
                    shell=True
                )
                return result.returncode == 0
                
        except Exception as e:
            print(f"Error setting volume: {e}")
            return False
    
    def adjust_volume(self, change: int) -> bool:
        """
        Adjust volume by a relative amount
        
        Args:
            change: Volume change (-100 to +100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            current_volume = self.get_volume_level()
            if current_volume is not None:
                new_volume = current_volume + change
                return self.set_volume(new_volume)
            return False
        except Exception as e:
            print(f"Error adjusting volume: {e}")
            return False
    
    def shutdown_computer(self, delay: int = 0) -> bool:
        """
        Shutdown the computer
        
        Args:
            delay: Delay in seconds before shutdown (0 for immediate)
            
        Returns:
            True if command sent successfully, False otherwise
        """
        try:
            if self.system == "windows":
                if delay > 0:
                    subprocess.run(['shutdown', '/s', '/t', str(delay)], check=True)
                else:
                    subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
            else:
                # For other operating systems
                subprocess.run(['shutdown', '-h', 'now'], check=True)
            
            return True
            
        except Exception as e:
            print(f"Error shutting down computer: {e}")
            return False
    
    def restart_computer(self, delay: int = 0) -> bool:
        """
        Restart the computer
        
        Args:
            delay: Delay in seconds before restart (0 for immediate)
            
        Returns:
            True if command sent successfully, False otherwise
        """
        try:
            if self.system == "windows":
                if delay > 0:
                    subprocess.run(['shutdown', '/r', '/t', str(delay)], check=True)
                else:
                    subprocess.run(['shutdown', '/r', '/t', '0'], check=True)
            else:
                # For other operating systems
                subprocess.run(['shutdown', '-r', 'now'], check=True)
            
            return True
            
        except Exception as e:
            print(f"Error restarting computer: {e}")
            return False
    
    def cancel_shutdown(self) -> bool:
        """
        Cancel a pending shutdown/restart
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.system == "windows":
                subprocess.run(['shutdown', '/a'], check=True)
            else:
                # For other operating systems
                subprocess.run(['killall', 'shutdown'], check=True)
            
            return True
            
        except Exception as e:
            print(f"Error canceling shutdown: {e}")
            return False
    
    def lock_computer(self) -> bool:
        """
        Lock the computer
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.system == "windows":
                subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], check=True)
            else:
                # For other operating systems
                subprocess.run(['gnome-screensaver-command', '--lock'], check=True)
            
            return True
            
        except Exception as e:
            print(f"Error locking computer: {e}")
            return False
    
    def get_running_processes(self, limit: int = 20) -> list:
        """
        Get list of running processes
        
        Args:
            limit: Maximum number of processes to return
            
        Returns:
            List of process information
        """
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and return top processes
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            return processes[:limit]
            
        except Exception as e:
            print(f"Error getting running processes: {e}")
            return []
    
    def kill_process(self, process_name: str) -> bool:
        """
        Kill a process by name
        
        Args:
            process_name: Name of the process to kill
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        proc.terminate()
                        proc.wait(timeout=3)
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass
            
            return False
            
        except Exception as e:
            print(f"Error killing process {process_name}: {e}")
            return False


if __name__ == "__main__":
    # Test the system controls
    controls = SystemControls()
    
    print("🎯 Testing Nova's System Controls")
    print("=" * 40)
    
    # Test system info
    print("\n📊 System Information:")
    info = controls.get_system_info()
    for key, value in info.items():
        if key != 'disk_usage':
            print(f"  {key}: {value}")
    
    # Test volume control
    print(f"\n🔊 Current Volume: {controls.get_volume_level()}%")
    
    # Test application opening (commented out to avoid opening apps during testing)
    # print("\n🚀 Testing application opening...")
    # success = controls.open_application("notepad")
    # print(f"  Notepad opened: {success}")
    
    print("\n✅ System controls test completed!")
