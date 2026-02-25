import os
import google.generativeai as genai
from serpapi import GoogleSearch
from dotenv import load_dotenv

# --- 1. Configuration ---
# Load API keys from environment variables for security
try:
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
except KeyError:
    print("🔴 Error: Please set the 'GOOGLE_API_KEY' and 'SERPAPI_API_KEY' environment variables.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)


# --- 2. Define the Web Search Tool ---
# This is our local Python function. The model will not execute this directly.
# It will ask US to execute it with the right arguments.
def web_search(query: str) -> str:
    """
    Performs a web search using the Google Search engine to find up-to-date information,
    recent events, or topics outside of the model's training data.
    
    Args:
        query: The specific search query string.
    
    Returns:
        A formatted string containing the top search results, including snippets and links.
    """
    print(f"⚡ Manually executing web search for: '{query}'")
    try:
        params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        # Process and format the results for the LLM.
        output_str = ""
        if "organic_results" in results and results["organic_results"]:
            for result in results["organic_results"][:5]: # Top 5 results
                output_str += f"Title: {result.get('title', 'N/A')}\n"
                output_str += f"Link: {result.get('link', 'N/A')}\n"
                output_str += f"Snippet: {result.get('snippet', 'N/A')}\n---\n"
        elif "answer_box" in results:
             output_str += f"Answer Box: {results['answer_box'].get('snippet') or results['answer_box'].get('answer')}\n---\n"
        else:
            return "No relevant search results found."
            
        return output_str
    except Exception as e:
        return f"An error occurred during web search: {e}"

# --- 3. Initialize the Model with the Tool ---
# We pass the function itself into the tools list. The SDK handles converting it
# into a format the model can understand.
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[web_search],
    system_instruction=(
        "You are a helpful and intelligent research assistant. "
        "Your goal is to answer the user's questions accurately and concisely. "
        "If a question requires current information or knowledge beyond your training, "
        "use the web_search tool to get the information first, then provide your final answer."
    )
)

# --- 4. Main Execution Loop (Manual Agent Logic) ---
if __name__ == "__main__":
    print("🚀 AI Web Explorer (Manual Mode) is ready! Ask me anything. Type 'exit' to quit.")
    
    # Start a chat session. Automatic function calling will handle the back-and-forth
    # between the model deciding to use a tool and our code executing it.
    chat = model.start_chat(enable_automatic_function_calling=True)

    while True:
        user_question = input("\n> You: ")
        if user_question.lower() == 'exit':
            print("👋 Goodbye!")
            break
        
        print("🤖 Thinking...")
        
        # This single call now handles the entire multi-step process:
        # 1. Sends the user question to the model.
        # 2. If the model responds with a FunctionCall, the SDK will pause.
        # 3. It then calls our `web_search` function with the correct arguments.
        # 4. It takes the return value and sends it back to the model in a second API call.
        # 5. The final response from the model (after it has the search results) is returned here.
        response = chat.send_message(user_question)
        
        # The final answer is in the 'text' attribute of the last message in the chat.
        print(f"\n> AI: {response.text}")
