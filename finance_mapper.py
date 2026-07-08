import requests
import json
import sqlite3

# Your official OpenFEC API key safely stored in the script
API_KEY = "sv23KTnGzGG6j5MJyhjMjvJUo4ykmMwxtjo7eLu9"
BASE_URL = "https://api.open.fec.gov/v1"

def triage_donor_sector(employer_name, pac_name):
    """
    Evaluates raw donor strings to categorize them by economic sector.
    """
    employer_name = str(employer_name).upper()
    pac_name = str(pac_name).upper()
    
    sector_keywords = {
        "FINANCE / BANKING": ["BANK", "CAPITAL", "INVESTMENT", "CHASE", "WELLS FARGO"],
        "DEFENSE / AEROSPACE": ["LOCKHEED", "BOEING", "NORTHROP", "RAYTHEON"],
        "PHARMACEUTICAL": ["PFIZER", "JOHNSON & JOHNSON", "MERCK", "ELI LILLY"],
        "ENERGY / UTILITIES": ["EXXON", "CHEVRON", "FLORIDA POWER", "NEXTERA", "FPL"]
    }
    
    for sector, keywords in sector_keywords.items():
        if any(keyword in pac_name for keyword in keywords):
            return sector
            
    for sector, keywords in sector_keywords.items():
        if any(keyword in employer_name for keyword in keywords):
            return sector
            
    return "Unclassified / General Public"

def fetch_candidate_finance(fec_candidate_id):
    """
    Pulls raw financial data directly from the Federal Election Commission.
    """
    url = f"{BASE_URL}/candidate/{fec_candidate_id}/totals/"
    params = {
        "api_key": API_KEY,
        "cycle": 2026 
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['results']:
            finances = data['results'][0]
            return {
                "Total Receipts": finances.get('receipts', 0),
                "Total Spent": finances.get('disbursements', 0),
                "Cash on Hand": finances.get('cash_on_hand_end_period', 0),
                "Debt": finances.get('debts_owed_by_committee', 0)
            }
        else:
            return "System Log: No current financial data filed for this candidate."
            
    except Exception as e:
        return f"System Log: Connection error - {e}"
