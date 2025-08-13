"""
Nova AI Assistant - Demo Script
Test individual components without running the full voice interface
"""

import time
from voice_interface import VoiceInterface
from system_controls import SystemControls
from web_tools import WebTools
from utilities import Utilities


def test_voice_interface():
    """Test the voice interface components"""
    print("🎤 Testing Voice Interface")
    print("=" * 40)
    
    voice = VoiceInterface()
    
    # Test speakers
    print("🔊 Testing speakers...")
    voice.test_speakers()
    
    # Test microphone
    print("\n🎤 Testing microphone...")
    if voice.test_microphone():
        print("✅ Microphone test passed!")
    else:
        print("❌ Microphone test failed!")
    
    print()


def test_system_controls():
    """Test the system controls"""
    print("💻 Testing System Controls")
    print("=" * 40)
    
    system = SystemControls()
    
    # Test system info
    print("📊 Getting system information...")
    info = system.get_system_info()
    for key, value in info.items():
        if key != 'disk_usage':
            print(f"  {key}: {value}")
    
    # Test volume
    print(f"\n🔊 Current volume: {system.get_volume_level()}%")
    
    print()


def test_web_tools():
    """Test the web tools"""
    print("🌐 Testing Web Tools")
    print("=" * 40)
    
    web = WebTools()
    
    # Test Wikipedia
    print("📚 Testing Wikipedia search...")
    result = web.search_wikipedia("artificial intelligence", sentences=2)
    if result['success']:
        print(f"✅ {result['message']}")
        if 'summary' in result:
            print(f"📖 Summary: {result['summary'][:100]}...")
    else:
        print(f"❌ {result['message']}")
    
    # Test weather (demo)
    print("\n🌤️ Testing weather info...")
    result = web.get_weather_info("London")
    if result['success']:
        print(f"✅ {result['message']}")
    
    # Test news
    print("\n📰 Testing news headlines...")
    result = web.get_news_headlines("technology", count=3)
    if result['success']:
        print(f"✅ {result['message']}")
        for i, headline in enumerate(result['headlines'], 1):
            print(f"  {i}. {headline}")
    
    print()


def test_utilities():
    """Test the utilities"""
    print("🔧 Testing Utilities")
    print("=" * 40)
    
    utils = Utilities()
    
    # Test time
    print("⏰ Testing time functions...")
    result = utils.get_current_time()
    if result['success']:
        print(f"✅ {result['message']}")
    
    # Test date
    print("\n📅 Testing date functions...")
    result = utils.get_current_date()
    if result['success']:
        print(f"✅ {result['message']}")
    
    # Test weather personality
    print("\n🌤️ Testing weather personality...")
    response = utils.get_weather_personality("sunny", "New York")
    print(f"✅ {response}")
    
    # Test random quote
    print("\n💭 Testing random quote...")
    result = utils.get_random_quote()
    if result['success']:
        print(f"✅ {result['message']}")
    
    # Test random fact
    print("\n🧠 Testing random fact...")
    result = utils.get_random_fact()
    if result['success']:
        print(f"✅ {result['message']}")
    
    print()


def test_command_processing():
    """Test command processing patterns"""
    print("🎯 Testing Command Processing")
    print("=" * 40)
    
    # Import the main class for testing
    try:
        from main import NovaAI
        nova = NovaAI()
        
        # Test some commands
        test_commands = [
            "what time is it",
            "what's the weather like",
            "open notepad",
            "search for Python tutorials",
            "tell me about artificial intelligence",
            "take a screenshot",
            "volume up",
            "give me a quote",
            "what's in the news",
            "help"
        ]
        
        print("Testing command processing...")
        for command in test_commands:
            response = nova.process_command(command)
            print(f"\n🎤 Command: {command}")
            print(f"🤖 Response: {response}")
        
    except ImportError as e:
        print(f"❌ Could not import NovaAI: {e}")
        print("Make sure all modules are properly installed.")
    
    print()


def main():
    """Main demo function"""
    print("🌟 Nova AI Assistant - Component Demo")
    print("=" * 60)
    print("This demo will test individual components of Nova AI Assistant")
    print("without running the full voice interface.")
    print()
    
    try:
        # Test each component
        test_voice_interface()
        test_system_controls()
        test_web_tools()
        test_utilities()
        test_command_processing()
        
        print("🎉 All component tests completed!")
        print("\n💡 To run the full Nova AI Assistant:")
        print("   python main.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check your installation and try again.")


if __name__ == "__main__":
    main()
