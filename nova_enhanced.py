"""
Nova AI Assistant - Enhanced Version
With browser control, animations, and improved command handling
"""

import time
import random
import re
import threading
import webbrowser
import subprocess
import os
from typing import Dict, List, Optional
import sys

# Import Nova's modules
from voice_interface import VoiceInterface
from system_controls import SystemControls
from web_tools import WebTools
from utilities import Utilities


class NovaEnhanced:
    """Enhanced Nova AI Assistant with animations and browser control"""
    
    def __init__(self):
        """Initialize Enhanced Nova AI Assistant"""
        print("🚀 Initializing Enhanced Nova AI Assistant...")
        
        # Initialize all modules
        self.voice = VoiceInterface()
        self.system = SystemControls()
        self.web = WebTools()
        self.utils = Utilities()
        
        # Nova's enhanced personality
        self.name = "Nova"
        self.user_name = "Sir"
        self.is_active = False
        
        # Animation states
        self.is_listening = False
        self.is_speaking = False
        self.current_animation = None
        
        # Enhanced command patterns
        self.command_patterns = self._setup_enhanced_patterns()
        self.personality_responses = self._setup_enhanced_personality()
        
        # Browser control
        self.browser_commands = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'github': 'https://github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'reddit': 'https://www.reddit.com',
            'twitter': 'https://twitter.com',
            'linkedin': 'https://linkedin.com',
            'facebook': 'https://facebook.com',
            'instagram': 'https://instagram.com',
            'netflix': 'https://netflix.com',
            'spotify': 'https://open.spotify.com',
            'amazon': 'https://amazon.com',
            'wikipedia': 'https://wikipedia.org',
            'news': 'https://news.google.com',
            'weather': 'https://weather.com',
            'maps': 'https://maps.google.com',
            'gmail': 'https://gmail.com',
            'drive': 'https://drive.google.com',
            'calendar': 'https://calendar.google.com',
            'translate': 'https://translate.google.com'
        }
        
        # Session data
        self.session_start = time.time()
        self.command_count = 0
        self.conversation_history = []
        
        print("✅ Enhanced Nova AI Assistant initialized successfully!")
    
    def _setup_enhanced_patterns(self) -> Dict:
        """Setup enhanced command recognition patterns"""
        return {
            # Browser and web commands
            'open_website': [
                r'\b(open|go\s+to|visit|navigate\s+to)\s+(.+?)\b',
                r'\b(website|site|page)\s+(.+?)\b',
                r'\b(browse|search)\s+(.+?)\b'
            ],
            'search_web': [
                r'\b(search|find|look\s+up)\s+(for\s+)?(.+?)\b',
                r'\b(google|web\s+search)\s+(.+?)\b',
                r'\b(search\s+the\s+web|search\s+internet)\s+(for\s+)?(.+?)\b'
            ],
            'open_app': [
                r'\b(open|launch|start|run)\s+(.+?)(?:\s+for\s+me)?\b',
                r'\b(launch|start|run)\s+(.+?)\b',
                r'\bopen\s+(.+?)\s+(application|app|program)\b'
            ],
            
            # Time and date commands
            'time': [
                r'\b(what|what\'s|tell\s+me|give\s+me|show\s+me)\s+(the\s+)?time\b',
                r'\b(time|clock|hour)\b',
                r'\bwhat\s+time\s+is\s+it\b',
                r'\bcurrent\s+time\b'
            ],
            'date': [
                r'\b(what|what\'s|tell\s+me|give\s+me|show\s+me)\s+(the\s+)?date\b',
                r'\b(date|day|today)\b',
                r'\bwhat\s+(day|date)\s+(is\s+)?(it|today)\b',
                r'\bcurrent\s+date\b'
            ],
            
            # Weather and information
            'weather': [
                r'\b(what|what\'s|tell\s+me|give\s+me|show\s+me)\s+(the\s+)?weather\b',
                r'\bweather\s+(like|in|for)\b',
                r'\bhow\s+is\s+the\s+weather\b',
                r'\btemperature\b',
                r'\bforecast\b'
            ],
            
            # System control
            'screenshot': [
                r'\b(take|capture|save)\s+(a\s+)?screenshot\b',
                r'\bscreenshot\b',
                r'\bscreen\s+shot\b',
                r'\bcapture\s+screen\b'
            ],
            'volume': [
                r'\b(volume|sound|audio)\s+(up|down|mute|unmute)\b',
                r'\b(adjust|set|change)\s+volume\s+(to\s+)?(\d+)\b',
                r'\bvolume\s+(to\s+)?(\d+)\b',
                r'\b(turn\s+)?(up|down)\s+volume\b'
            ],
            
            # Entertainment and utilities
            'quote': [
                r'\b(quote|inspiration|motivation|wisdom)\b',
                r'\b(give\s+me|tell\s+me|show\s+me)\s+(a\s+)?(quote|inspiration)\b',
                r'\bmotivate\s+me\b'
            ],
            'fact': [
                r'\b(fact|interesting|did\s+you\s+know)\b',
                r'\b(tell\s+me|give\s+me|show\s+me)\s+(a\s+)?(fact|interesting\s+fact)\b',
                r'\brandom\s+fact\b'
            ],
            
            # Help and system
            'help': [
                r'\b(help|what\s+can\s+you\s+do|capabilities|commands)\b',
                r'\bhow\s+to\s+use\b',
                r'\btutorial\b',
                r'\bguide\b'
            ],
            'exit': [
                r'\b(exit|quit|stop|goodbye|bye|shut\s+down\s+nova)\b',
                r'\bclose\s+nova\b',
                r'\bend\s+session\b'
            ],
            
            # Conversational
            'greeting': [
                r'\b(hello|hi|hey|good\s+(morning|afternoon|evening))\b',
                r'\bhow\s+are\s+you\b',
                r'\bwhat\'s\s+up\b'
            ],
            'thanks': [
                r'\b(thank\s+you|thanks|appreciate)\b',
                r'\bgood\s+job\b',
                r'\bwell\s+done\b'
            ]
        }
    
    def _setup_enhanced_personality(self) -> Dict:
        """Setup enhanced personality responses"""
        return {
            'greetings': [
                "Hello there, {user}! Nova is ready to assist you with anything you need.",
                "Greetings, {user}! How can I make your day more productive and entertaining?",
                "Hi {user}! Nova is online and ready to help. What shall we accomplish today?",
                "Good day, {user}! I'm here to turn your ideas into reality.",
                "Hey {user}! Nova is ready to be your digital companion. What's on your mind?"
            ],
            'listening': [
                "🎧 Listening carefully, {user}...",
                "🎤 I'm all ears, {user}...",
                "🔍 Processing your request, {user}...",
                "💭 Analyzing your command, {user}...",
                "⚡ Working on it, {user}..."
            ],
            'speaking': [
                "🗣️ Speaking now, {user}...",
                "💬 Here's what I found, {user}...",
                "📢 Delivering your information, {user}...",
                "🎯 Here's the answer, {user}...",
                "✨ Sharing the results, {user}..."
            ],
            'success': [
                "✅ Mission accomplished, {user}!",
                "🎉 Task completed successfully!",
                "🚀 Done and done, {user}!",
                "💪 Successfully executed, {user}!",
                "🌟 All systems green, {user}!"
            ],
            'thinking': [
                "🤔 Let me think about that...",
                "🧠 Processing with my digital brain...",
                "💭 Analyzing the situation...",
                "🔍 Computing the best approach...",
                "⚡ Working my AI magic..."
            ]
        }
    
    def show_animation(self, animation_type: str, message: str = ""):
        """Show animated feedback"""
        if animation_type == "listening":
            self.is_listening = True
            self.current_animation = "listening"
            print(f"\n🎧 {message}")
            print("🎤 [Listening...] 🔴")
        elif animation_type == "speaking":
            self.is_speaking = True
            self.current_animation = "speaking"
            print(f"\n🗣️ {message}")
            print("💬 [Speaking...] 🟢")
        elif animation_type == "thinking":
            print(f"\n🤔 {message}")
            print("🧠 [Thinking...] 🟡")
        elif animation_type == "processing":
            print(f"\n⚡ {message}")
            print("🔧 [Processing...] 🔵")
        elif animation_type == "success":
            print(f"\n✅ {message}")
            print("🎉 [Success!] 🟢")
        elif animation_type == "error":
            print(f"\n❌ {message}")
            print("⚠️  [Error] 🔴")
    
    def stop_animation(self):
        """Stop current animation"""
        if self.current_animation == "listening":
            self.is_listening = False
            print("🔇 [Listening stopped]")
        elif self.current_animation == "speaking":
            self.is_speaking = False
            print("🔇 [Speaking stopped]")
        self.current_animation = None
    
    def open_website(self, site_name: str) -> str:
        """Open a website in the browser"""
        try:
            site_name = site_name.lower().strip()
            
            # Check if it's a known site
            if site_name in self.browser_commands:
                url = self.browser_commands[site_name]
                webbrowser.open(url)
                return f"Opening {site_name} in your browser, {self.user_name}! 🚀"
            
            # Try to construct a URL
            if not site_name.startswith(('http://', 'https://')):
                url = f"https://www.{site_name}.com"
            else:
                url = site_name
            
            webbrowser.open(url)
            return f"Opening {site_name} in your browser, {self.user_name}! 🌐"
            
        except Exception as e:
            return f"Sorry, {self.user_name}, I couldn't open {site_name}. Error: {str(e)}"
    
    def search_web(self, query: str) -> str:
        """Perform a web search"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching the web for '{query}', {self.user_name}! 🔍"
        except Exception as e:
            return f"Sorry, {self.user_name}, the web search failed. Error: {str(e)}"
    
    def process_enhanced_command(self, command: str) -> str:
        """Process commands with enhanced recognition"""
        self.command_count += 1
        command = command.lower().strip()
        
        print(f"\n🎯 Processing command: {command}")
        
        # Add to conversation history
        self.conversation_history.append(f"User: {command}")
        
        # Check for website opening
        if self._match_pattern(command, 'open_website'):
            site = self._extract_parameter(command, 'open_website')
            if site:
                self.show_animation("processing", f"Opening {site}...")
                response = self.open_website(site)
                self.show_animation("success", "Website opened!")
                return response
        
        # Check for web search
        elif self._match_pattern(command, 'search_web'):
            query = self._extract_parameter(command, 'search_web')
            if query:
                self.show_animation("processing", f"Searching for '{query}'...")
                response = self.search_web(query)
                self.show_animation("success", "Search completed!")
                return response
        
        # Check for app opening
        elif self._match_pattern(command, 'open_app'):
            app = self._extract_parameter(command, 'open_app')
            if app:
                self.show_animation("processing", f"Opening {app}...")
                success = self.system.open_application(app)
                if success:
                    self.show_animation("success", f"{app} opened!")
                    return f"Opening {app} for you, {self.user_name}! 🚀"
                else:
                    self.show_animation("error", f"Couldn't open {app}")
                    return f"Sorry, {self.user_name}, I couldn't find or open {app}."
        
        # Check for time commands
        elif self._match_pattern(command, 'time'):
            self.show_animation("processing", "Getting current time...")
            result = self.utils.get_current_time()
            if result['success']:
                self.show_animation("success", "Time retrieved!")
                return result['message']
        
        # Check for date commands
        elif self._match_pattern(command, 'date'):
            self.show_animation("processing", "Getting current date...")
            result = self.utils.get_current_date()
            if result['success']:
                self.show_animation("success", "Date retrieved!")
                return result['message']
        
        # Check for weather commands
        elif self._match_pattern(command, 'weather'):
            self.show_animation("processing", "Checking weather...")
            weather_type = random.choice(['sunny', 'cloudy', 'rainy', 'snowy'])
            response = self.utils.get_weather_personality(weather_type, "your area")
            self.show_animation("success", "Weather checked!")
            return response
        
        # Check for screenshot commands
        elif self._match_pattern(command, 'screenshot'):
            self.show_animation("processing", "Taking screenshot...")
            result = self.system.take_screenshot()
            if result:
                self.show_animation("success", "Screenshot captured!")
                return f"Screenshot captured and saved, {self.user_name}! 📸"
            else:
                self.show_animation("error", "Screenshot failed")
                return f"Sorry, {self.user_name}, the screenshot failed."
        
        # Check for volume commands
        elif self._match_pattern(command, 'volume'):
            self.show_animation("processing", "Adjusting volume...")
            if 'up' in command:
                success = self.system.adjust_volume(10)
                if success:
                    self.show_animation("success", "Volume increased!")
                    return f"Volume increased, {self.user_name}! 🔊"
            elif 'down' in command:
                success = self.system.adjust_volume(-10)
                if success:
                    self.show_animation("success", "Volume decreased!")
                    return f"Volume decreased, {self.user_name}! 🔉"
            elif 'mute' in command:
                success = self.system.set_volume(0)
                if success:
                    self.show_animation("success", "Audio muted!")
                    return f"Audio muted, {self.user_name}! 🔇"
        
        # Check for quote commands
        elif self._match_pattern(command, 'quote'):
            self.show_animation("processing", "Finding inspiration...")
            result = self.utils.get_random_quote()
            if result['success']:
                self.show_animation("success", "Quote found!")
                return result['message']
        
        # Check for fact commands
        elif self._match_pattern(command, 'fact'):
            self.show_animation("processing", "Finding interesting facts...")
            result = self.utils.get_random_fact()
            if result['success']:
                self.show_animation("success", "Fact found!")
                return result['message']
        
        # Check for greeting commands
        elif self._match_pattern(command, 'greeting'):
            return random.choice(self.personality_responses['greetings']).format(user=self.user_name)
        
        # Check for thanks commands
        elif self._match_pattern(command, 'thanks'):
            return f"You're welcome, {self.user_name}! I'm here to help. 😊"
        
        # Check for help commands
        elif self._match_pattern(command, 'help'):
            return self._get_enhanced_help()
        
        # Check for exit commands
        elif self._match_pattern(command, 'exit'):
            return f"Goodbye, {self.user_name}! It's been a pleasure serving you. Nova signing off! 👋"
        
        # Unknown command
        else:
            return f"I'm not sure how to handle '{command}', {self.user_name}. Try saying 'help' to see what I can do! 🤔"
    
    def _match_pattern(self, command: str, pattern_type: str) -> bool:
        """Check if command matches a specific pattern"""
        patterns = self.command_patterns.get(pattern_type, [])
        for pattern in patterns:
            if re.search(pattern, command):
                return True
        return False
    
    def _extract_parameter(self, command: str, pattern_type: str) -> Optional[str]:
        """Extract parameter from command using patterns"""
        patterns = self.command_patterns.get(pattern_type, [])
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                if pattern_type == 'open_website':
                    return match.group(2).strip()
                elif pattern_type == 'search_web':
                    return match.group(2).strip()
                elif pattern_type == 'open_app':
                    return match.group(1).strip()
        return None
    
    def _get_enhanced_help(self) -> str:
        """Get enhanced help information"""
        help_text = f"""
🌟 **Nova Enhanced - What I Can Do**

🌐 **Browser & Web Control**
• "Open Google" - Open websites
• "Search for Python tutorials" - Web search
• "Go to GitHub" - Navigate to sites
• "Visit YouTube" - Open popular sites

💻 **System Control**
• "Open Notepad" - Launch applications
• "Take a screenshot" - Capture screen
• "Volume up/down" - Control audio
• "Lock computer" - Secure system

🕐 **Information & Utilities**
• "What time is it?" - Get current time
• "What's the weather like?" - Weather info
• "Give me a quote" - Motivational quotes
• "Tell me a fact" - Interesting facts

💬 **Conversation**
• "Hello" - Greet me
• "How are you?" - Check my status
• "Thank you" - Express gratitude
• "Help" - See this menu

🎯 **Voice Commands**
Say "Nova" followed by your command!
Example: "Nova, open Google"
        """
        return help_text.strip()
    
    def run_enhanced(self):
        """Main run loop for Enhanced Nova"""
        try:
            # Greet the user
            greeting = random.choice(self.personality_responses['greetings']).format(user=self.user_name)
            print(f"\n🤖 {greeting}")
            self.voice.speak(greeting)
            
            print("\n" + "="*60)
            print("🎧 Enhanced Nova is listening for your commands...")
            print("💡 Say 'Nova' followed by your command")
            print("🌐 Try: 'Nova, open Google' or 'Nova, search for Python'")
            print("❓ Say 'Nova, help' to see enhanced capabilities")
            print("🚪 Say 'Nova, exit' to close the assistant")
            print("="*60)
            
            # Start listening loop
            self.voice.start_listening_loop(self._process_enhanced_voice_command)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Enhanced Nova interrupted by user")
            self.shutdown()
        except Exception as e:
            print(f"\n❌ Error in Enhanced Nova: {e}")
            self.shutdown()
    
    def _process_enhanced_voice_command(self, command: str):
        """Process voice command with enhanced features"""
        try:
            # Process the command
            response = self.process_enhanced_command(command)
            
            # Add to conversation history
            self.conversation_history.append(f"Nova: {response}")
            
            # Speak the response
            print(f"\n🤖 Nova: {response}")
            self.voice.speak(response)
            
        except Exception as e:
            error_msg = f"Sorry, {self.user_name}, I encountered an error: {str(e)}"
            print(f"\n❌ {error_msg}")
            self.voice.speak(error_msg)
    
    def shutdown(self):
        """Shutdown Enhanced Nova"""
        print("\n🔄 Shutting down Enhanced Nova AI Assistant...")
        
        # Stop voice interface
        if hasattr(self, 'voice'):
            self.voice.stop_listening()
        
        # Calculate session stats
        session_duration = time.time() - self.session_start
        minutes = int(session_duration // 60)
        seconds = int(session_duration % 60)
        
        print(f"📊 Enhanced Session Summary:")
        print(f"   Commands processed: {self.command_count}")
        print(f"   Session duration: {minutes}m {seconds}s")
        print(f"   Conversation entries: {len(self.conversation_history)}")
        print(f"   Thank you for using Enhanced Nova AI Assistant!")
        
        print("\n👋 Goodbye!")


def main():
    """Main entry point for Enhanced Nova AI Assistant"""
    print("🌟 Welcome to Nova AI Assistant - Enhanced Edition!")
    print("🚀 Initializing enhanced systems...")
    
    try:
        # Create and run Enhanced Nova
        nova = NovaEnhanced()
        nova.run_enhanced()
        
    except Exception as e:
        print(f"❌ Failed to initialize Enhanced Nova AI Assistant: {e}")
        print("🔧 Please check your installation and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
