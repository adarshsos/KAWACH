import requests
import concurrent.futures
import re
import hashlib

def scan_username(target: str) -> list:
    """
    Deep Data Extraction OSINT Scanner.
    Automatically detects Email vs Phone vs Username and routes to the correct intelligence engine.
    """
    # 1. Detect if target is an Email
    if re.match(r"[^@]+@[^@]+\.[^@]+", target):
        return _scan_email(target)
        
    # 2. Detect if target is a Phone Number (e.g., +1234567890)
    clean_target = target.replace(" ", "").replace("-", "")
    if re.match(r"^\+?[1-9]\d{6,14}$", clean_target):
        return _scan_phone(clean_target)
        
    # 3. Otherwise, treat as Username
    return _scan_social_profiles(target)

def _scan_email(email: str) -> list:
    found_profiles = []
    
    # Gravatar API (Global Avatar Registry) - 100% Real
    md5_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(f"https://en.gravatar.com/{md5_hash}.json", headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if "entry" in data and len(data["entry"]) > 0:
                entry = data["entry"][0]
                found_profiles.append({
                    "platform": "Gravatar Global Registry",
                    "url": entry.get("profileUrl", ""),
                    "metadata": {
                        "Preferred Username": entry.get("preferredUsername", "N/A"),
                        "Display Name": entry.get("displayName", "N/A"),
                        "Profile Verified": "Yes"
                    }
                })
    except Exception:
        pass
        
    # Additional logic: if we wanted, we could add Hunter.io or other APIs here.
    if not found_profiles:
        # If no gravatar is found, return a generic analysis
        domain = email.split('@')[1]
        found_profiles.append({
            "platform": "Domain Analysis",
            "url": f"http://{domain}",
            "metadata": {
                "Email Domain": domain,
                "Status": "No public social profiles linked directly to this exact email address."
            }
        })
        
    return found_profiles

def _scan_phone(phone: str) -> list:
    found_profiles = []
    if not phone.startswith("+"):
        phone = "+" + phone
        
    # Real deterministic prefix analysis for Open Source Intelligence
    # Instead of an API key, we map ITU-T E.164 country codes natively
    country_map = {
        "+1": "USA/Canada", "+44": "United Kingdom", "+91": "India", "+61": "Australia", 
        "+81": "Japan", "+49": "Germany", "+33": "France", "+86": "China",
        "+55": "Brazil", "+7": "Russia/Kazakhstan", "+27": "South Africa"
    }
    
    region = "Unknown Region"
    for prefix in sorted(country_map.keys(), key=len, reverse=True):
        if phone.startswith(prefix):
            region = country_map[prefix]
            break
            
    found_profiles.append({
        "platform": "Telecom OSINT Mapping",
        "url": "#",
        "metadata": {
            "Phone Number": phone,
            "Origin Region": region,
            "Validation Status": "Valid E.164 Format",
            "Public Records": "Requires Law Enforcement Subpoena or Premium API"
        }
    })
    
    return found_profiles

def _scan_social_profiles(username: str) -> list:
    # Rich Data APIs for deep extraction (SpiderFoot style)
    rich_platforms = {
        "GitHub": f"https://api.github.com/users/{username}",
        "HackerNews": f"https://hacker-news.firebaseio.com/v0/user/{username}.json",
        "Reddit": f"https://www.reddit.com/user/{username}/about.json"
    }
    
    # Standard Boolean HTTP checks (Sherlock style)
    basic_platforms = {
        "Patreon": f"https://www.patreon.com/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Linktree": f"https://linktr.ee/{username}",
        "Flickr": f"https://www.flickr.com/photos/{username}/"
    }

    found_profiles = []

    def check_rich_site(name, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) KAWACH OSINT/1.0'}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200 and response.text != "null":
                data = response.json()
                metadata = {}
                if name == "GitHub":
                    metadata = {
                        "Name": data.get("name", "N/A"),
                        "Company": data.get("company", "N/A"),
                        "Location": data.get("location", "N/A"),
                        "Public Repos": data.get("public_repos", 0),
                        "Followers": data.get("followers", 0)
                    }
                elif name == "HackerNews":
                    metadata = {
                        "Karma": data.get("karma", 0),
                        "Created": data.get("created", 0)
                    }
                elif name == "Reddit":
                    if "data" in data:
                        metadata = {
                            "Total Karma": data["data"].get("total_karma", 0),
                            "Verified Email": "Yes" if data["data"].get("has_verified_email", False) else "No",
                            "Is Employee": "Yes" if data["data"].get("is_employee", False) else "No"
                        }
                    else:
                        return None
                return {"platform": name, "url": f"https://{name.lower()}.com/{username}", "metadata": metadata}
        except Exception:
            pass
        return None

    def check_basic_site(name, url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                return {"platform": name, "url": url, "metadata": {"Status": "Public Profile Found", "Exposure": "High"}}
        except Exception:
            pass
        return None

    # Run checks in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for name, url in rich_platforms.items():
            futures.append(executor.submit(check_rich_site, name, url))
        for name, url in basic_platforms.items():
            futures.append(executor.submit(check_basic_site, name, url))
            
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                found_profiles.append(res)
                
    return found_profiles
