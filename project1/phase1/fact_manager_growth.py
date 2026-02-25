import json
import os
import requests
import json
import time

# Define the API endpoint URL for a random fact
API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"
# Use a constant for the filename for easy management
FACTS_FILE = 'fact_archive.json'

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
            return fact_text
        else:
            print("\n⚠️ Could not find the fact text in the API response.")

    except requests.exceptions.RequestException as e:
        # This catches network-related errors (e.g., no internet connection)
        print(f"\n❌ Error connecting to the API: {e}")
    except json.JSONDecodeError:
        # This catches errors if the response isn't valid JSON
        print("\n❌ Error: Failed to parse the response from the API.")

def load_facts():
    """
    Loads facts from the JSON file.
    If the file doesn't exist, it returns an empty list.
    """
    if not os.path.exists(FACTS_FILE):
        return []  # Return an empty list if the file is not found
    try:
        with open(FACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # In case the file is empty or corrupted, start fresh
        return []

def save_facts(facts):
    """
    Saves the list of facts to the JSON file.
    The 'indent=4' makes the file human-readable.
    """
    with open(FACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(facts, f, indent=4, ensure_ascii=False)

def is_duplicate(new_fact_text, existing_facts):
    """
    Checks if a new fact's text already exists in the archive.
    """
    # Create a set of existing fact texts for very fast lookups
    existing_texts = {fact['text'] for fact in existing_facts}
    return new_fact_text in existing_texts

def add_unique_fact(new_fact_text):
    """
    Main function to add a new fact if it is not a duplicate.
    Returns True if the fact was added, False otherwise.
    """
    print(f"Attempting to add fact: '{new_fact_text}'")
    
    # 1. Load existing facts
    all_facts = load_facts()
    
    # 2. Check for duplicates
    if is_duplicate(new_fact_text, all_facts):
        print("⚡ Status: Fact is a duplicate. Not added.")
        return False
        
    # 3. Add the new fact
    new_fact = {'text': new_fact_text}
    all_facts.append(new_fact)
    
    # 4. Save the updated list back to the file
    save_facts(all_facts)
    
    print("✅ Status: New fact added successfully!")
    return True

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Running Fact Archive Manager ---")
    while True:
        fact = get_random_fact()
        # Add the first fact (should be new)
        add_unique_fact(fact)
        time.sleep(60)

    # Print final state of the archive
    final_archive = load_facts()
    print(f"🚀 Final Archive contains {len(final_archive)} facts.")
    print(final_archive)