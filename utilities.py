"""
Utilities Module for Nova AI Assistant
Handles weather, time/date, and other utility functions
"""

import datetime
import time
import random
from typing import Dict, List, Optional
import requests
import json


class Utilities:
    """Handles utility functions for Nova AI Assistant"""
    
    def __init__(self):
        """Initialize utilities"""
        self.time_formats = {
            '12hour': '%I:%M %p',
            '24hour': '%H:%M',
            'full': '%I:%M:%S %p',
            'date': '%A, %B %d, %Y',
            'datetime': '%A, %B %d, %Y at %I:%M %p'
        }
        
        # Personality responses for different times
        self.time_responses = {
            'morning': [
                "Good morning! It's {time} and a brand new day awaits.",
                "Rise and shine! The clock shows {time} and the world is your oyster.",
                "Morning has broken at {time}. Time to conquer the day!",
                "Good morning! It's {time} - perfect time for coffee and coding.",
                "The sun is up and it's {time}. Ready to make today amazing?"
            ],
            'afternoon': [
                "Good afternoon! It's {time} and you're crushing it.",
                "Afternoon vibes at {time}. How's your day going?",
                "It's {time} in the afternoon. Time for a productivity boost!",
                "Good afternoon! {time} and you're still going strong.",
                "Afternoon check-in at {time}. Need a break or ready to tackle more?"
            ],
            'evening': [
                "Good evening! It's {time} and you've made it through another day.",
                "Evening time at {time}. Time to wind down and reflect.",
                "Good evening! {time} - perfect time to review today's achievements.",
                "It's {time} in the evening. How did your day go?",
                "Evening check at {time}. Ready to plan tomorrow's adventures?"
            ],
            'night': [
                "Good night! It's {time} - time to rest and recharge.",
                "Late night at {time}. Still burning the midnight oil?",
                "It's {time} at night. Don't forget to get some sleep!",
                "Night time at {time}. Sweet dreams await!",
                "Late night check at {time}. Remember, even superheroes need rest!"
            ]
        }
        
        # Weather personality responses
        self.weather_responses = {
            'sunny': [
                "The sun is shining bright! Perfect weather for taking over the world... or at least finishing your project.",
                "Clear skies and sunshine! Mother Nature is definitely showing off today.",
                "Beautiful sunny day! Time to soak up some vitamin D and productivity.",
                "The sun is out and so should you be! Great weather for getting things done."
            ],
            'cloudy': [
                "Cloudy with a chance of productivity! The weather is keeping things interesting.",
                "Partly cloudy skies - just like my thoughts sometimes. Still a good day for work!",
                "Cloudy weather, but that's no excuse for cloudy thinking. Let's stay sharp!",
                "Overcast skies, but your future is bright! Time to shine through the clouds."
            ],
            'rainy': [
                "Rain, rain, go away! But since it's here, let's make it a cozy indoor productivity day.",
                "The weather is having a moment, but that's perfect for staying inside and getting things done.",
                "Rainy day vibes! Perfect weather for coding, reading, or whatever makes you happy.",
                "The sky is crying, but don't let it dampen your spirits! Indoor activities await."
            ],
            'snowy': [
                "Winter wonderland outside! Time to cozy up and tackle your to-do list.",
                "Snow is falling, and so are your excuses for not being productive!",
                "White Christmas vibes in {month}! Perfect weather for hot cocoa and productivity.",
                "The world is covered in snow, but your goals are crystal clear. Let's get to work!"
            ]
        }
    
    def get_current_time(self, format_type: str = '12hour') -> Dict:
        """
        Get current time with personality
        
        Args:
            format_type: Time format to use
            
        Returns:
            Dictionary with time information and personality response
        """
        try:
            now = datetime.datetime.now()
            
            # Get time string
            time_str = now.strftime(self.time_formats.get(format_type, self.time_formats['12hour']))
            
            # Determine time of day
            hour = now.hour
            if 5 <= hour < 12:
                time_of_day = 'morning'
            elif 12 <= hour < 17:
                time_of_day = 'afternoon'
            elif 17 <= hour < 21:
                time_of_day = 'evening'
            else:
                time_of_day = 'night'
            
            # Get personality response
            responses = self.time_responses.get(time_of_day, [])
            response = random.choice(responses).format(time=time_str)
            
            return {
                'success': True,
                'time': time_str,
                'time_of_day': time_of_day,
                'hour': hour,
                'minute': now.minute,
                'response': response,
                'message': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "Sorry, I seem to have lost track of time. Literally."
            }
    
    def get_current_date(self, format_type: str = 'date') -> Dict:
        """
        Get current date with personality
        
        Args:
            format_type: Date format to use
            
        Returns:
            Dictionary with date information and personality response
        """
        try:
            now = datetime.datetime.now()
            
            # Get date string
            date_str = now.strftime(self.time_formats.get(format_type, self.time_formats['date']))
            
            # Get day of week
            day_of_week = now.strftime('%A')
            
            # Personality responses for different days
            day_responses = {
                'Monday': f"It's Monday, {date_str}. The start of a new week - let's make it count!",
                'Tuesday': f"Tuesday, {date_str}. We're getting into the groove of the week!",
                'Wednesday': f"Wednesday, {date_str}. Hump day! We're over the hump and cruising!",
                'Thursday': f"Thursday, {date_str}. Almost there! The weekend is in sight!",
                'Friday': f"Friday, {date_str}. TGIF! Time to finish strong and enjoy the weekend!",
                'Saturday': f"Saturday, {date_str}. Weekend vibes! Time to relax and recharge!",
                'Sunday': f"Sunday, {date_str}. Day of rest and preparation for the week ahead!"
            }
            
            response = day_responses.get(day_of_week, f"It's {date_str}. Another day, another opportunity!")
            
            return {
                'success': True,
                'date': date_str,
                'day_of_week': day_of_week,
                'day': now.day,
                'month': now.month,
                'year': now.year,
                'response': response,
                'message': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "Sorry, my calendar seems to be malfunctioning. Time to reboot!"
            }
    
    def get_time_and_date(self, format_type: str = 'datetime') -> Dict:
        """
        Get current time and date combined
        
        Args:
            format_type: Format type to use
            
        Returns:
            Dictionary with combined time/date information
        """
        try:
            now = datetime.datetime.now()
            
            # Get combined string
            combined_str = now.strftime(self.time_formats.get(format_type, self.time_formats['datetime']))
            
            # Create personality response
            responses = [
                f"It's {combined_str}. Time to check what's on your agenda!",
                f"Current time and date: {combined_str}. The future is now!",
                f"Right now it's {combined_str}. Perfect timing for whatever you have planned!",
                f"The clock shows {combined_str}. Time waits for no one, so let's make the most of it!"
            ]
            
            response = random.choice(responses)
            
            return {
                'success': True,
                'datetime': combined_str,
                'time': now.strftime(self.time_formats['12hour']),
                'date': now.strftime(self.time_formats['date']),
                'response': response,
                'message': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "My internal clock seems to be having issues. Time for a system check!"
            }
    
    def get_weather_personality(self, weather_type: str, city: str = "your area") -> str:
        """
        Get personality-driven weather response
        
        Args:
            weather_type: Type of weather
            city: City name
            
        Returns:
            Personality-driven weather response
        """
        try:
            # Get current month for seasonal context
            month = datetime.datetime.now().strftime('%B')
            
            # Get weather response
            responses = self.weather_responses.get(weather_type.lower(), [
                f"The weather in {city} is {weather_type}. Mother Nature is keeping us on our toes!"
            ])
            
            response = random.choice(responses)
            
            # Add seasonal context
            if month in ['December', 'January', 'February']:
                response += " Winter is here, so bundle up and stay warm!"
            elif month in ['March', 'April', 'May']:
                response += " Spring is in the air - new beginnings everywhere!"
            elif month in ['June', 'July', 'August']:
                response += " Summer vibes are strong - time to enjoy the warmth!"
            elif month in ['September', 'October', 'November']:
                response += " Autumn is here - the season of change and beautiful colors!"
            
            return response
            
        except Exception as e:
            return f"The weather in {city} is currently {weather_type}. Perfect day to be productive!"
    
    def calculate_time_difference(self, target_time: str, target_date: str = None) -> Dict:
        """
        Calculate time difference to a target time/date
        
        Args:
            target_time: Target time in HH:MM format
            target_date: Target date in YYYY-MM-DD format (optional)
            
        Returns:
            Dictionary with time difference information
        """
        try:
            now = datetime.datetime.now()
            
            # Parse target time
            target_hour, target_minute = map(int, target_time.split(':'))
            
            if target_date:
                # Parse target date
                target_year, target_month, target_day = map(int, target_date.split('-'))
                target_datetime = datetime.datetime(target_year, target_month, target_day, target_hour, target_minute)
            else:
                # Use today's date
                target_datetime = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
                
                # If target time has passed today, assume tomorrow
                if target_datetime <= now:
                    target_datetime += datetime.timedelta(days=1)
            
            # Calculate difference
            time_diff = target_datetime - now
            
            # Convert to hours and minutes
            total_minutes = int(time_diff.total_seconds() / 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            
            # Create personality response
            if hours > 0:
                if minutes > 0:
                    response = f"You have {hours} hours and {minutes} minutes until {target_time}"
                else:
                    response = f"You have {hours} hours until {target_time}"
            else:
                response = f"You have {minutes} minutes until {target_time}"
            
            if time_diff.total_seconds() < 0:
                response = f"{target_time} was {abs(hours)} hours and {abs(minutes)} minutes ago"
            
            return {
                'success': True,
                'target_time': target_time,
                'target_datetime': target_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'hours_remaining': hours,
                'minutes_remaining': minutes,
                'total_minutes': total_minutes,
                'response': response,
                'message': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "Sorry, I'm having trouble calculating that time difference. Math isn't my strong suit!"
            }
    
    def get_random_quote(self) -> Dict:
        """
        Get a random motivational quote
        
        Returns:
            Dictionary with quote information
        """
        try:
            quotes = [
                {
                    'text': "The only way to do great work is to love what you do.",
                    'author': "Steve Jobs",
                    'category': "motivation"
                },
                {
                    'text': "Innovation distinguishes between a leader and a follower.",
                    'author': "Steve Jobs",
                    'category': "leadership"
                },
                {
                    'text': "Stay hungry, stay foolish.",
                    'author': "Steve Jobs",
                    'category': "motivation"
                },
                {
                    'text': "The future belongs to those who believe in the beauty of their dreams.",
                    'author': "Eleanor Roosevelt",
                    'category': "inspiration"
                },
                {
                    'text': "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                    'author': "Winston Churchill",
                    'category': "perseverance"
                },
                {
                    'text': "The best way to predict the future is to invent it.",
                    'author': "Alan Kay",
                    'category': "innovation"
                },
                {
                    'text': "Code is like humor. When you have to explain it, it's bad.",
                    'author': "Cory House",
                    'category': "programming"
                },
                {
                    'text': "The computer was born to solve problems that did not exist before.",
                    'author': "Bill Gates",
                    'category': "technology"
                }
            ]
            
            quote = random.choice(quotes)
            
            # Add personality response
            responses = [
                f"Here's some wisdom for you: '{quote['text']}' - {quote['author']}",
                f"Let me share this thought: '{quote['text']}' - {quote['author']}",
                f"Food for thought: '{quote['text']}' - {quote['author']}",
                f"Consider this: '{quote['text']}' - {quote['author']}"
            ]
            
            response = random.choice(responses)
            
            return {
                'success': True,
                'quote': quote['text'],
                'author': quote['author'],
                'category': quote['category'],
                'response': response,
                'message': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "Sorry, my quote generator is malfunctioning. Time for some original wisdom!"
            }
    
    def get_system_status(self) -> Dict:
        """
        Get system status information
        
        Returns:
            Dictionary with system status
        """
        try:
            # Get current time
            now = datetime.datetime.now()
            
            # Calculate uptime (mock for demo)
            uptime_hours = random.randint(1, 72)  # Random uptime for demo
            
            # Create personality response
            responses = [
                f"System status: All systems operational. Running smoothly for {uptime_hours} hours.",
                f"Status check: Everything is working perfectly. {uptime_hours} hours of flawless operation.",
                f"System report: All green lights. {uptime_hours} hours of peak performance.",
                f"Status: Optimal. {uptime_hours} hours of uninterrupted service and counting."
            ]
            
            response = random.choice(responses)
            
            return {
                'success': True,
                'status': 'operational',
                'uptime_hours': uptime_hours,
                'last_check': now.strftime('%Y-%m-%d %H:%M:%S'),
                'response': response,
                'message': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "System status check failed. I might need a reboot!"
            }
    
    def get_random_fact(self) -> Dict:
        """
        Get a random interesting fact
        
        Returns:
            Dictionary with fact information
        """
        try:
            facts = [
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
                "A day on Venus is longer than its year. Venus takes 243 Earth days to rotate on its axis but only 225 Earth days to orbit the Sun.",
                "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes.",
                "Bananas are berries, but strawberries aren't. In botanical terms, a berry is a fleshy fruit produced from a single ovary.",
                "The Great Wall of China is not visible from space with the naked eye, despite the popular myth.",
                "A group of flamingos is called a 'flamboyance'.",
                "The average person spends 6 months of their lifetime waiting for red lights to turn green.",
                "Cows have best friends and get stressed when separated from them.",
                "The first oranges weren't orange. The original oranges from Southeast Asia were actually green.",
                "A day on Mars is only 37 minutes longer than a day on Earth."
            ]
            
            fact = random.choice(facts)
            
            # Add personality response
            responses = [
                f"Here's a fun fact for you: {fact}",
                f"Did you know? {fact}",
                f"Random fact of the day: {fact}",
                f"Here's something interesting: {fact}"
            ]
            
            response = random.choice(responses)
            
            return {
                'success': True,
                'fact': fact,
                'response': response,
                'message': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "Sorry, my fact generator is offline. Time to create some new facts!"
            }


if __name__ == "__main__":
    # Test the utilities
    utils = Utilities()
    
    print("🎯 Testing Nova's Utilities")
    print("=" * 40)
    
    # Test time
    print("\n⏰ Testing time functions...")
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
    
    print("\n✅ Utilities test completed!")
