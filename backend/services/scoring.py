def calculate_cyber_health_score(device_risks: int, network_secure: bool, breached_accounts: int, weak_passwords: int) -> dict:
    """
    Calculates a Cyber Health Score (0-100) using a weighted analysis algorithm.
    
    Weights:
    - Device Risks (30%)
    - Network Security (20%)
    - Breached Accounts (30%)
    - Password Hygiene (20%)
    """
    score = 100
    
    # 1. Device Risks (Deduct up to 30 points)
    device_deduction = min(device_risks * 10, 30)
    score -= device_deduction
    
    # 2. Network Security (Deduct 20 points if unsecured)
    if not network_secure:
        score -= 20
        
    # 3. Breached Accounts (Deduct up to 30 points)
    breach_deduction = min(breached_accounts * 15, 30)
    score -= breach_deduction
    
    # 4. Password Hygiene (Deduct up to 20 points)
    password_deduction = min(weak_passwords * 5, 20)
    score -= password_deduction
    
    # Determine Status
    if score >= 80:
        status = "Excellent"
    elif score >= 50:
        status = "Fair"
    else:
        status = "Critical Risk"
        
    return {
        "score": score,
        "status": status,
        "breakdown": {
            "device_deduction": device_deduction,
            "network_deduction": 20 if not network_secure else 0,
            "breach_deduction": breach_deduction,
            "password_deduction": password_deduction
        }
    }
