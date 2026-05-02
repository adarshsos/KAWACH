import requests
import hashlib

def check_breach(password: str = None) -> int:
    breach_count = 0
    if password:
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                hashes = (line.split(':') for line in response.text.splitlines())
                for h, count in hashes:
                    if h == suffix:
                        breach_count += int(count)
                        break
        except Exception:
            pass
    return breach_count

def check_email_breach(email: str) -> list:
    """
    REAL implementation querying the free, open-source XposedOrNot API for email data breaches.
    This replaces the HIBP simulation and provides 100% authentic, real-time cyber security data.
    """
    headers = {'User-Agent': 'kawach-security-app'}
    found_breaches = []
    
    try:
        # Step 1: Check if email is breached
        check_url = f"https://api.xposedornot.com/v1/check-email/{email}"
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "breaches" in data and len(data["breaches"]) > 0:
                breach_names = data["breaches"][0]
                
                # Step 2: Fetch detailed metadata for the found breaches
                all_breaches_response = requests.get("https://api.xposedornot.com/v1/breaches", headers=headers, timeout=10)
                if all_breaches_response.status_code == 200:
                    all_breaches = all_breaches_response.json().get("exposedBreaches", [])
                    
                    # Create a dictionary for instant O(1) lookup
                    breach_dict = {b.get("breachID", ""): b for b in all_breaches}
                    
                    for name in breach_names:
                        if name in breach_dict:
                            b_data = breach_dict[name]
                            found_breaches.append({
                                "Name": b_data.get("breachID", name),
                                "Domain": b_data.get("domain", "Unknown"),
                                "BreachDate": b_data.get("breachedDate", "Unknown").split("T")[0],
                                "DataClasses": b_data.get("exposedData", ["Email addresses"])
                            })
                        else:
                            # Fallback if specific metadata is missing
                            found_breaches.append({
                                "Name": name,
                                "Domain": "Unknown",
                                "BreachDate": "Unknown",
                                "DataClasses": ["Email addresses"]
                            })
        elif response.status_code == 404:
            return [] # Safely return empty list if no breaches found!
            
    except Exception as e:
        print(f"Error querying XposedOrNot: {e}")
        pass
        
    return found_breaches
