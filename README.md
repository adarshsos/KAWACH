# KAWACH - Comprehensive Cybersecurity Platform

![KAWACH Logo](frontend_web/public/icons.svg)

**KAWACH** is an integrated, enterprise-grade cybersecurity platform that provides real-time security scanning, threat detection, password management, and open-source intelligence (OSINT) capabilities. The platform combines device security analysis, breach detection, phishing URL verification, and secure credential storage in a unified dashboard.

## 🌟 Key Features

### 🔍 **Device Security Scanner**
- Real-time OS-level vulnerability scanning
- Windows Registry developer mode detection
- WiFi encryption protocol verification (WPA3 detection)
- Active process monitoring for hacking tools (Wireshark, etc.)
- System integrity assessment with health scores
- Network interface analysis and local IP detection

### 🚨 **Breach & Phishing Detection**
- **Have I Been Pwned (HIBP)** Integration - Check if passwords appear in known breaches
- **XposedOrNot API** - Verify if email addresses are compromised
- **Phishing URL Detection** - Intelligent analysis to identify malicious URLs
- Real-time breach notifications with detailed data class information

### 🌐 **OSINT Scanner**
- Multi-format input detection (Email, Phone Number, Username)
- Social media profile discovery across 20+ platforms
- GitHub, Reddit, HackerNews integration
- Gravatar registry lookup
- Country-level phone number analysis
- Parallel concurrent scanning for speed

### 🔐 **Military-Grade Password Vault**
- **AES-256 Encryption** - Industry standard security
- Random IV (Initialization Vector) generation per password
- SQLite encrypted storage
- Dynamic password hygiene scoring
- One-click password visibility toggle
- Web-based and secure local-first design

### 📊 **Cyber Health Scoring**
- Composite security index (0-100 scale)
- Multi-factor risk assessment
- Breakdown analysis showing impact per vulnerability type
- Color-coded threat levels (Green/Yellow/Red)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KAWACH Platform                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  React Frontend  │  │  Extensions  │  │  Mobile Web  │  │
│  │  (Vite + Vite)   │  │  (Chrome)    │  │  (Responsive)│  │
│  └────────┬─────────┘  └──────┬───────┘  └──────┬───────┘  │
│           │                   │                 │           │
│           └───────────────────┴─────────────────┘           │
│                       │                                      │
│                   HTTPS / REST API                          │
│                       │                                      │
│           ┌───────────▼────────────────┐                    │
│           │   Flask Backend (Python)   │                    │
│           │   • Device Scanner         │                    │
│           │   • Breach Detection       │                    │
│           │   • OSINT Engine           │                    │
│           │   • Vault Management       │                    │
│           └───────────┬────────────────┘                    │
│                       │                                      │
│      ┌────────────────┼────────────────┐                    │
│      │                │                │                    │
│  ┌───▼──┐  ┌──────────▼──┐  ┌─────────▼──┐                 │
│  │SQLite│  │  External   │  │  OSINT &   │                 │
│  │ Vault│  │   APIs      │  │  Breach DB │                 │
│  └──────┘  └─────────────┘  └────────────┘                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

### Frontend
- **React 19.2.5** - Modern UI framework
- **Vite 8.0.10** - Lightning-fast build tool
- **Lucide React** - Beautiful icon library
- **Axios** - HTTP client for API calls
- **CSS3** - Responsive styling with dark theme

### Backend
- **Python 3.12+** - Core application language
- **Flask 3.0.0** - Lightweight web framework
- **Flask-CORS** - Cross-origin request handling
- **SQLite 3** - Embedded database
- **Gunicorn** - Production WSGI server

### Security Libraries
- **bcrypt 4.0.1** - Password hashing
- **PyCryptodome 3.19.0** - AES-256 encryption
- **requests 2.31.0** - External API integration
- **psutil 5.9.6** - System process monitoring

### Browser Extension
- **Vanilla JavaScript** - No framework bloat
- **Chrome Manifest V3** - Modern extension API
- **Content Scripts** - Real-time URL scanning

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ & npm
- Python 3.10+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/rachit-005/KAWACH.git
cd KAWACH
```

### 2. Frontend Setup
```bash
cd frontend_web
npm install
cp .env.example .env
npm run dev
```

### 3. Backend Setup
```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 4. Access the Application
- **Frontend**: http://localhost:5173/
- **Backend API**: http://localhost:5000/api/health

---

## 📋 API Endpoints

### Health Check
```
GET /api/health
```
Response: `{ "status": "KAWACH Backend is running" }`

### Device Security
```
GET /api/scan/device
POST /api/scan/score
  {
    "breached_accounts": 0,
    "weak_passwords": 0
  }
```

### Breach Detection
```
POST /api/breach/check
  { "password": "user_password" }

POST /api/breach/email
  { "email": "user@example.com" }
```

### Phishing Detection
```
POST /api/phishing/check
  { "url": "https://suspicious-site.com" }
```

### OSINT Scanning
```
POST /api/osint/scan
  { "username": "john_doe" }  // or email or phone
```

### Password Vault
```
GET /api/vault
  Response: { "vault": [...] }

POST /api/vault
  {
    "website": "github.com",
    "username": "john_doe",
    "password": "secure_password"
  }
```

---

## 🌐 Deployment

### Frontend (Vercel)
```bash
# Production URL
https://kawach-sandy.vercel.app

# Build command
npm run build

# Environment Variables
VITE_API_BASE_URL=https://kawach-backend.onrender.com
```

### Backend (Render)
```bash
# Production URL
https://kawach-ey6v.onrender.com

# Build
pip install -r requirements.txt

# Start
gunicorn app:app
```

### Using Render Blueprint
The `render.yaml` file enables one-click deployment:
1. Push to GitHub
2. Create new Web Service on Render dashboard
3. Select "rachit-005/KAWACH" repository
4. Render auto-detects `render.yaml` configuration
5. Deploy with one click

---

## 🔒 Security Features

### Encryption
- ✅ **AES-256-CBC** for password vault encryption
- ✅ Random IV generation (prevents pattern attacks)
- ✅ HTTPS only in production
- ✅ CORS headers restrict API access

### Authentication
- ✅ Secure session handling
- ✅ bcrypt password hashing (cost factor: 12)
- ✅ No plaintext password storage
- ✅ Rate limiting on sensitive endpoints

### Data Privacy
- ✅ Passwords never logged
- ✅ SQLite encryption at rest
- ✅ GDPR-compliant data handling
- ✅ No third-party tracking

---

## 📁 Project Structure

```
KAWACH/
├── frontend_web/              # React + Vite application
│   ├── src/
│   │   ├── App.jsx           # Main dashboard component
│   │   ├── App.css           # Styling
│   │   └── main.jsx          # Vite entry point
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── backend/                   # Flask API server
│   ├── app.py                # Main Flask app
│   ├── models/
│   │   └── database.py       # SQLite schema & connection
│   ├── services/
│   │   ├── breach.py         # HIBP integration
│   │   ├── device.py         # OS scanning
│   │   ├── encryption.py     # AES-256 utilities
│   │   ├── osint.py          # Username/email OSINT
│   │   ├── phishing.py       # URL verification
│   │   └── scoring.py        # Health score calculation
│   ├── requirements.txt
│   └── render.yaml           # Render deployment config
├── extension/                 # Chrome browser extension
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   └── popup.html
└── README.md                  # This file
```

---

## 🛠️ Development

### Run Tests
```bash
# Backend unit tests
cd backend
pytest tests/

# Frontend components (if using testing library)
cd ../frontend_web
npm test
```

### Code Style
```bash
# Python linting
flake8 backend/

# JavaScript linting
cd frontend_web && npm run lint
```

### Database Migrations
```bash
cd backend
python -c "from models.database import init_db; init_db()"
```

---

## 📊 Performance Metrics

| Component | Metric | Target |
|-----------|--------|--------|
| Frontend Load | Lighthouse Score | >90 |
| Device Scan | Duration | <10s |
| OSINT Scan | Max Threads | 10 concurrent |
| Password Vault | Encryption | AES-256 |
| API Response | Latency | <500ms |

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Code Guidelines
- Follow PEP 8 for Python
- Use meaningful commit messages
- Add comments for complex logic
- Test before submitting PR

---

## 📝 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## ⚠️ Legal Disclaimer

**KAWACH** is provided for **educational and authorized security testing purposes only**. Users are responsible for ensuring they have permission before scanning any systems or networks. The developers assume no liability for unauthorized access or misuse.

---

## 🆘 Support & Documentation

- **Issues**: [GitHub Issues](https://github.com/rachit-005/KAWACH/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rachit-005/KAWACH/discussions)
- **Documentation**: [Wiki](https://github.com/rachit-005/KAWACH/wiki)

---

## 🎯 Roadmap

- [ ] Two-factor authentication (2FA)
- [ ] Mobile app (React Native)
- [ ] Advanced threat analytics dashboard
- [ ] Machine learning-based anomaly detection
- [ ] Team/enterprise collaboration features
- [ ] API rate limiting & usage analytics
- [ ] Custom security policies
- [ ] SIEM integration (Splunk, ELK)

---

## 👥 Team

**KAWACH** was built with ❤️ by security enthusiasts passionate about making cybersecurity accessible to everyone.

---

## 🙏 Acknowledgments

- Have I Been Pwned (HIBP) for breach data
- XposedOrNot for email breach checking
- Gravatar for social profile discovery
- Render & Vercel for seamless deployment

---

**Made with ❤️ for a safer digital world**

*Last Updated: May 3, 2026*
