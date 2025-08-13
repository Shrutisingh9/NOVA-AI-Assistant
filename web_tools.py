"""
Web Tools Module for Nova AI Assistant
Handles web search, Wikipedia queries, and other web-based operations
"""

import requests
import wikipedia
import pywhatkit
import webbrowser
from typing import Optional, List, Dict
import json
import re
from urllib.parse import quote_plus


class WebTools:
    """Handles web-based operations for Nova AI Assistant"""
    
    def __init__(self):
        """Initialize web tools"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Configure Wikipedia
        wikipedia.set_lang('en')
        wikipedia.set_rate_limiting(True)
    
    def search_google(self, query: str, open_browser: bool = False) -> Dict:
        """
        Perform a Google search
        
        Args:
            query: Search query
            open_browser: Whether to open results in browser
            
        Returns:
            Dictionary with search results and status
        """
        try:
            if open_browser:
                # Open Google search in default browser
                search_url = f"https://www.google.com/search?q={quote_plus(query)}"
                webbrowser.open(search_url)
                
                return {
                    'success': True,
                    'message': f"Opened Google search for '{query}' in your browser",
                    'url': search_url,
                    'results': []
                }
            else:
                # Use pywhatkit for search (limited results)
                try:
                    # This will open a browser tab with search results
                    pywhatkit.search(query)
                    
                    return {
                        'success': True,
                        'message': f"Performed Google search for '{query}'",
                        'query': query,
                        'results': []
                    }
                except Exception as e:
                    # Fallback to simple URL opening
                    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
                    webbrowser.open(search_url)
                    
                    return {
                        'success': True,
                        'message': f"Opened Google search for '{query}' in your browser",
                        'url': search_url,
                        'results': []
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to perform Google search for '{query}'"
            }
    
    def search_wikipedia(self, query: str, sentences: int = 3) -> Dict:
        """
        Search Wikipedia for information
        
        Args:
            query: Search query
            sentences: Number of sentences to return in summary
            
        Returns:
            Dictionary with Wikipedia results
        """
        try:
            # First try to get a direct page match
            try:
                page = wikipedia.page(query, auto_suggest=False)
                summary = wikipedia.summary(query, sentences=sentences)
                
                return {
                    'success': True,
                    'title': page.title,
                    'summary': summary,
                    'url': page.url,
                    'message': f"Found Wikipedia article: {page.title}"
                }
                
            except wikipedia.DisambiguationError as e:
                # Handle disambiguation pages
                options = e.options[:5]  # Limit to first 5 options
                
                return {
                    'success': True,
                    'type': 'disambiguation',
                    'query': query,
                    'options': options,
                    'message': f"Multiple Wikipedia articles found for '{query}'. Please be more specific.",
                    'suggestions': options
                }
                
            except wikipedia.PageError:
                # Page not found, try searching
                search_results = wikipedia.search(query, results=5)
                
                if search_results:
                    return {
                        'success': True,
                        'type': 'search_results',
                        'query': query,
                        'results': search_results,
                        'message': f"No exact match found for '{query}', but here are some related articles:",
                        'suggestions': search_results
                    }
                else:
                    return {
                        'success': False,
                        'message': f"No Wikipedia articles found for '{query}'"
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to search Wikipedia for '{query}'"
            }
    
    def get_wikipedia_summary(self, title: str, sentences: int = 3) -> Dict:
        """
        Get a specific Wikipedia article summary
        
        Args:
            title: Exact Wikipedia article title
            sentences: Number of sentences to return
            
        Returns:
            Dictionary with article summary
        """
        try:
            summary = wikipedia.summary(title, sentences=sentences)
            page = wikipedia.page(title)
            
            return {
                'success': True,
                'title': title,
                'summary': summary,
                'url': page.url,
                'message': f"Here's what I found about {title}"
            }
            
        except wikipedia.PageError:
            return {
                'success': False,
                'message': f"Wikipedia article '{title}' not found"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get Wikipedia summary for '{title}'"
            }
    
    def open_url(self, url: str) -> Dict:
        """
        Open a URL in the default browser
        
        Args:
            url: URL to open
            
        Returns:
            Dictionary with operation status
        """
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            
            return {
                'success': True,
                'message': f"Opened {url} in your browser",
                'url': url
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to open {url}"
            }
    
    def get_weather_info(self, city: str, api_key: Optional[str] = None) -> Dict:
        """
        Get weather information for a city
        
        Args:
            city: City name
            api_key: OpenWeatherMap API key (optional)
            
        Returns:
            Dictionary with weather information
        """
        try:
            # For demo purposes, we'll use a simple approach
            # In production, you'd want to use a real weather API
            
            if not api_key:
                # Return mock weather data for demo
                return {
                    'success': True,
                    'city': city,
                    'temperature': '22°C',
                    'description': 'Partly cloudy',
                    'humidity': '65%',
                    'wind_speed': '12 km/h',
                    'message': f"Weather in {city}: 22°C, partly cloudy with 65% humidity",
                    'note': 'This is demo data. For real weather, provide an OpenWeatherMap API key.'
                }
            
            # Real API implementation would go here
            # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            # response = self.session.get(url)
            # data = response.json()
            
            return {
                'success': True,
                'city': city,
                'message': f"Weather API key provided for {city}. Implement real API call here."
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get weather for {city}"
            }
    
    def search_youtube(self, query: str, open_browser: bool = True) -> Dict:
        """
        Search YouTube for videos
        
        Args:
            query: Search query
            open_browser: Whether to open results in browser
            
        Returns:
            Dictionary with search results
        """
        try:
            if open_browser:
                search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
                webbrowser.open(search_url)
                
                return {
                    'success': True,
                    'message': f"Opened YouTube search for '{query}' in your browser",
                    'url': search_url
                }
            else:
                # Could implement YouTube API here for actual results
                return {
                    'success': True,
                    'message': f"YouTube search for '{query}' ready",
                    'query': query
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to search YouTube for '{query}'"
            }
    
    def get_news_headlines(self, category: str = "general", count: int = 5) -> Dict:
        """
        Get news headlines (mock implementation)
        
        Args:
            category: News category
            count: Number of headlines to return
            
        Returns:
            Dictionary with news headlines
        """
        try:
            # Mock news data for demo
            mock_news = {
                "general": [
                    "AI Breakthrough: New Language Model Shows Remarkable Capabilities",
                    "Space Exploration: Mars Mission Discovers Ancient Water Evidence",
                    "Technology: Quantum Computing Milestone Achieved",
                    "Science: Breakthrough in Renewable Energy Storage",
                    "Health: New Medical Treatment Shows Promising Results"
                ],
                "technology": [
                    "Python 3.12 Released with Performance Improvements",
                    "Machine Learning: New Framework Simplifies AI Development",
                    "Cybersecurity: Major Vulnerability Discovered and Patched",
                    "Cloud Computing: New Services Announced",
                    "Mobile: Latest Smartphone Features Revealed"
                ],
                "science": [
                    "Climate Change: New Research Shows Accelerating Trends",
                    "Biology: New Species Discovered in Amazon Rainforest",
                    "Physics: Quantum Entanglement Experiment Succeeds",
                    "Chemistry: Breakthrough in Carbon Capture Technology",
                    "Astronomy: New Exoplanet Discovered in Habitable Zone"
                ]
            }
            
            headlines = mock_news.get(category, mock_news["general"])[:count]
            
            return {
                'success': True,
                'category': category,
                'headlines': headlines,
                'count': len(headlines),
                'message': f"Here are the latest {category} news headlines:",
                'note': 'This is demo data. For real news, integrate with a news API.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get {category} news headlines"
            }
    
    def translate_text(self, text: str, target_language: str = "en") -> Dict:
        """
        Translate text (mock implementation)
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            Dictionary with translation
        """
        try:
            # Mock translation for demo
            # In production, you'd use Google Translate API or similar
            
            mock_translations = {
                "hello": "hola",
                "goodbye": "adiós",
                "thank you": "gracias",
                "how are you": "cómo estás",
                "good morning": "buenos días"
            }
            
            if text.lower() in mock_translations:
                translation = mock_translations[text.lower()]
                return {
                    'success': True,
                    'original': text,
                    'translated': translation,
                    'target_language': target_language,
                    'message': f"'{text}' translates to '{translation}' in {target_language}",
                    'note': 'This is demo data. For real translation, integrate with Google Translate API.'
                }
            else:
                return {
                    'success': True,
                    'original': text,
                    'translated': f"[{text}] (translated to {target_language})",
                    'target_language': target_language,
                    'message': f"Translation of '{text}' to {target_language}",
                    'note': 'This is demo data. For real translation, integrate with Google Translate API.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to translate text to {target_language}"
            }
    
    def get_definition(self, word: str) -> Dict:
        """
        Get word definition (mock implementation)
        
        Args:
            word: Word to define
            
        Returns:
            Dictionary with word definition
        """
        try:
            # Mock definitions for demo
            # In production, you'd use a dictionary API
            
            mock_definitions = {
                "artificial intelligence": "The simulation of human intelligence in machines that are programmed to think and learn like humans.",
                "machine learning": "A subset of artificial intelligence that enables systems to automatically learn and improve from experience.",
                "python": "A high-level, interpreted programming language known for its simplicity and readability.",
                "algorithm": "A set of rules or instructions designed to solve a specific problem or perform a particular task.",
                "database": "An organized collection of structured information or data, typically stored electronically in a computer system."
            }
            
            if word.lower() in mock_definitions:
                definition = mock_definitions[word.lower()]
                return {
                    'success': True,
                    'word': word,
                    'definition': definition,
                    'message': f"Definition of '{word}': {definition}",
                    'note': 'This is demo data. For real definitions, integrate with a dictionary API.'
                }
            else:
                return {
                    'success': True,
                    'word': word,
                    'definition': f"A term or concept that requires definition.",
                    'message': f"'{word}' is a term that can be defined.",
                    'note': 'This is demo data. For real definitions, integrate with a dictionary API.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get definition for '{word}'"
            }


if __name__ == "__main__":
    # Test the web tools
    tools = WebTools()
    
    print("🎯 Testing Nova's Web Tools")
    print("=" * 40)
    
    # Test Wikipedia search
    print("\n📚 Testing Wikipedia search...")
    result = tools.search_wikipedia("artificial intelligence", sentences=2)
    if result['success']:
        print(f"✅ {result['message']}")
        if 'summary' in result:
            print(f"📖 Summary: {result['summary']}")
    else:
        print(f"❌ {result['message']}")
    
    # Test Google search
    print("\n🔍 Testing Google search...")
    result = tools.search_google("Python programming", open_browser=False)
    print(f"✅ {result['message']}")
    
    # Test weather (demo)
    print("\n🌤️ Testing weather info...")
    result = tools.get_weather_info("London")
    if result['success']:
        print(f"✅ {result['message']}")
    
    # Test news
    print("\n📰 Testing news headlines...")
    result = tools.get_news_headlines("technology", count=3)
    if result['success']:
        print(f"✅ {result['message']}")
        for i, headline in enumerate(result['headlines'], 1):
            print(f"  {i}. {headline}")
    
    print("\n✅ Web tools test completed!")
