"""
Nova AI Assistant - Installation Script
Helps users install dependencies and set up Nova AI Assistant
"""

import subprocess
import sys
import os
import platform


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python {version.major}.{version.minor} detected.")
        print("   Nova AI Assistant requires Python 3.11 or higher.")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
    return True


def check_pip():
    """Check if pip is available"""
    print("\n📦 Checking pip availability...")
    
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        print("❌ pip not found. Please install pip first.")
        return False


def install_requirements():
    """Install required packages"""
    print("\n📥 Installing required packages...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False


def install_pyaudio_windows():
    """Install PyAudio on Windows (special handling)"""
    print("\n🔊 Installing PyAudio for Windows...")
    
    try:
        # Try installing pipwin first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
        print("✅ pipwin installed successfully!")
        
        # Install PyAudio using pipwin
        subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
        print("✅ PyAudio installed successfully!")
        return True
        
    except subprocess.CalledProcessError:
        print("⚠️  pipwin method failed. Trying alternative...")
        
        try:
            # Try direct installation
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyAudio"])
            print("✅ PyAudio installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyAudio installation failed.")
            print("   Please install PyAudio manually:")
            print("   1. Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
            print("   2. Install with: pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl")
            return False


def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing module imports...")
    
    required_modules = [
        'speech_recognition',
        'pyttsx3',
        'pywhatkit',
        'wikipedia',
        'requests',
        'PIL',
        'pyautogui',
        'psutil'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All modules imported successfully!")
    return True


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating necessary directories...")
    
    directories = ['screenshots', 'logs', 'temp']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")


def run_tests():
    """Run basic tests"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test individual components
        subprocess.check_call([sys.executable, "demo.py"])
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Some tests failed. Check the output above for details.")
        return False


def main():
    """Main installation function"""
    print("🌟 Nova AI Assistant - Installation Script")
    print("=" * 50)
    print("This script will help you install Nova AI Assistant")
    print("and all its dependencies.")
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    if not check_pip():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Special handling for PyAudio on Windows
    if platform.system().lower() == "windows":
        if not install_pyaudio_windows():
            print("\n⚠️  PyAudio installation failed. You may need to install it manually.")
            print("   Nova will still work, but voice features may not function properly.")
    
    # Test imports
    if not test_imports():
        print("\n❌ Some modules failed to import.")
        print("   Please check the error messages above and try reinstalling.")
        return False
    
    # Create directories
    create_directories()
    
    # Run tests
    print("\n🎯 Installation completed! Running tests...")
    if run_tests():
        print("\n🎉 Nova AI Assistant is ready to use!")
        print("\n💡 To start Nova:")
        print("   python main.py")
        print("\n💡 To run tests:")
        print("   python demo.py")
        print("\n💡 For help:")
        print("   python main.py --help")
        return True
    else:
        print("\n⚠️  Installation completed with warnings.")
        print("   Some features may not work properly.")
        return False


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 Ready to meet your AI companion!")
        else:
            print("\n❌ Installation failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Installation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        sys.exit(1)
