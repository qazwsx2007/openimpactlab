import requests
import json

# Define the API endpoint URL for a random fact
API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"

def get_random_fact():
    """
    Connects to the uselessfacts API, fetches a random fact, and displays it.
    """
    print("Connecting to the Fact Stream...")
    try:
        # Step 1: Make the GET request to the API
        response = requests.get(API_URL)

        # Step 2: Check if the request was successful (e.g., status code 200 OK)
        # This will raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Step 3: Parse the JSON response into a Python dictionary
        fact_data = response.json()

        # Step 4: Extract the fact text from the dictionary
        # Using .get() is safer than direct key access (e.g., fact_data['text'])
        # as it won't crash if the 'text' key is missing.
        fact_text = fact_data.get('text')

        if fact_text:
            print("\n✅ Successfully fetched a fact:")
            print(f"-> {fact_text}")
        else:
            print("\n⚠️ Could not find the fact text in the API response.")

    except requests.exceptions.RequestException as e:
        # This catches network-related errors (e.g., no internet connection)
        print(f"\n❌ Error connecting to the API: {e}")
    except json.JSONDecodeError:
        # This catches errors if the response isn't valid JSON
        print("\n❌ Error: Failed to parse the response from the API.")

# This ensures the code runs only when the script is executed directly
if __name__ == "__main__":
    get_random_fact()