"""
Nova AI Assistant - Main Module
The core command handler and personality engine for Nova AI Assistant
Inspired by J.A.R.V.I.S. and F.R.I.D.A.Y. from Iron Man
"""

import time
import random
import re
from typing import Dict, List, Optional
import sys
import os

# Import Nova's modules
from voice_interface import VoiceInterface
from system_controls import SystemControls
from web_tools import WebTools
from utilities import Utilities


class NovaAI:
    """Nova AI Assistant - Your personal AI companion"""
    
    def __init__(self):
        """Initialize Nova AI Assistant"""
        print("🚀 Initializing Nova AI Assistant...")
        
        # Initialize all modules
        self.voice = VoiceInterface()
        self.system = SystemControls()
        self.web = WebTools()
        self.utils = Utilities()
        
        # Nova's personality traits
        self.name = "Nova"
        self.personality = {
            'greeting_style': 'friendly_witty',
            'response_style': 'professional_playful',
            'humor_level': 'moderate',
            'formality': 'casual_professional'
        }
        
        # Command patterns and responses
        self.command_patterns = self._setup_command_patterns()
        self.personality_responses = self._setup_personality_responses()
        
        # Session data
        self.session_start = time.time()
        self.command_count = 0
        self.user_name = "Sir"  # Default, can be personalized
        
        print("✅ Nova AI Assistant initialized successfully!")
    
    def _setup_command_patterns(self) -> Dict:
        """Setup command recognition patterns"""
        return {
            # Time and date commands
            'time': [
                r'\b(what|what\'s|tell me|give me|show me)\s+(the\s+)?time\b',
                r'\b(time|clock|hour)\b',
                r'\bwhat\s+time\s+is\s+it\b'
            ],
            'date': [
                r'\b(what|what\'s|tell me|give me|show me)\s+(the\s+)?date\b',
                r'\b(date|day|today)\b',
                r'\bwhat\s+(day|date)\s+(is\s+)?(it|today)\b'
            ],
            'datetime': [
                r'\b(what|what\'s|tell me|give me|show me)\s+(the\s+)?(time\s+and\s+)?date\b',
                r'\bcurrent\s+(time|date)\b',
                r'\bnow\b'
            ],
            
            # Weather commands
            'weather': [
                r'\b(what|what\'s|tell me|give me|show me)\s+(the\s+)?weather\b',
                r'\bweather\s+(like|in|for)\b',
                r'\bhow\s+is\s+the\s+weather\b',
                r'\btemperature\b'
            ],
            
            # Application commands
            'open_app': [
                r'\bopen\s+(.+?)(?:\s+for\s+me)?\b',
                r'\b(launch|start|run)\s+(.+?)\b',
                r'\bopen\s+(.+?)\s+application\b'
            ],
            
            # Web search commands
            'web_search': [
                r'\b(search|find|look\s+up)\s+(for\s+)?(.+?)\b',
                r'\bgoogle\s+(.+?)\b',
                r'\bsearch\s+the\s+web\s+for\s+(.+?)\b'
            ],
            
            # Wikipedia commands
            'wikipedia': [
                r'\b(wikipedia|wiki)\s+(.+?)\b',
                r'\btell\s+me\s+about\s+(.+?)\b',
                r'\bwhat\s+is\s+(.+?)\b',
                r'\bwho\s+is\s+(.+?)\b',
                r'\bdefine\s+(.+?)\b'
            ],
            
            # System control commands
            'screenshot': [
                r'\b(take|capture|save)\s+(a\s+)?screenshot\b',
                r'\bscreenshot\b',
                r'\bscreen\s+shot\b'
            ],
            'volume': [
                r'\b(volume|sound|audio)\s+(up|down|mute|unmute)\b',
                r'\b(adjust|set|change)\s+volume\s+(to\s+)?(\d+)\b',
                r'\bvolume\s+(to\s+)?(\d+)\b'
            ],
            'shutdown': [
                r'\b(shutdown|shut\s+down|turn\s+off|power\s+off)\s+(computer|pc|laptop)\b',
                r'\b(shutdown|shut\s+down|turn\s+off|power\s+off)\b'
            ],
            'restart': [
                r'\b(restart|reboot|reset)\s+(computer|pc|laptop)\b',
                r'\b(restart|reboot|reset)\b'
            ],
            'lock': [
                r'\b(lock|secure)\s+(computer|pc|laptop|screen)\b',
                r'\block\b'
            ],
            
            # Utility commands
            'quote': [
                r'\b(quote|inspiration|motivation|wisdom)\b',
                r'\b(give\s+me|tell\s+me|show\s+me)\s+(a\s+)?(quote|inspiration)\b'
            ],
            'fact': [
                r'\b(fact|interesting|did\s+you\s+know)\b',
                r'\b(tell\s+me|give\s+me|show\s+me)\s+(a\s+)?(fact|interesting\s+fact)\b'
            ],
            'status': [
                r'\b(status|health|how\s+are\s+you)\b',
                r'\b(system\s+)?status\b',
                r'\bhow\s+are\s+things\b'
            ],
            
            # YouTube search
            'youtube': [
                r'\b(youtube|video)\s+(.+?)\b',
                r'\bsearch\s+youtube\s+for\s+(.+?)\b',
                r'\bfind\s+video\s+(.+?)\b'
            ],
            
            # News
            'news': [
                r'\b(news|headlines|latest)\b',
                r'\bwhat\'s\s+in\s+the\s+news\b',
                r'\b(tell\s+me|give\s+me|show\s+me)\s+(the\s+)?(news|headlines)\b'
            ],
            
            # Help and system
            'help': [
                r'\b(help|what\s+can\s+you\s+do|capabilities|commands)\b',
                r'\bhow\s+to\s+use\b',
                r'\btutorial\b'
            ],
            'exit': [
                r'\b(exit|quit|stop|goodbye|bye|shut\s+down\s+nova)\b',
                r'\bclose\s+nova\b'
            ]
        }
    
    def _setup_personality_responses(self) -> Dict:
        """Setup Nova's personality responses"""
        return {
            'greetings': [
                "Greetings, {user}! Nova at your service, ready to make your day more efficient and slightly more entertaining.",
                "Hello there, {user}! Nova here, your AI companion for all things digital and delightful.",
                "Good day, {user}! Nova is online and ready to assist with your every whim and command.",
                "Greetings, {user}! Nova is here to turn your productivity up to eleven and add a dash of personality.",
                "Hello, {user}! Nova is ready to be your digital sidekick. What shall we accomplish today?"
            ],
            'confirmation': [
                "Consider it done, {user}!",
                "On it, {user}!",
                "Roger that, {user}!",
                "Affirmative, {user}!",
                "You got it, {user}!"
            ],
            'thinking': [
                "Processing your request with the speed of thought...",
                "Let me consult my digital brain...",
                "Analyzing the situation...",
                "Computing the best approach...",
                "Working my AI magic..."
            ],
            'success': [
                "Mission accomplished, {user}!",
                "Task completed successfully!",
                "Done and done, {user}!",
                "Successfully executed, {user}!",
                "All systems green, {user}!"
            ],
            'error': [
                "Well, that didn't go as planned. Let me try a different approach.",
                "Houston, we have a problem. But don't worry, I'm on it!",
                "Error detected, but I'm not giving up that easily!",
                "Something went sideways, {user}. Let me fix this!",
                "Technical difficulties, but I'm troubleshooting as we speak!"
            ],
            'clarification': [
                "I need a bit more clarity on that, {user}. Could you rephrase?",
                "Hmm, that's a bit fuzzy. Mind being more specific?",
                "I'm not quite catching your drift, {user}. Can you elaborate?",
                "That command needs some fine-tuning. What exactly did you have in mind?",
                "I'm getting mixed signals here. Could you clarify?"
            ],
            'unknown': [
                "That's a new one on me, {user}. I'm still learning, you know!",
                "Interesting request, but I'm not quite sure how to handle that yet.",
                "You're stretching my capabilities, {user}. Let me think about this...",
                "That's beyond my current skill set, but I'm always expanding my knowledge!",
                "I'm stumped, {user}. Maybe try rephrasing that?"
            ]
        }
    
    def get_personality_response(self, response_type: str, **kwargs) -> str:
        """Get a personality-driven response"""
        responses = self.personality_responses.get(response_type, [])
        if responses:
            response = random.choice(responses)
            return response.format(**kwargs)
        return f"Response type '{response_type}' not found."
    
    def greet_user(self) -> str:
        """Generate a personalized greeting"""
        greeting = self.get_personality_response('greetings', user=self.user_name)
        return greeting
    
    def process_command(self, command: str) -> str:
        """Process user command and return response"""
        self.command_count += 1
        command = command.lower().strip()
        
        print(f"\n🎯 Processing command: {command}")
        
        # Check for time-related commands
        if self._match_pattern(command, 'time'):
            return self._handle_time_command()
        elif self._match_pattern(command, 'date'):
            return self._handle_date_command()
        elif self._match_pattern(command, 'datetime'):
            return self._handle_datetime_command()
        
        # Check for weather commands
        elif self._match_pattern(command, 'weather'):
            return self._handle_weather_command()
        
        # Check for application commands
        elif self._match_pattern(command, 'open_app'):
            return self._handle_open_app_command(command)
        
        # Check for web search commands
        elif self._match_pattern(command, 'web_search'):
            return self._handle_web_search_command(command)
        
        # Check for Wikipedia commands
        elif self._match_pattern(command, 'wikipedia'):
            return self._handle_wikipedia_command(command)
        
        # Check for system control commands
        elif self._match_pattern(command, 'screenshot'):
            return self._handle_screenshot_command()
        elif self._match_pattern(command, 'volume'):
            return self._handle_volume_command(command)
        elif self._match_pattern(command, 'shutdown'):
            return self._handle_shutdown_command()
        elif self._match_pattern(command, 'restart'):
            return self._handle_restart_command()
        elif self._match_pattern(command, 'lock'):
            return self._handle_lock_command()
        
        # Check for utility commands
        elif self._match_pattern(command, 'quote'):
            return self._handle_quote_command()
        elif self._match_pattern(command, 'fact'):
            return self._handle_fact_command()
        elif self._match_pattern(command, 'status'):
            return self._handle_status_command()
        
        # Check for YouTube search
        elif self._match_pattern(command, 'youtube'):
            return self._handle_youtube_command(command)
        
        # Check for news
        elif self._match_pattern(command, 'news'):
            return self._handle_news_command()
        
        # Check for help
        elif self._match_pattern(command, 'help'):
            return self._handle_help_command()
        
        # Check for exit
        elif self._match_pattern(command, 'exit'):
            return self._handle_exit_command()
        
        # Unknown command
        else:
            return self._handle_unknown_command(command)
    
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
                # Extract the parameter based on pattern type
                if pattern_type == 'open_app':
                    return match.group(1).strip()
                elif pattern_type == 'web_search':
                    return match.group(2).strip()
                elif pattern_type == 'wikipedia':
                    return match.group(2).strip()
                elif pattern_type == 'youtube':
                    return match.group(2).strip()
                elif pattern_type == 'volume':
                    if len(match.groups()) >= 2:
                        return match.group(2)
        return None
    
    def _handle_time_command(self) -> str:
        """Handle time-related commands"""
        result = self.utils.get_current_time()
        if result['success']:
            return result['message']
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_date_command(self) -> str:
        """Handle date-related commands"""
        result = self.utils.get_current_date()
        if result['success']:
            return result['message']
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_datetime_command(self) -> str:
        """Handle combined time and date commands"""
        result = self.utils.get_time_and_date()
        if result['success']:
            return result['message']
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_weather_command(self) -> str:
        """Handle weather-related commands"""
        # For demo, use mock weather
        weather_type = random.choice(['sunny', 'cloudy', 'rainy', 'snowy'])
        city = "your area"
        
        response = self.utils.get_weather_personality(weather_type, city)
        return response
    
    def _handle_open_app_command(self, command: str) -> str:
        """Handle application opening commands"""
        app_name = self._extract_parameter(command, 'open_app')
        if app_name:
            thinking = self.get_personality_response('thinking')
            print(f"💭 {thinking}")
            
            success = self.system.open_application(app_name)
            if success:
                return f"Opening {app_name} for you, {self.user_name}!"
            else:
                return f"Sorry, {self.user_name}, I couldn't find or open {app_name}. Maybe it's not installed?"
        else:
            return self.get_personality_response('clarification', user=self.user_name)
    
    def _handle_web_search_command(self, command: str) -> str:
        """Handle web search commands"""
        query = self._extract_parameter(command, 'web_search')
        if query:
            thinking = self.get_personality_response('thinking')
            print(f"💭 {thinking}")
            
            result = self.web.search_google(query, open_browser=True)
            if result['success']:
                return result['message']
            else:
                return self.get_personality_response('error', user=self.user_name)
        else:
            return self.get_personality_response('clarification', user=self.user_name)
    
    def _handle_wikipedia_command(self, command: str) -> str:
        """Handle Wikipedia commands"""
        query = self._extract_parameter(command, 'wikipedia')
        if query:
            thinking = self.get_personality_response('thinking')
            print(f"💭 {thinking}")
            
            result = self.web.search_wikipedia(query, sentences=3)
            if result['success']:
                if 'summary' in result:
                    return f"{result['message']} Here's what I found: {result['summary']}"
                elif 'suggestions' in result:
                    return f"{result['message']} Try one of these: {', '.join(result['suggestions'][:3])}"
                else:
                    return result['message']
            else:
                return result['message']
        else:
            return self.get_personality_response('clarification', user=self.user_name)
    
    def _handle_screenshot_command(self) -> str:
        """Handle screenshot commands"""
        thinking = self.get_personality_response('thinking')
        print(f"💭 {thinking}")
        
        result = self.system.take_screenshot()
        if result:
            return f"Screenshot captured and saved, {self.user_name}! Your digital moment is preserved."
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_volume_command(self, command: str) -> str:
        """Handle volume control commands"""
        # Extract volume level or direction
        if 'up' in command:
            success = self.system.adjust_volume(10)
            if success:
                return f"Volume increased, {self.user_name}! Let's make some noise!"
            else:
                return self.get_personality_response('error', user=self.user_name)
        elif 'down' in command:
            success = self.system.adjust_volume(-10)
            if success:
                return f"Volume decreased, {self.user_name}. Keeping it down to earth!"
            else:
                return self.get_personality_response('error', user=self.user_name)
        elif 'mute' in command:
            success = self.system.set_volume(0)
            if success:
                return f"Audio muted, {self.user_name}. Silence is golden!"
            else:
                return self.get_personality_response('error', user=self.user_name)
        else:
            # Try to extract specific volume level
            volume_match = re.search(r'(\d+)', command)
            if volume_match:
                volume = int(volume_match.group(1))
                success = self.system.set_volume(volume)
                if success:
                    return f"Volume set to {volume}%, {self.user_name}! Perfect level for productivity."
                else:
                    return self.get_personality_response('error', user=self.user_name)
            else:
                return self.get_personality_response('clarification', user=self.user_name)
    
    def _handle_shutdown_command(self) -> str:
        """Handle shutdown commands"""
        return f"Shutdown command received, {self.user_name}. Are you sure you want me to shut down your computer? This action cannot be undone."
    
    def _handle_restart_command(self) -> str:
        """Handle restart commands"""
        return f"Restart command received, {self.user_name}. Are you sure you want me to restart your computer? This will close all applications."
    
    def _handle_lock_command(self) -> str:
        """Handle lock commands"""
        thinking = self.get_personality_response('thinking')
        print(f"💭 {thinking}")
        
        success = self.system.lock_computer()
        if success:
            return f"Computer locked, {self.user_name}! Your digital fortress is secure."
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_quote_command(self) -> str:
        """Handle quote commands"""
        result = self.utils.get_random_quote()
        if result['success']:
            return result['message']
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_fact_command(self) -> str:
        """Handle fact commands"""
        result = self.utils.get_random_fact()
        if result['success']:
            return result['message']
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_status_command(self) -> str:
        """Handle status commands"""
        result = self.utils.get_system_status()
        if result['success']:
            return result['message']
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_youtube_command(self, command: str) -> str:
        """Handle YouTube search commands"""
        query = self._extract_parameter(command, 'youtube')
        if query:
            thinking = self.get_personality_response('thinking')
            print(f"💭 {thinking}")
            
            result = self.web.search_youtube(query, open_browser=True)
            if result['success']:
                return result['message']
            else:
                return self.get_personality_response('error', user=self.user_name)
        else:
            return self.get_personality_response('clarification', user=self.user_name)
    
    def _handle_news_command(self) -> str:
        """Handle news commands"""
        thinking = self.get_personality_response('thinking')
        print(f"💭 {thinking}")
        
        result = self.web.get_news_headlines("technology", count=3)
        if result['success']:
            response = f"{result['message']}\n"
            for i, headline in enumerate(result['headlines'], 1):
                response += f"{i}. {headline}\n"
            return response.strip()
        else:
            return self.get_personality_response('error', user=self.user_name)
    
    def _handle_help_command(self) -> str:
        """Handle help commands"""
        help_text = f"""
Here's what I can do for you, {self.user_name}:

🕐 **Time & Date**
• "What time is it?" - Get current time
• "What's the date?" - Get current date
• "What's the time and date?" - Get both

🌤️ **Weather & Information**
• "What's the weather like?" - Get weather info
• "Tell me about [topic]" - Wikipedia search
• "Search for [query]" - Web search
• "YouTube [query]" - Search YouTube

💻 **System Control**
• "Open [app name]" - Launch applications
• "Take a screenshot" - Capture screen
• "Volume up/down" - Control audio
• "Lock computer" - Secure your system

💡 **Entertainment**
• "Give me a quote" - Motivational quotes
• "Tell me a fact" - Interesting facts
• "What's in the news?" - Latest headlines
• "How are you?" - Check my status

Just say "Nova" followed by your command, and I'll handle the rest!
        """
        return help_text.strip()
    
    def _handle_exit_command(self) -> str:
        """Handle exit commands"""
        return f"Goodbye, {self.user_name}! It's been a pleasure serving you. Nova signing off!"
    
    def _handle_unknown_command(self, command: str) -> str:
        """Handle unknown commands"""
        return self.get_personality_response('unknown', user=self.user_name)
    
    def run(self):
        """Main run loop for Nova AI Assistant"""
        try:
            # Greet the user
            greeting = self.greet_user()
            print(f"\n🤖 {greeting}")
            self.voice.speak(greeting)
            
            print("\n" + "="*60)
            print("🎧 Nova is listening for your commands...")
            print("💡 Say 'Nova' followed by your command")
            print("❓ Say 'Nova, help' to see what I can do")
            print("🚪 Say 'Nova, exit' to close the assistant")
            print("="*60)
            
            # Start listening loop
            self.voice.start_listening_loop(self._process_voice_command)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Nova interrupted by user")
            self.shutdown()
        except Exception as e:
            print(f"\n❌ Error in Nova: {e}")
            self.shutdown()
    
    def _process_voice_command(self, command: str):
        """Process voice command and respond"""
        try:
            # Process the command
            response = self.process_command(command)
            
            # Speak the response
            print(f"\n🤖 Nova: {response}")
            self.voice.speak(response)
            
        except Exception as e:
            error_msg = f"Sorry, {self.user_name}, I encountered an error: {str(e)}"
            print(f"\n❌ {error_msg}")
            self.voice.speak(error_msg)
    
    def shutdown(self):
        """Shutdown Nova AI Assistant"""
        print("\n🔄 Shutting down Nova AI Assistant...")
        
        # Stop voice interface
        if hasattr(self, 'voice'):
            self.voice.stop_listening()
        
        # Calculate session stats
        session_duration = time.time() - self.session_start
        minutes = int(session_duration // 60)
        seconds = int(session_duration % 60)
        
        print(f"📊 Session Summary:")
        print(f"   Commands processed: {self.command_count}")
        print(f"   Session duration: {minutes}m {seconds}s")
        print(f"   Thank you for using Nova AI Assistant!")
        
        print("\n👋 Goodbye!")


def main():
    """Main entry point for Nova AI Assistant"""
    print("🌟 Welcome to Nova AI Assistant!")
    print("🚀 Initializing systems...")
    
    try:
        # Create and run Nova
        nova = NovaAI()
        nova.run()
        
    except Exception as e:
        print(f"❌ Failed to initialize Nova AI Assistant: {e}")
        print("🔧 Please check your installation and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
