from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from models.database import init_db, get_db_connection

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize Database
init_db()

# Import Services
from services.phishing import evaluate_url
from services.device import scan_device
from services.scoring import calculate_cyber_health_score
from services.encryption import hash_password, check_password, encrypt_vault_data, decrypt_vault_data
from services.breach import check_breach

# ---------------- HEALTH CHECK ----------------
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "KAWACH Backend is running"})


# ---------------- PHISHING ----------------
@app.route('/api/phishing/check', methods=['POST'])
def check_phishing():
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    result = evaluate_url(url)
    return jsonify(result)


# ---------------- DEVICE SCAN ----------------
@app.route('/api/scan/device', methods=['GET'])
def run_device_scan():
    result = scan_device()
    return jsonify(result)


# ---------------- CYBER SCORE ----------------
@app.route('/api/scan/score', methods=['POST'])
def get_cyber_score():
    data = request.get_json()

    device_scan = scan_device()
    
    score = calculate_cyber_health_score(
        device_risks=device_scan['device_risks'],
        network_secure=device_scan['network_secure'],
        breached_accounts=data.get('breached_accounts', 0),
        weak_passwords=data.get('weak_passwords', 0)
    )

    score['advanced_metrics'] = device_scan.get('advanced_metrics', {})
    return jsonify(score)


# ---------------- BREACH CHECK ----------------
@app.route('/api/breach/check', methods=['POST'])
def run_breach_check():
    data = request.get_json()
    password = data.get('password', '')

    if not password:
        return jsonify({"error": "Password is required"}), 400

    count = check_breach(password=password)
    return jsonify({"breaches_found": count})


@app.route('/api/breach/email', methods=['POST'])
def run_email_breach_check():
    data = request.get_json()
    email = data.get('email', '')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    from services.breach import check_email_breach
    results = check_email_breach(email)

    return jsonify({
        "breaches": results,
        "count": len(results)
    })


# ---------------- OSINT ----------------
@app.route('/api/osint/scan', methods=['POST'])
def osint_scan():
    data = request.get_json()
    username = data.get('username', '')

    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    from services.osint import scan_username
    found_sites = scan_username(username)

    return jsonify({
        "username": username,
        "profiles_found": len(found_sites),
        "platforms": found_sites,
        "risk_assessment": "High Exposure" if len(found_sites) >= 2 else "Moderate Exposure"
    })


# ---------------- VAULT ----------------
@app.route('/api/vault', methods=['GET', 'POST'])
def manage_vault():
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = 1

    cursor.execute("""
        INSERT OR IGNORE INTO users (id, username, password_hash)
        VALUES (1, 'admin', 'dummyhash')
    """)
    conn.commit()

    if request.method == 'POST':
        data = request.get_json()
        website = data.get('website')
        username = data.get('username')
        password = data.get('password')

        encrypted_pw, iv = encrypt_vault_data(password)

        cursor.execute("""
            INSERT INTO vault (user_id, website, username, encrypted_password, iv)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, website, username, encrypted_pw, iv))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "Success",
            "message": "Password encrypted (AES-256) and saved"
        })

    elif request.method == 'GET':
        cursor.execute("""
            SELECT id, website, username, encrypted_password, iv
            FROM vault WHERE user_id = ?
        """, (user_id,))

        rows = cursor.fetchall()
        passwords = []

        for row in rows:
            try:
                decrypted = decrypt_vault_data(row['encrypted_password'], row['iv'])
            except:
                decrypted = "Error decrypting"

            passwords.append({
                "id": row['id'],
                "website": row['website'],
                "username": row['username'],
                "password": decrypted
            })

        conn.close()
        return jsonify({"vault": passwords})


# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
