import os
import google.generativeai as genai
from dotenv import load_dotenv

def setup_ai_brain():
    """
    Configures the Gemini API key from environment variables.
    """
    # Load environment variables from a .env file
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
    
    genai.configure(api_key=api_key)
    print("✅ AI Brain setup complete.")

def ask_ai(question):
    """
    Sends a question to the Gemini model and returns the response.
    
    Args:
        question (str): The user's question.

    Returns:
        str: The AI's response.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Send the prompt and get the response
        response = model.generate_content(question)
        
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    """
    Main function to run the AI research assistant.
    """
    print("🧠 Welcome to your AI Research Assistant!")
    print("This script connects to the Gemini API to answer your questions.")
    
    try:
        setup_ai_brain()
        
        while True:
            # Get user input
            user_question = input("\n❓ Ask your question (or type 'exit' to quit): ")
            
            if user_question.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            if not user_question:
                print("Please enter a question.")
                continue

            print("\n🤔 Thinking...")
            
            # Get the AI's answer
            ai_response = ask_ai(user_question)
            
            # Print the final answer
            print("\n💡 AI Response:")
            print("----------------")
            print(ai_response)
            print("----------------")

    except ValueError as ve:
        print(f"⚠️ Configuration Error: {ve}")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()