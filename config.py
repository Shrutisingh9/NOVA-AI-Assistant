"""
Configuration file for Nova AI Assistant
Customize Nova's behavior and settings here
"""

# Voice Interface Settings
VOICE_SETTINGS = {
    'wake_word': 'nova',  # Word to activate Nova
    'speech_rate': 180,   # Words per minute
    'volume': 0.9,        # Volume level (0.0 to 1.0)
    'timeout': 5,         # Seconds to wait for speech to start
    'phrase_time_limit': 10,  # Maximum seconds for a single phrase
}

# Personality Settings
PERSONALITY_SETTINGS = {
    'user_name': 'Sir',   # Default name for user
    'greeting_style': 'friendly_witty',
    'response_style': 'professional_playful',
    'humor_level': 'moderate',
    'formality': 'casual_professional'
}

# System Control Settings
SYSTEM_SETTINGS = {
    'screenshot_path': 'screenshots',  # Default screenshot directory
    'allowed_apps': [  # Apps that Nova can open
        'chrome', 'firefox', 'edge', 'notepad', 'wordpad',
        'calculator', 'paint', 'spotify', 'discord', 'steam',
        'vscode', 'word', 'excel', 'powerpoint', 'outlook',
        'teams', 'zoom', 'skype'
    ],
    'volume_step': 10,  # Volume change increment
}

# Web Tools Settings
WEB_SETTINGS = {
    'wikipedia_sentences': 3,  # Default number of sentences for Wikipedia summaries
    'search_results_limit': 5,  # Number of search results to return
    'news_categories': ['general', 'technology', 'science'],  # Available news categories
}

# Weather Settings (for future API integration)
WEATHER_SETTINGS = {
    'default_city': 'your area',
    'api_key': None,  # OpenWeatherMap API key
    'units': 'metric',  # metric or imperial
}

# Logging Settings
LOGGING_SETTINGS = {
    'enabled': True,
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'file': 'nova.log',
    'max_size': 1024 * 1024,  # 1MB
    'backup_count': 3
}

# Development Settings
DEV_SETTINGS = {
    'debug_mode': False,
    'test_mode': False,
    'mock_weather': True,  # Use mock weather data for demo
    'mock_news': True,     # Use mock news data for demo
}

# Custom Responses (add your own personality touches)
CUSTOM_RESPONSES = {
    'greetings': [
        "Greetings, {user}! Nova at your service, ready to make your day more efficient and slightly more entertaining.",
        "Hello there, {user}! Nova here, your AI companion for all things digital and delightful.",
        "Good day, {user}! Nova is online and ready to assist with your every whim and command.",
    ],
    'thinking': [
        "Processing your request with the speed of thought...",
        "Let me consult my digital brain...",
        "Analyzing the situation...",
        "Computing the best approach...",
        "Working my AI magic...",
    ],
    'success': [
        "Mission accomplished, {user}!",
        "Task completed successfully!",
        "Done and done, {user}!",
        "Successfully executed, {user}!",
        "All systems green, {user}!",
    ]
}

# Feature Flags (enable/disable specific features)
FEATURE_FLAGS = {
    'voice_interface': True,
    'system_controls': True,
    'web_tools': True,
    'utilities': True,
    'screenshots': True,
    'volume_control': True,
    'app_launcher': True,
    'weather_info': True,
    'news_headlines': True,
    'wikipedia_search': True,
    'web_search': True,
    'youtube_search': True,
}

# API Keys (add your own API keys here)
API_KEYS = {
    'openweathermap': None,  # Get from https://openweathermap.org/api
    'newsapi': None,         # Get from https://newsapi.org/
    'youtube': None,         # Get from Google Cloud Console
    'google_translate': None, # Get from Google Cloud Console
}

# Paths and Directories
PATHS = {
    'screenshots': 'screenshots',
    'logs': 'logs',
    'config': 'config',
    'temp': 'temp',
}

# Time and Date Formats
TIME_FORMATS = {
    '12hour': '%I:%M %p',
    '24hour': '%H:%M',
    'full': '%I:%M:%S %p',
    'date': '%A, %B %d, %Y',
    'datetime': '%A, %B %d, %Y at %I:%M %p'
}

# Command Aliases (customize command shortcuts)
COMMAND_ALIASES = {
    'time': ['clock', 'hour', 'what time'],
    'date': ['day', 'today', 'what date'],
    'weather': ['temperature', 'forecast', 'climate'],
    'open': ['launch', 'start', 'run'],
    'search': ['find', 'look up', 'google'],
    'screenshot': ['screen shot', 'capture', 'snapshot'],
    'volume': ['sound', 'audio', 'loudness'],
    'help': ['assist', 'support', 'commands', 'what can you do'],
    'exit': ['quit', 'stop', 'goodbye', 'bye', 'close'],
}
