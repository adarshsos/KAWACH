import urllib.parse
import re

def evaluate_url(url: str) -> dict:
    """
    Evaluates a URL against OWASP standards to detect phishing.
    """
    risk_score = 0
    reasons = []
    
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return {"risk_score": 100, "status": "Invalid URL", "reasons": ["URL cannot be parsed"]}

    # 1. Protocol check
    if parsed.scheme != 'https':
        risk_score += 40
        reasons.append("Unsecured protocol (HTTP instead of HTTPS)")
        
    # 2. IP Address in Domain
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", parsed.netloc):
        risk_score += 50
        reasons.append("IP Address used instead of Domain Name")
        
    # 3. Suspicious characters
    if '@' in url:
        risk_score += 30
        reasons.append("Contains '@' symbol, often used to spoof domains")
        
    # 4. Long URL
    if len(url) > 75:
        risk_score += 10
        reasons.append("URL length is unusually long")
        
    # 5. Multiple subdomains
    if parsed.netloc.count('.') > 3:
        risk_score += 20
        reasons.append("Unusually high number of subdomains")

    status = "Safe"
    if risk_score > 60:
        status = "High Risk (Phishing)"
    elif risk_score > 30:
        status = "Moderate Risk (Suspicious)"

    return {
        "risk_score": min(risk_score, 100),
        "status": status,
        "reasons": reasons
    }
