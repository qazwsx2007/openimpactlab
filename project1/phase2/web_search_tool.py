import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
# --- Configuration ---
# Load your secret API key from an environment variable.
# NEVER hardcode your API key in the script.

load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")

def get_search_results(query: str, num_results: int = 5):
    """
    Performs a Google search using the SerpApi service.

    Args:
        query (str): The search query.
        num_results (int): The number of search results to return.

    Returns:
        list: A list of dictionaries, where each dictionary represents a search result.
              Returns an empty list if the search fails or no results are found.
    """
    if not API_KEY:
        print("Error: SERPAPI_API_KEY environment variable not set.")
        return []

    # API parameters
    params = {
        "q": query,
        "api_key": API_KEY,
        "num": num_results,
        "engine": "google", # Specifies to use the Google search engine
        "gl": "us",         # Geolocation for the search
        "hl": "en"          # Interface language
    }

    try:
        print(f"⚡ Performing web search for: '{query}' using SerpApi...")
        search = GoogleSearch(params)
        results = search.get_dict()

        formatted_results = []
        # Check for organic results, which are the main search listings
        if 'organic_results' in results:
            for item in results['organic_results']:
                formatted_results.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'snippet': item.get('snippet')
                })
        else:
            # Sometimes there's an answer box but no organic results for very specific queries
            if 'answer_box' in results and 'snippet' in results['answer_box']:
                 formatted_results.append({
                    'title': results['answer_box'].get('title', query),
                    'link': results['answer_box'].get('link', ''),
                    'snippet': results['answer_box'].get('snippet')
                })
            else:
                print("No organic search results found.")

        return formatted_results

    except Exception as e:
        print(f"An unexpected error occurred with SerpApi: {e}")
        return []

# --- Main execution block to test the function ---
if __name__ == "__main__":
    search_query = "What is the role of reinforcement learning in robotics?"
    search_results = get_search_results(search_query)

    if search_results:
        print(f"\n✅ Found {len(search_results)} results:\n")
        # Print the raw search results as requested
        for i, result in enumerate(search_results, 1):
            print(f"--- Result {i} ---")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}\n")
    else:
        print("Search failed or returned no results.")