# ai/ai_matcher.py

import os
import sqlite3
import pandas as pd
from google import genai

# --- Initialize Gemini AI Client ---
client = None
try:
    # The API key is automatically picked up from the GEMINI_API_KEY environment variable.
    client = genai.Client()
except Exception as e:
    print(f"Warning: Failed to initialize Gemini AI client: {e}. AI suggestions will be unavailable.")

DB_NAME = "farmermarket.db"


def fetch_recent_data():
    """
    Fetch recent data from the SQLite database.
    Returns a dictionary containing 'tools' and 'crops' DataFrames.
    """
    conn = sqlite3.connect(DB_NAME)
    try:
        tools_df = pd.read_sql_query("SELECT * FROM tools ORDER BY rowid DESC LIMIT 10", conn)
        crops_df = pd.read_sql_query("SELECT * FROM crops ORDER BY rowid DESC LIMIT 10", conn)
    except Exception as e:
        print(f"Error fetching data from DB: {e}")
        tools_df = pd.DataFrame()
        crops_df = pd.DataFrame()
    finally:
        conn.close()

    return {
        "tools": tools_df,
        "crops": crops_df
    }


def get_recommendations(context: dict):
    """
    Generate AI-powered marketplace recommendations based on context and recent DB data.
    Returns a string with suggestions or a fixed error message if AI is unavailable.
    
    :param context: Dictionary containing user context or preferences.
    """
    if not client:
        return "(AI suggestion unavailable: Gemini AI client not initialized.)"

    # Fetch recent database data
    recent_data = fetch_recent_data()

    # Prepare prompt for the AI model
    prompt = f"""
As an AI assistant for a farmer's marketplace, your task is to provide actionable recommendations to a farmer based on their recent activity.

**Farmer's Context:**
- **Name:** {context.get('farmer', 'A farmer')}
- **Location:** {context.get('location', 'their area')}
- **Recent Action:** Listed a {context.get('type')} for {'rent' if context.get('type') == 'tool' else 'sale'}.
- **Item:** {context.get('item')}

**Recent Marketplace Activity:**
- **Recent Tools Listed:** {recent_data['tools'].to_dict(orient='records')}
- **Recent Crops Listed:** {recent_data['crops'].to_dict(orient='records')}

**Your Task:**
Generate 2-3 concise and practical recommendations for the farmer. The recommendations should be directly related to their recent activity and the overall marketplace context.

**Example Recommendations:**

*   **For a farmer who listed a tractor for rent:**
    *   "Consider also listing your plow and seeder. Farmers who rent tractors often need these implements as well."
    *   "There is a high demand for wheat in your area. Consider planting wheat in the next season."

*   **For a farmer who listed wheat for sale:**
    *   "A new harvester was just listed for rent in your area. It could help you with your next harvest."
    *   "Consider diversifying your crops. Many farmers in your area are also planting corn."

**Recommendations for {context.get('farmer', 'the farmer')}:**
-
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', contents=prompt
        )
        return response.text
    except Exception as e:
        return f"(AI suggestion unavailable due to an error: {e})"
