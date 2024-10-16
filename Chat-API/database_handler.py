import sqlite3
from dotenv import load_dotenv
import os
from supabase import create_client, Client
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def initialize_database():
    #Create table in supabase
    pass
def check_api_key(api_key):
    #Check if the API key is valid
    response = supabase.table('api_keys').select('*').eq('api_key', api_key).execute()
    if response.data:
        return True
    else:
        return False
    
def store_api_key(name, email, api_key):
    data = {
        'id': str(uuid.uuid4()),  # Generate a unique ID
        'name': name,
        'email': email,
        'api_key': api_key,
        'created_at': datetime.now().isoformat()
    }

    # Insert the data into Supabase
    response = supabase.table('api_keys').insert(data).execute()

    if response.status_code == 201:
        print("API key successfully stored.")
    else:
        print(f"Failed to store API key: {response.data}")