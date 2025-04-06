import sys
from typing import Optional
from database import AstrologyDB
from bot import AstrologyBot
import os
from dotenv import load_dotenv

class AstrologyBotCLI:
    def __init__(self):
        """Initialize the CLI interface."""
        self.db = AstrologyDB()
        self.bot = AstrologyBot(self.db)
        self.load_interpretations()
        
    def load_interpretations(self):
        """Load initial astrological interpretations."""
        interpretations = [
            "Sun in Aries represents leadership, initiative, and a pioneering spirit",
            "Moon in Cancer indicates emotional sensitivity and strong nurturing instincts",
            "Venus in Taurus shows appreciation for luxury, comfort, and sensual pleasures",
            "Mars in Leo demonstrates confidence, creativity, and a desire for recognition",
            "Jupiter in Sagittarius brings optimism, expansion, and philosophical growth",
            "Saturn in Capricorn represents discipline, responsibility, and long-term planning",
            "Uranus in Aquarius indicates innovation, independence, and humanitarian ideals",
            "Neptune in Pisces shows spiritual awareness, creativity, and compassion",
            "Pluto in Scorpio represents transformation, power, and deep psychological insight",
            "Mercury in Gemini indicates quick thinking, adaptability, and communication skills"
        ]
        
        for i, text in enumerate(interpretations):
            metadata = {
                "planet": text.split()[0],
                "sign": text.split()[2],
                "index": i
            }
            self.db.add_interpretation(text, metadata)
    
    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*50)
        print("Welcome to the Astrology Bot!")
        print("="*50)
        print("\nI can help you with:")
        print("1. Astrological interpretations")
        print("2. Planetary positions and meanings")
        print("3. Zodiac sign characteristics")
        print("4. General astrological advice")
        print("\nType 'exit' to quit or 'help' for more options.")
        print("-"*50)
    
    def print_help(self):
        """Print help message."""
        print("\nAvailable Commands:")
        print("- help: Show this help message")
        print("- exit: Exit the program")
        print("- clear: Clear the screen")
        print("- examples: Show example questions")
        print("- birthchart: Get birth chart interpretation")
        print("\nYou can also ask any astrological question directly!")
        print("-"*50)
    
    def print_examples(self):
        """Print example questions."""
        print("\nExample Questions:")
        print("1. What does it mean to have Mars in Leo?")
        print("2. Tell me about emotional sensitivity in astrology")
        print("3. What are the characteristics of Mercury in Gemini?")
        print("4. How can I develop my leadership skills based on my astrological profile?")
        print("-"*50)
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_welcome()
    
    def process_birth_chart(self):
        """Process birth chart related queries."""
        print("\nBirth Chart Interpretation")
        print("Please provide the following information:")
        date = input("Date of birth (DD/MM/YYYY): ")
        time = input("Time of birth (HH:MM): ")
        location = input("Place of birth: ")
        
        query = f"Interpret birth chart for {date} at {time} in {location}"
        response = self.bot.process_query(query)
        print("\nInterpretation:")
        print(response)
        print("-"*50)
    
    def run(self):
        """Run the CLI interface."""
        self.clear_screen()
        
        while True:
            try:
                user_input = input("\nYour question: ").strip().lower()
                
                if user_input == 'exit':
                    print("\nThank you for using Astrology Bot! Goodbye!")
                    break
                elif user_input == 'help':
                    self.print_help()
                elif user_input == 'clear':
                    self.clear_screen()
                elif user_input == 'examples':
                    self.print_examples()
                elif user_input == 'birthchart':
                    self.process_birth_chart()
                elif user_input:
                    print("\nProcessing your question...")
                    response = self.bot.process_query(user_input)
                    print("\nResponse:")
                    print(response)
                    print("-"*50)
                else:
                    print("Please enter a valid question or command.")
                    
            except KeyboardInterrupt:
                print("\n\nThank you for using Astrology Bot! Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Main entry point for the CLI."""
    try:
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY not found in .env file")
            print("Please add your OpenAI API key to the .env file")
            sys.exit(1)
            
        cli = AstrologyBotCLI()
        cli.run()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 