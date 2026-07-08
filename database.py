import sqlite3
import json
from finance_mapper import fetch_candidate_finance

# database.py - The Permanent Steel Vault

# --- PART 1: THE ENGINE BLOCK (SQLite) ---
def connect_vault():
    """Creates a permanent file on the hard drive and builds the ledger."""
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    
    # Build the structural steel: a table with 3 columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ledger (
            id TEXT PRIMARY KEY,
            title TEXT,
            payload TEXT
        )
    ''')
    conn.commit()
    return conn

def insert_record(conn, record_id, title, payload):
    """Bolts a single record into the database."""
    cursor = conn.cursor()
    
    # If the payload is a dictionary (like the FEC math), convert it to text for storage
    if isinstance(payload, dict):
        payload_str = json.dumps(payload)
    else:
        payload_str = str(payload)
        
    cursor.execute('''
        INSERT OR REPLACE INTO ledger (id, title, payload)
        VALUES (?, ?, ?)
    ''', (record_id, title, payload_str))
    conn.commit()

def search_record(conn, record_id):
    """Pulls a record directly from the hard drive."""
    cursor = conn.cursor()
    cursor.execute("SELECT title, payload FROM ledger WHERE id = ?", (record_id,))
    result = cursor.fetchone()
    if result:
        return {"title": result[0], "payload": result[1]}
    return "Receipt not found."


# --- PART 2: THE FUEL TANK (History) ---
def load_historical_ledger(conn):
    """Pours the 3,000-year playbook into permanent storage."""
    historical_records = [
        {
            "id": "mission_statement",
            "title": "The Mission: The 3,000-Year Playbook",
            "payload": "For 3,000 years, a tiny ruling class has hoarded the world's wealth. They built myths, manipulated the truth, and divided us to keep us from seeing the ledger..."
        },
        {
            "id": "broken_model",
            "title": "The Broken Business Model",
            "payload": "The present economic system allows a tiny minority to accumulate massive capital while treating the destruction of habitable environments as a standard cost of doing business..."
        },
        {
            "id": "europe_india_drain",
            "title": "The European Record: The India Drain",
            "payload": "The British East India Company forced Indian farmers to grow cash crops. Economists calculated Great Britain drained $45 trillion from India using a rigged tax system."
        },
        {
            "id": "us_revolt",
            "title": "The US Record: The First Anti-Corporate Strike",
            "payload": "The 1773 Boston Tea Party was a direct, violent strike against the British East India Company monopoly, not just a polite argument over taxes."
        },
        {
            "id": "us_betrayal",
            "title": "The American Betrayal",
            "payload": "The American ruling class rebuilt the exact same corporate machine. Today, megacorporations use predatory loans and algorithms to mine the global public."
        },
        {
            "id": "europe_germany",
            "title": "The European Record: Germany (The War Machine)",
            "payload": "During WWII, corporations like IG Farben built factories next to concentration camps, intentionally using human beings as disposable slave labor to maximize profit margins."
        },
        {
            "id": "europe_france",
            "title": "The European Record: France (The Ransom)",
            "payload": "France forced Haiti to pay a massive ransom for freeing themselves from slavery, and created the CFA Franc to lock African national wealth inside the Paris treasury."
        },
        {
            "id": "europe_royals",
            "title": "The Royal Ledger",
            "payload": "The British Monarchy operates a $20 billion tax-free real estate empire. The jewels in their crowns are the exact stones looted from India and Africa."
        },
        {
            "id": "europe_bankers",
            "title": "The Bankers (The War Financiers)",
            "payload": "The Bank of England was created in 1694 to float national war debt. Banks loan money at interest for wars, and the working class pays the bill for generations."
        }
    ]

    for record in historical_records:
        insert_record(conn, record["id"], record["title"], record["payload"])
        
    print(f"SYSTEM STATUS: Successfully locked {len(historical_records)} historical records to the hard drive.")

# --- PART 3: THE FEC DATA LOADER ---
def load_campaign_dossier(conn, candidate_id):
    """Pulls raw FEC data and locks it into the permanent database."""
    print(f"SYSTEM STATUS: Initiating data pull for Candidate {candidate_id}...")
    
    finance_data = fetch_candidate_finance(candidate_id)
    
    if isinstance(finance_data, str):
        print(finance_data)
        return False
        
    title = f"Campaign Finance Dossier: {candidate_id}"
    insert_record(conn, candidate_id, title, finance_data)
    print(f"SYSTEM STATUS: Dossier {candidate_id} secured in permanent storage.")

# --- PART 4: IGNITION ---
if __name__ == "__main__":
    # 1. Connect to the permanent file
    vault_conn = connect_vault()
    
    # 2. Load the history
    load_historical_ledger(vault_conn)
    
    # 3. Pull the financial numbers
    load_campaign_dossier(vault_conn, "H6AZ03245")
    
    # 4. Verify the locks held
    print("\n--- PERMANENT VAULT INSPECTION ---")
    print("Historical Record:", search_record(vault_conn, "us_betrayal")['title'])
    print("Financial Record:", search_record(vault_conn, "H6AZ03245")['payload'])
    
    # 5. Shut the engine down cleanly
    vault_conn.close()