"""
Nova AI Assistant - Launcher Script
Choose your preferred Nova experience
"""

import os
import sys
import subprocess


def show_menu():
    """Show the Nova launcher menu"""
    print("🌟" + "="*50 + "🌟")
    print("           NOVA AI ASSISTANT LAUNCHER")
    print("🌟" + "="*50 + "🌟")
    print()
    print("Choose your Nova experience:")
    print()
    print("1. 🚀 Enhanced Nova (Recommended)")
    print("   - Better command recognition")
    print("   - Browser control & web search")
    print("   - Enhanced personality")
    print("   - Visual feedback & animations")
    print()
    print("2. 🎭 Original Nova")
    print("   - Classic Nova experience")
    print("   - Basic command handling")
    print("   - Voice interface")
    print()
    print("3. 🖥️  Nova GUI")
    print("   - Graphical user interface")
    print("   - Visual animations")
    print("   - Click-to-test commands")
    print("   - Real-time conversation view")
    print()
    print("4. 🧪 Demo Mode")
    print("   - Test individual components")
    print("   - No voice interaction")
    print("   - Component verification")
    print()
    print("5. 🔧 Installation Helper")
    print("   - Install dependencies")
    print("   - Check system compatibility")
    print("   - Troubleshoot issues")
    print()
    print("0. 🚪 Exit")
    print()


def launch_enhanced_nova():
    """Launch Enhanced Nova"""
    print("🚀 Launching Enhanced Nova AI Assistant...")
    print("Features: Better commands, browser control, enhanced personality")
    print()
    
    try:
        subprocess.run([sys.executable, "nova_enhanced.py"])
    except FileNotFoundError:
        print("❌ Enhanced Nova not found. Running original Nova instead...")
        subprocess.run([sys.executable, "main.py"])
    except Exception as e:
        print(f"❌ Error launching Enhanced Nova: {e}")
        print("Falling back to original Nova...")
        subprocess.run([sys.executable, "main.py"])


def launch_original_nova():
    """Launch Original Nova"""
    print("🎭 Launching Original Nova AI Assistant...")
    print("Features: Classic experience, voice interface, basic commands")
    print()
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except FileNotFoundError:
        print("❌ Original Nova not found!")
        print("Please check your installation.")
    except Exception as e:
        print(f"❌ Error launching Original Nova: {e}")


def launch_gui_nova():
    """Launch Nova GUI"""
    print("🖥️  Launching Nova GUI...")
    print("Features: Visual interface, animations, click commands")
    print()
    
    try:
        subprocess.run([sys.executable, "nova_gui.py"])
    except FileNotFoundError:
        print("❌ Nova GUI not found!")
        print("Please check your installation.")
    except Exception as e:
        print(f"❌ Error launching Nova GUI: {e}")


def launch_demo():
    """Launch Demo Mode"""
    print("🧪 Launching Demo Mode...")
    print("Features: Component testing, no voice interaction")
    print()
    
    try:
        subprocess.run([sys.executable, "demo.py"])
    except FileNotFoundError:
        print("❌ Demo script not found!")
        print("Please check your installation.")
    except Exception as e:
        print(f"❌ Error launching Demo: {e}")


def launch_installer():
    """Launch Installation Helper"""
    print("🔧 Launching Installation Helper...")
    print("Features: Dependency installation, system checks")
    print()
    
    try:
        subprocess.run([sys.executable, "install.py"])
    except FileNotFoundError:
        print("❌ Installation script not found!")
        print("Please check your installation.")
    except Exception as e:
        print(f"❌ Error launching Installer: {e}")


def check_files():
    """Check which Nova files are available"""
    print("📁 Checking available Nova files...")
    print()
    
    files = {
        "main.py": "Original Nova",
        "nova_enhanced.py": "Enhanced Nova", 
        "nova_gui.py": "Nova GUI",
        "demo.py": "Demo Mode",
        "install.py": "Installation Helper"
    }
    
    available = []
    for file, description in files.items():
        if os.path.exists(file):
            print(f"✅ {file} - {description}")
            available.append(file)
        else:
            print(f"❌ {file} - {description}")
    
    print()
    return available


def main():
    """Main launcher function"""
    print("🌟 Welcome to Nova AI Assistant Launcher!")
    print()
    
    # Check available files
    available_files = check_files()
    
    if not available_files:
        print("❌ No Nova files found!")
        print("Please check your installation or run the installer.")
        return
    
    print("="*60)
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
            
            if choice == "0":
                print("👋 Goodbye! Thanks for using Nova AI Assistant!")
                break
            elif choice == "1":
                if "nova_enhanced.py" in available_files:
                    launch_enhanced_nova()
                else:
                    print("❌ Enhanced Nova not available. Choose another option.")
            elif choice == "2":
                if "main.py" in available_files:
                    launch_original_nova()
                else:
                    print("❌ Original Nova not available. Choose another option.")
            elif choice == "3":
                if "nova_gui.py" in available_files:
                    launch_gui_nova()
                else:
                    print("❌ Nova GUI not available. Choose another option.")
            elif choice == "4":
                if "demo.py" in available_files:
                    launch_demo()
                else:
                    print("❌ Demo mode not available. Choose another option.")
            elif choice == "5":
                if "install.py" in available_files:
                    launch_installer()
                else:
                    print("❌ Installation helper not available. Choose another option.")
            else:
                print("❌ Invalid choice. Please enter a number between 0-5.")
            
            print()
            input("Press Enter to return to menu...")
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Nova AI Assistant!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
