"""
Nova AI Assistant - GUI Version
With visual animations and enhanced user interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import random
import webbrowser
from datetime import datetime

# Import Nova's modules
from voice_interface import VoiceInterface
from system_controls import SystemControls
from web_tools import WebTools
from utilities import Utilities


class NovaGUI:
    """GUI version of Nova AI Assistant with visual animations"""
    
    def __init__(self, root):
        """Initialize Nova GUI"""
        self.root = root
        self.root.title("Nova AI Assistant - Enhanced GUI")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize Nova modules
        self.voice = VoiceInterface()
        self.system = SystemControls()
        self.web = WebTools()
        self.utils = Utilities()
        
        # GUI state
        self.is_listening = False
        self.is_speaking = False
        self.conversation_history = []
        
        # Setup GUI
        self.setup_gui()
        self.setup_animations()
        
        # Start Nova
        self.start_nova()
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🌟 Nova AI Assistant", 
            font=("Arial", 24, "bold"),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#1a1a1a')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Status label
        self.status_label = tk.Label(
            status_frame,
            text="🟢 Nova is ready!",
            font=("Arial", 12),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Animation canvas
        self.animation_canvas = tk.Canvas(
            status_frame,
            width=100,
            height=30,
            bg='#1a1a1a',
            highlightthickness=0
        )
        self.animation_canvas.pack(side=tk.RIGHT)
        
        # Conversation area
        conv_frame = tk.Frame(main_frame, bg='#1a1a1a')
        conv_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Conversation label
        conv_label = tk.Label(
            conv_frame,
            text="💬 Conversation",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        conv_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Conversation text area
        self.conversation_text = scrolledtext.ScrolledText(
            conv_frame,
            height=15,
            bg='#2a2a2a',
            fg='#ffffff',
            font=("Consolas", 10),
            insertbackground='#00ff88'
        )
        self.conversation_text.pack(fill=tk.BOTH, expand=True)
        
        # Control frame
        control_frame = tk.Frame(main_frame, bg='#1a1a1a')
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Voice control button
        self.voice_button = tk.Button(
            control_frame,
            text="🎤 Start Listening",
            command=self.toggle_voice,
            bg='#00ff88',
            fg='#000000',
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.voice_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Test commands frame
        test_frame = tk.Frame(main_frame, bg='#1a1a1a')
        test_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Test commands label
        test_label = tk.Label(
            test_frame,
            text="🧪 Test Commands",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        test_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Test buttons frame
        buttons_frame = tk.Frame(test_frame, bg='#1a1a1a')
        buttons_frame.pack(fill=tk.X)
        
        # Test buttons
        test_commands = [
            ("🌐 Open Google", lambda: self.test_command("open google")),
            ("⏰ What Time", lambda: self.test_command("what time is it")),
            ("🌤️ Weather", lambda: self.test_command("what's the weather like")),
            ("💭 Quote", lambda: self.test_command("give me a quote")),
            ("📸 Screenshot", lambda: self.test_command("take a screenshot")),
            ("🔍 Search Python", lambda: self.test_command("search for Python tutorials"))
        ]
        
        for i, (text, command) in enumerate(test_commands):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                bg='#333333',
                fg='#ffffff',
                font=("Arial", 10),
                relief=tk.FLAT,
                padx=15,
                pady=5
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)
        
        # Quick actions frame
        actions_frame = tk.Frame(main_frame, bg='#1a1a1a')
        actions_frame.pack(fill=tk.X)
        
        # Quick actions label
        actions_label = tk.Label(
            actions_frame,
            text="⚡ Quick Actions",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        actions_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Quick action buttons
        quick_actions = [
            ("🚀 YouTube", lambda: self.open_website("youtube")),
            ("💻 GitHub", lambda: self.open_website("github")),
            ("📰 News", lambda: self.open_website("news")),
            ("🗺️ Maps", lambda: self.open_website("maps"))
        ]
        
        for i, (text, command) in enumerate(quick_actions):
            btn = tk.Button(
                actions_frame,
                text=text,
                command=command,
                bg='#444444',
                fg='#ffffff',
                font=("Arial", 10),
                relief=tk.FLAT,
                padx=15,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=(0, 10))
    
    def setup_animations(self):
        """Setup animation variables"""
        self.animation_frames = 0
        self.animation_running = False
    
    def start_nova(self):
        """Start Nova AI Assistant"""
        self.add_to_conversation("Nova", "Hello! I'm Nova, your AI assistant. I'm ready to help you with anything you need! 🚀")
        self.update_status("🟢 Nova is ready!", "#00ff88")
    
    def toggle_voice(self):
        """Toggle voice listening mode"""
        if not self.is_listening:
            self.start_voice_listening()
        else:
            self.stop_voice_listening()
    
    def start_voice_listening(self):
        """Start voice listening"""
        self.is_listening = True
        self.voice_button.config(text="🔇 Stop Listening", bg='#ff4444')
        self.update_status("🎤 Listening for commands...", "#ffaa00")
        self.start_listening_animation()
        
        # Start voice listening in separate thread
        threading.Thread(target=self.voice_listening_loop, daemon=True).start()
    
    def stop_voice_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.voice_button.config(text="🎤 Start Listening", bg='#00ff88')
        self.update_status("🟢 Nova is ready!", "#00ff88")
        self.stop_listening_animation()
    
    def voice_listening_loop(self):
        """Voice listening loop"""
        try:
            while self.is_listening:
                # Listen for wake word
                command = self.voice.listen(timeout=3, phrase_time_limit=5)
                if command and "nova" in command.lower():
                    self.root.after(0, lambda: self.update_status("🎯 Processing command...", "#00aaff"))
                    
                    # Listen for actual command
                    actual_command = self.voice.listen(timeout=5, phrase_time_limit=15)
                    if actual_command:
                        # Remove wake word and process
                        clean_command = actual_command.replace("nova", "").strip()
                        if clean_command:
                            self.root.after(0, lambda: self.process_voice_command(clean_command))
                    
                    self.root.after(0, lambda: self.update_status("🎤 Listening for commands...", "#ffaa00"))
        except Exception as e:
            self.root.after(0, lambda: self.add_to_conversation("System", f"Voice listening error: {str(e)}"))
            self.root.after(0, lambda: self.stop_voice_listening())
    
    def process_voice_command(self, command: str):
        """Process voice command"""
        self.add_to_conversation("You", command)
        self.update_status("⚡ Processing command...", "#00aaff")
        
        # Process command and get response
        response = self.process_command(command)
        
        # Add response to conversation
        self.add_to_conversation("Nova", response)
        
        # Speak response
        self.speak_response(response)
        
        # Update status
        self.update_status("🎤 Listening for commands...", "#ffaa00")
    
    def process_command(self, command: str) -> str:
        """Process text command and return response"""
        command = command.lower().strip()
        
        # Website opening
        if any(word in command for word in ['open', 'go to', 'visit']):
            for word in ['open', 'go to', 'visit']:
                if word in command:
                    site = command.replace(word, '').strip()
                    return self.open_website(site)
        
        # Web search
        elif any(word in command for word in ['search', 'find', 'look up']):
            for word in ['search', 'find', 'look up']:
                if word in command:
                    query = command.replace(word, '').strip()
                    if 'for' in query:
                        query = query.replace('for', '').strip()
                    return self.search_web(query)
        
        # Time
        elif any(word in command for word in ['time', 'clock']):
            result = self.utils.get_current_time()
            if result['success']:
                return result['message']
        
        # Date
        elif any(word in command for word in ['date', 'day']):
            result = self.utils.get_current_date()
            if result['success']:
                return result['message']
        
        # Weather
        elif any(word in command for word in ['weather', 'temperature']):
            weather_type = random.choice(['sunny', 'cloudy', 'rainy', 'snowy'])
            return self.utils.get_weather_personality(weather_type, "your area")
        
        # Screenshot
        elif any(word in command for word in ['screenshot', 'screen shot']):
            result = self.system.take_screenshot()
            if result:
                return f"Screenshot captured and saved! 📸"
            else:
                return "Sorry, the screenshot failed."
        
        # Quote
        elif any(word in command for word in ['quote', 'inspiration']):
            result = self.utils.get_random_quote()
            if result['success']:
                return result['message']
        
        # Fact
        elif any(word in command for word in ['fact', 'interesting']):
            result = self.utils.get_random_fact()
            if result['success']:
                return result['message']
        
        # Help
        elif 'help' in command:
            return "I can help you with: opening websites, searching the web, getting time/date, weather, screenshots, quotes, and facts! Just ask!"
        
        # Greeting
        elif any(word in command for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I assist you today? 😊"
        
        # Unknown command
        else:
            return f"I'm not sure how to handle '{command}'. Try saying 'help' to see what I can do!"
    
    def open_website(self, site_name: str) -> str:
        """Open a website"""
        try:
            site_name = site_name.lower().strip()
            
            # Known sites
            known_sites = {
                'google': 'https://www.google.com',
                'youtube': 'https://www.youtube.com',
                'github': 'https://github.com',
                'stackoverflow': 'https://stackoverflow.com',
                'reddit': 'https://reddit.com',
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
            
            if site_name in known_sites:
                url = known_sites[site_name]
                webbrowser.open(url)
                return f"Opening {site_name} in your browser! 🚀"
            else:
                # Try to construct URL
                url = f"https://www.{site_name}.com"
                webbrowser.open(url)
                return f"Opening {site_name} in your browser! 🌐"
                
        except Exception as e:
            return f"Sorry, I couldn't open {site_name}. Error: {str(e)}"
    
    def search_web(self, query: str) -> str:
        """Perform web search"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching the web for '{query}'! 🔍"
        except Exception as e:
            return f"Sorry, the web search failed. Error: {str(e)}"
    
    def speak_response(self, response: str):
        """Speak the response"""
        try:
            self.is_speaking = True
            self.update_status("🗣️ Speaking...", "#ff00ff")
            self.start_speaking_animation()
            
            # Speak in separate thread
            threading.Thread(target=self._speak_thread, args=(response,), daemon=True).start()
        except Exception as e:
            self.add_to_conversation("System", f"Speech error: {str(e)}")
            self.is_speaking = False
            self.update_status("🟢 Nova is ready!", "#00ff88")
    
    def _speak_thread(self, response: str):
        """Speech thread"""
        try:
            self.voice.speak(response)
            self.root.after(0, lambda: self.stop_speaking_animation())
            self.root.after(0, lambda: self.update_status("🟢 Nova is ready!", "#00ff88"))
        except Exception as e:
            self.root.after(0, lambda: self.add_to_conversation("System", f"Speech error: {str(e)}"))
        finally:
            self.is_speaking = False
    
    def test_command(self, command: str):
        """Test a command"""
        self.add_to_conversation("You", f"[Test] {command}")
        response = self.process_command(command)
        self.add_to_conversation("Nova", response)
        self.speak_response(response)
    
    def add_to_conversation(self, speaker: str, message: str):
        """Add message to conversation"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {speaker}: {message}\n"
        
        self.conversation_text.insert(tk.END, formatted_message)
        self.conversation_text.see(tk.END)
        
        # Add to history
        self.conversation_history.append(f"[{timestamp}] {speaker}: {message}")
    
    def update_status(self, message: str, color: str):
        """Update status message"""
        self.status_label.config(text=message, fg=color)
    
    def start_listening_animation(self):
        """Start listening animation"""
        self.animation_running = True
        self.animate_listening()
    
    def stop_listening_animation(self):
        """Stop listening animation"""
        self.animation_running = False
        self.animation_canvas.delete("all")
    
    def animate_listening(self):
        """Animate listening indicator"""
        if not self.animation_running:
            return
        
        self.animation_canvas.delete("all")
        
        # Create pulsing circles
        for i in range(3):
            x = 20 + i * 25
            y = 15
            radius = 5 + 3 * abs((self.animation_frames + i * 10) % 20 - 10)
            color = f"#{int(255 * (1 - radius/15)):02x}ff00"
            
            self.animation_canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill=color, outline=""
            )
        
        self.animation_frames += 1
        self.root.after(100, self.animate_listening)
    
    def start_speaking_animation(self):
        """Start speaking animation"""
        self.animate_speaking()
    
    def stop_speaking_animation(self):
        """Stop speaking animation"""
        self.animation_canvas.delete("all")
    
    def animate_speaking(self):
        """Animate speaking indicator"""
        if not self.is_speaking:
            return
        
        self.animation_canvas.delete("all")
        
        # Create wave animation
        for i in range(5):
            x = 20 + i * 15
            y = 15
            height = 10 + 5 * abs((self.animation_frames + i * 5) % 20 - 10)
            color = f"#ff00{int(255 * (1 - height/20)):02x}"
            
            self.animation_canvas.create_rectangle(
                x - 2, y - height//2,
                x + 2, y + height//2,
                fill=color, outline=""
            )
        
        self.animation_frames += 1
        if self.is_speaking:
            self.root.after(100, self.animate_speaking)


def main():
    """Main entry point for Nova GUI"""
    root = tk.Tk()
    app = NovaGUI(root)
    
    # Handle window close
    def on_closing():
        if app.is_listening:
            app.stop_voice_listening()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
