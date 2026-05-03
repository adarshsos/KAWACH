import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, Smartphone, Wifi, Key, AlertTriangle, Link as LinkIcon, Database, CheckCircle, Eye, EyeOff, Globe, Download, Activity, Search } from 'lucide-react';
import './App.css';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'https://kawach-ey6v.onrender.com').replace(/\/$/, '');
const apiUrl = (path) => `${API_BASE_URL}${path}`;
function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [showDocs, setShowDocs] = useState(false);
  
  // Dashboard State
  const [scoreData, setScoreData] = useState(null);
  const [loadingScore, setLoadingScore] = useState(true);

  // Phishing State
  const [url, setUrl] = useState('');
  const [phishResult, setPhishResult] = useState(null);

  // Breach State
  const [breachEmail, setBreachEmail] = useState('');
  const [breachResult, setBreachResult] = useState(null);

  // OSINT State
  const [osintInput, setOsintInput] = useState('');
  const [osintResult, setOsintResult] = useState(null);

  // Vault State
  const [vaultData, setVaultData] = useState([]);
  const [newVault, setNewVault] = useState({ website: '', username: '', password: '' });
  const [showPasswords, setShowPasswords] = useState({});

  useEffect(() => {
    fetchScore();
  }, []);

  const fetchScore = async () => {
    setLoadingScore(true);
    try {
      const response = await axios.post(apiUrl('/api/scan/score'), {
        breached_accounts: 0,
        weak_passwords: 0
      });
      setScoreData(response.data);
    } catch (error) {
      console.error("Backend error", error);
    }
    setLoadingScore(false);
  };

  const checkPhishing = async () => {
    try {
      const response = await axios.post(apiUrl('/api/phishing/check'), { url });
      setPhishResult(response.data);
    } catch (e) {
      console.error(e);
    }
  };

  const checkBreach = async () => {
    try {
      const response = await axios.post(apiUrl('/api/breach/email'), { email: breachEmail });
      setBreachResult(response.data);
    } catch (e) {
      console.error(e);
    }
  };

  const checkOsint = async () => {
    try {
      setOsintResult({loading: true});
      // Send the raw input to backend so the new intelligent routing can detect Email vs Phone vs Username
      const cleanInput = osintInput.trim();
      const response = await axios.post(apiUrl('/api/osint/scan'), { username: cleanInput });
      setOsintResult(response.data);
    } catch (e) {
      console.error(e);
      setOsintResult(null);
    }
  };

  const fetchVault = async () => {
    try {
      const response = await axios.get(apiUrl('/api/vault'));
      setVaultData(response.data.vault);
    } catch (e) {
      console.error(e);
    }
  };

  const saveToVault = async () => {
    try {
      await axios.post(apiUrl('/api/vault'), newVault);
      setNewVault({ website: '', username: '', password: '' });
      fetchVault();
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    let interval;
    if (activeTab === 'vault') {
      fetchVault();
      interval = setInterval(fetchVault, 3000);
    }
    return () => clearInterval(interval);
  }, [activeTab]);

  const getPasswordHygiene = (password) => {
    if (password.length > 12 && /[A-Z]/.test(password) && /[0-9]/.test(password) && /[^A-Za-z0-9]/.test(password)) {
      return { label: 'Strong', color: '#10b981' };
    }
    if (password.length > 8) {
      return { label: 'Moderate', color: '#f59e0b' };
    }
    return { label: 'Weak', color: '#ef4444' };
  };

  const renderDashboard = () => {
    if (loadingScore || !scoreData) return <div style={{textAlign:'center'}}>Scanning System...</div>;
    
    const color = scoreData.score >= 80 ? '#10b981' : scoreData.score >= 50 ? '#f59e0b' : '#ef4444';
    const deg = `${(scoreData.score / 100) * 360}deg`;

    // Make sure advanced metrics exists (fallback for older backend responses)
    const adv = scoreData.advanced_metrics || {
      dev_mode: "Unknown", system_update: "Unknown", wifi_protocol: "Unknown", malicious_apps: 0
    };

    return (
      <div>
        <h2 className="gradient-heading"><Shield color="#38bdf8" /> Device Security Scanner</h2>
        <p style={{color: '#94a3b8', marginBottom: '2rem', lineHeight: '1.6'}}>
          This module performs a real-time, low-level OS scan on your actual machine. It checks your Windows Registry for Developer Mode vulnerabilities, uses the native <code>netsh</code> command to verify your active Wi-Fi encryption protocol (e.g., WPA3), and actively monitors your PID list for suspicious hacking tools (like Wireshark).
        </p>
        <div className="dashboard-grid">
          <div className="score-section">
            <h2 style={{fontWeight: 'normal', color: 'var(--text-secondary)'}}>Health Score</h2>
            <div className="score-circle" style={{ '--score-color': color, '--score-deg': deg }}>
              <div className="score-inner">{scoreData.score}</div>
            </div>
            <h3 style={{ color }}>{scoreData.status}</h3>
          </div>
          <div className="details-section">
            <div className="detail-item">
              <div className="detail-icon"><Smartphone /></div>
              <div>
                <h3>System Integrity</h3>
                <p style={{fontSize: '0.85rem', color: '#cbd5e1'}}>OS Update: <span style={{color: adv.system_update === 'Up to date' ? '#10b981' : '#f59e0b'}}>{adv.system_update}</span></p>
                <p style={{fontSize: '0.85rem', color: '#cbd5e1'}}>Developer Mode: <span style={{color: adv.dev_mode === 'Disabled' ? '#10b981' : '#ef4444'}}>{adv.dev_mode}</span></p>
                <p style={{fontSize: '0.85rem', color: '#cbd5e1'}}>Malicious Permissions: <span style={{color: adv.malicious_apps === 0 ? '#10b981' : '#ef4444'}}>{adv.malicious_apps} detected</span></p>
              </div>
            </div>
            <div className="detail-item">
              <div className="detail-icon"><Wifi /></div>
              <div>
                <h3>Network Interfaces</h3>
                <p style={{fontSize: '0.85rem', color: '#cbd5e1'}}>Protocol: <span style={{color: '#38bdf8'}}>{adv.wifi_protocol}</span></p>
                <p style={{fontSize: '0.85rem', color: '#cbd5e1'}}>{scoreData.breakdown.network_deduction === 0 ? 'No suspicious ports found' : 'Unsecured Local Ports Detected'}</p>
                {adv.active_interfaces && adv.active_interfaces.length > 0 && (
                  <div style={{marginTop: '0.5rem', background: 'rgba(0,0,0,0.2)', padding: '0.5rem', borderRadius: '4px'}}>
                    <div style={{fontSize: '0.75rem', color: '#94a3b8', marginBottom: '2px'}}>Active Local IP(s):</div>
                    {adv.active_interfaces.map((intf, idx) => (
                      <div key={idx} style={{fontSize: '0.8rem', fontFamily: 'monospace', color: '#10b981'}}>{intf.ip} <span style={{color: '#64748b'}}>({intf.name})</span></div>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <button className="action-btn" onClick={fetchScore} style={{marginTop: '1rem'}}>Run Full Scan Again</button>
          </div>
        </div>
      </div>
    );
  };

  const renderVault = () => (
    <div>
      <h2 className="gradient-heading"><Database color="#38bdf8" /> Password Manager (AES-256)</h2>
      <p style={{marginBottom: '2rem', color: 'var(--text-secondary)', lineHeight: '1.6'}}>
        This is a Google-Style Password Vault. When you save a password, the Python backend generates a secure Initialization Vector (IV) and encrypts it using military-grade <b>AES-256</b> before it ever touches the SQLite database. It includes a dynamic Password Hygiene evaluator.
      </p>
      
      <div className="input-group" style={{background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '12px'}}>
        <input placeholder="Website (e.g., google.com)" className="input-field" value={newVault.website} onChange={e => setNewVault({...newVault, website: e.target.value})} />
        <input placeholder="Username" className="input-field" value={newVault.username} onChange={e => setNewVault({...newVault, username: e.target.value})} />
        <input type="password" placeholder="Password" className="input-field" value={newVault.password} onChange={e => setNewVault({...newVault, password: e.target.value})} />
        <button className="action-btn" onClick={saveToVault}>Encrypt & Save to Vault</button>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '2rem'}}>
        {vaultData.map((item) => {
          const hygiene = getPasswordHygiene(item.password || '');
          return (
            <div key={item.id} style={{background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.5rem', position: 'relative', overflow: 'hidden'}}>
              <div style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '4px', background: hygiene.color}}></div>
              <h3 style={{margin: '0 0 0.5rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem'}}><Globe size={18}/> {item.website}</h3>
              <p style={{color: '#94a3b8', fontSize: '0.9rem', marginBottom: '1rem'}}>{item.username}</p>
              
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#0f172a', padding: '0.5rem 1rem', borderRadius: '6px'}}>
                <span style={{fontFamily: 'monospace', letterSpacing: '2px'}}>
                  {showPasswords[item.id] ? item.password : '••••••••'}
                </span>
                <button 
                  style={{background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer'}}
                  onClick={() => setShowPasswords({...showPasswords, [item.id]: !showPasswords[item.id]})}
                >
                  {showPasswords[item.id] ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              <div style={{marginTop: '1rem', fontSize: '0.8rem', display: 'flex', justifyContent: 'space-between'}}>
                <span style={{color: '#64748b'}}>Hygiene Score:</span>
                <span style={{color: hygiene.color, fontWeight: 'bold'}}>{hygiene.label}</span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  );

  const renderBreach = () => (
    <div>
      <h2 className="gradient-heading"><AlertTriangle color="#38bdf8" /> Breach Scanner (HIBP)</h2>
      <p style={{marginBottom: '2rem', color: 'var(--text-secondary)', lineHeight: '1.6'}}>
        This scanner queries the Have I Been Pwned database. Enter your email address to extract exact information about leaked data classes (passwords, IP addresses, locations) and the specific domains where the breach occurred.
      </p>
      
      <div className="input-group">
        <input 
          type="email" 
          placeholder="Enter your email address (e.g., adarsh@example.com)" 
          className="input-field"
          value={breachEmail}
          onChange={(e) => setBreachEmail(e.target.value)}
        />
        <button className="action-btn" onClick={checkBreach}>Check HIBP Database</button>
      </div>

      {breachResult && (
        <div className="result-box" style={{ borderColor: breachResult.count > 0 ? '#ef4444' : '#10b981' }}>
          {breachResult.count > 0 ? (
            <div>
              <h3 style={{color: '#ef4444', marginBottom: '1.5rem'}}>⚠️ WARNING: Email found in {breachResult.count} data breaches!</h3>
              <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
                {breachResult.breaches.map((breach, idx) => (
                  <div key={idx} style={{background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '1rem', borderRadius: '8px'}}>
                    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem'}}>
                      <h4 style={{margin: 0, fontSize: '1.1rem', color: '#f87171'}}>{breach.Name} <span style={{color: '#94a3b8', fontSize: '0.9rem', fontWeight: 'normal'}}>({breach.Domain})</span></h4>
                      <span style={{background: 'rgba(0,0,0,0.5)', padding: '2px 8px', borderRadius: '12px', fontSize: '0.8rem', color: '#cbd5e1'}}>{breach.BreachDate}</span>
                    </div>
                    <div style={{fontSize: '0.85rem', color: '#cbd5e1'}}>
                      <strong style={{color: '#94a3b8'}}>Leaked Data:</strong> {breach.DataClasses.join(", ")}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <h3 style={{color: '#10b981'}}><CheckCircle size={20} style={{verticalAlign:'middle'}}/> Good News! This email was not found in any known breach database.</h3>
          )}
        </div>
      )}
    </div>
  );

  const renderOsint = () => (
    <div>
      <h2 className="gradient-heading"><Search color="#38bdf8" /> OSINT Engine (SpiderFoot + Sherlock)</h2>
      <p style={{marginBottom: '2rem', color: 'var(--text-secondary)', lineHeight: '1.6'}}>
        This is a fully functional Open-Source Intelligence (OSINT) engine integrating <b>Sherlock's multi-threading profile extraction</b> with <b>SpiderFoot's Deep Data Enrichment</b>. Enter a username, email, or phone number to uncover publicly available digital footprints and hidden metadata.
      </p>
      
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Enter Email, Phone No., or Username" 
          className="input-field"
          value={osintInput}
          onChange={(e) => setOsintInput(e.target.value)}
        />
        <button className="action-btn" onClick={checkOsint}>Initiate OSINT Extraction</button>
      </div>

      {osintResult && osintResult.loading && (
        <div style={{textAlign: 'center', color: '#38bdf8', marginTop: '2rem'}}>Engaging Data Enrichment Engine...</div>
      )}

      {osintResult && !osintResult.loading && (
        <div className="result-box" style={{ borderColor: osintResult.profiles_found > 3 ? '#ef4444' : '#f59e0b' }}>
          <h3>Data Enrichment Complete for: <span style={{color: 'white'}}>{osintResult.username}</span></h3>
          <p style={{marginTop: '0.5rem', color: '#94a3b8', marginBottom: '1.5rem'}}>
            Found active metadata on {osintResult.profiles_found} platforms.
          </p>
          
          <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
            {osintResult.platforms.map((item, idx) => (
              <div key={idx} style={{background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '12px'}}>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.8rem'}}>
                  <h4 style={{margin: 0, color: '#38bdf8', fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem'}}>🌐 {item.platform}</h4>
                  <a href={item.url} target="_blank" rel="noreferrer" style={{color: '#a5b4fc', fontSize: '0.8rem', textDecoration: 'none', border: '1px solid #a5b4fc', padding: '2px 8px', borderRadius: '12px'}}>View Profile ↗</a>
                </div>
                <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', background: 'rgba(0,0,0,0.2)', padding: '0.8rem', borderRadius: '8px'}}>
                  {Object.entries(item.metadata).map(([key, val], i) => (
                    <div key={i} style={{fontSize: '0.85rem'}}>
                      <span style={{color: '#94a3b8', fontFamily: 'monospace'}}>{key}:</span> <span style={{color: '#fff', fontWeight: 'bold'}}>{String(val)}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <p style={{marginTop: '1.5rem', fontWeight: 'bold', color: osintResult.profiles_found > 3 ? '#ef4444' : '#f59e0b'}}>
            Risk Assessment: {osintResult.risk_assessment}
          </p>
        </div>
      )}
    </div>
  );

  const renderPhishing = () => (
    <div>
      <h2 className="gradient-heading"><LinkIcon color="#38bdf8" /> Phishing Link Detector</h2>
      <p style={{marginBottom: '2rem', color: 'var(--text-secondary)', lineHeight: '1.6'}}>
        This scanner applies strict OWASP security rules to any URL you enter. It dissects the URL via Python regex to detect HTTP usage, suspicious symbols (like @ for spoofing), IP address masking, and abnormal subdomain lengths.
      </p>
      
      <div className="input-group">
        <input type="text" placeholder="Enter a URL (e.g., http://suspicious-site.com)" className="input-field" value={url} onChange={(e) => setUrl(e.target.value)} />
        <button className="action-btn" onClick={checkPhishing}>Analyze URL</button>
      </div>

      {phishResult && (
        <div className="result-box" style={{ borderColor: phishResult.risk_score > 50 ? '#ef4444' : '#10b981' }}>
          <h3>Status: <span style={{color: phishResult.risk_score > 50 ? '#ef4444' : '#10b981'}}>{phishResult.status}</span></h3>
          <p>Risk Score: {phishResult.risk_score}/100</p>
          {phishResult.reasons.length > 0 && (
            <ul style={{marginTop: '1rem', marginLeft: '1.5rem', color: 'var(--text-secondary)'}}>
              {phishResult.reasons.map((r, i) => <li key={i}>{r}</li>)}
            </ul>
          )}
        </div>
      )}
    </div>
  );

  const renderExtensionIntegration = () => (
    <div>
      <h2 className="gradient-heading"><Globe color="#38bdf8" /> Live Extension Protection</h2>
      <p style={{marginBottom: '2rem', color: 'var(--text-secondary)', lineHeight: '1.6'}}>
        The KAWACH Chrome extension is actively running in the background. It uses <b>Content Scripts</b> to physically intercept login forms dynamically (like 1Password) and executes real-time Phishing analysis. <b>If you visit a phishing website right now, the extension will instantly freeze the DOM and inject a massive red warning popup across your entire browser.</b>
      </p>

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem'}}>
        <div style={{background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.3)'}}>
          <h3 style={{color: '#10b981', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem'}}><CheckCircle size={18}/> Extension Active</h3>
          <p style={{fontSize: '0.9rem', color: '#cbd5e1'}}>Background Service Worker is currently monitoring DOM mutations and URLs.</p>
        </div>
        <div style={{background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '12px', border: '1px solid rgba(56, 189, 248, 0.3)'}}>
          <h3 style={{color: '#38bdf8', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem'}}><AlertTriangle size={18}/> Phishing Protection Engine</h3>
          <p style={{fontSize: '0.9rem', color: '#cbd5e1'}}>The extension will automatically inject a red popup if it detects IP-based URLs, Typosquatting, or known malicious domains.</p>
        </div>
        <div className="result-box" style={{borderLeftColor: '#10b981', margin: 0}}>
          <h3 style={{display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981'}}>
            <Activity size={20} /> Background Protection
          </h3>
          <p style={{marginTop: '1rem', color: '#cbd5e1', fontSize: '0.9rem', lineHeight: '1.5'}}>
            Automatically injects password generators and securely saves them to your vault without navigating away from the page.
          </p>
        </div>
        <div className="result-box" style={{borderLeftColor: '#f59e0b', margin: 0}}>
          <h3 style={{display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b'}}>
            <Shield size={20} /> Threat Injection
          </h3>
          <p style={{marginTop: '1rem', color: '#cbd5e1', fontSize: '0.9rem', lineHeight: '1.5'}}>
            If a high-risk phishing website is detected, the extension physically overrides the DOM to inject a red warning banner.
          </p>
        </div>
      </div>

      <div style={{background: 'rgba(255,255,255,0.03)', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)'}}>
        <h3 style={{marginBottom: '1rem'}}>Install KAWACH Extension</h3>
        <p style={{color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.9rem', lineHeight: '1.5'}}>
          To protect end-users without them needing the source code, you can distribute this lightweight ZIP package. They can easily add it directly to their Chromium-based browsers (Chrome, Edge, Brave).
        </p>
        
        <a href="/kawach-extension.zip" download="kawach-extension.zip" style={{textDecoration: 'none'}}>
          <button className="action-btn" style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', width: '100%', marginBottom: '2rem', padding: '1rem', fontSize: '1.1rem', background: 'linear-gradient(135deg, #6366f1, #38bdf8)'}}>
            <Download size={22} /> Download Extension Package (.zip)
          </button>
        </a>

        <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          <div style={{display: 'flex', alignItems: 'flex-start', gap: '0.8rem'}}>
            <div style={{background: '#38bdf8', color: '#0f172a', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '0.8rem', flexShrink: 0}}>1</div>
            <p style={{margin: 0, color: '#cbd5e1', fontSize: '0.9rem'}}><b>Extract</b> the downloaded `.zip` file to any folder on your computer.</p>
          </div>
          <div style={{display: 'flex', alignItems: 'flex-start', gap: '0.8rem'}}>
            <div style={{background: '#38bdf8', color: '#0f172a', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '0.8rem', flexShrink: 0}}>2</div>
            <p style={{margin: 0, color: '#cbd5e1', fontSize: '0.9rem'}}>Open your browser and navigate to <b>chrome://extensions</b></p>
          </div>
          <div style={{display: 'flex', alignItems: 'flex-start', gap: '0.8rem'}}>
            <div style={{background: '#38bdf8', color: '#0f172a', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '0.8rem', flexShrink: 0}}>3</div>
            <p style={{margin: 0, color: '#cbd5e1', fontSize: '0.9rem'}}>Toggle <b>Developer mode</b> (top right), click <b>Load unpacked</b>, and select the unzipped folder.</p>
          </div>
        </div>
        
        <div style={{marginTop: '2rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1.5rem', textAlign: 'center'}}>
          <button className="action-btn" onClick={() => setShowDocs(true)} style={{display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', background: 'transparent', border: '1px solid #38bdf8', color: '#38bdf8', width: 'auto', padding: '0.5rem 1.5rem'}}>
             View Technical Architecture Docs
          </button>
        </div>
      </div>
    </div>
  );

  const renderDocsModal = () => {
    if (!showDocs) return null;
    return (
      <div style={{position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.8)', zIndex: 9999, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '2rem'}}>
        <div style={{backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '16px', padding: '2.5rem', width: '100%', maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto'}}>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem'}}>
            <h2 style={{margin: 0, color: '#6366f1'}}>KAWACH Technical Documentation</h2>
            <button onClick={() => setShowDocs(false)} style={{background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.5rem'}}>✕</button>
          </div>
          
          <h3 style={{color: '#38bdf8', marginTop: '1.5rem'}}>1. AES-256 Encryption Engine</h3>
          <p style={{lineHeight: 1.6, color: '#cbd5e1'}}>
            The Secure Vault uses symmetric Advanced Encryption Standard (AES) with a 256-bit key in CBC mode. When you save a password, a secure Initialization Vector (IV) is generated. The password is padded to the block size and encrypted before hitting the SQLite database.
          </p>

          <h3 style={{color: '#38bdf8', marginTop: '1.5rem'}}>2. Proprietary Cyber Health Score</h3>
          <p style={{lineHeight: 1.6, color: '#cbd5e1'}}>
            The scoring engine uses a weighted heuristic algorithm based on Device Risks, Network Protocols, Breach Exposure, and Password Hygiene.
          </p>

          <h3 style={{color: '#38bdf8', marginTop: '1.5rem'}}>3. HIBP k-Anonymity Breach Check</h3>
          <p style={{lineHeight: 1.6, color: '#cbd5e1'}}>
            The app hashes your password via SHA-1 locally and sends <strong>only the first 5 characters</strong> to the Have I Been Pwned API to ensure k-Anonymity privacy.
          </p>

          <h3 style={{color: '#38bdf8', marginTop: '1.5rem'}}>4. OWASP Phishing Logic</h3>
          <p style={{lineHeight: 1.6, color: '#cbd5e1'}}>
            The URL analyzer applies OWASP heuristics dynamically (HTTP check, IP domain, suspicious symbols) to calculate a 0-100 Risk Score.
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <div className="sidebar">
        <div className="sidebar-title">KAWACH</div>
        <div className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
          <Shield /> Device Scanner
        </div>
        <div className={`nav-item ${activeTab === 'vault' ? 'active' : ''}`} onClick={() => setActiveTab('vault')}>
          <Database /> Password Manager
        </div>
        <div className={`nav-item ${activeTab === 'breach' ? 'active' : ''}`} onClick={() => setActiveTab('breach')}>
          <AlertTriangle /> Breach Scanner
        </div>
        <div className={`nav-item ${activeTab === 'osint' ? 'active' : ''}`} onClick={() => setActiveTab('osint')}>
          <Search /> OSINT Finder
        </div>
        <div className={`nav-item ${activeTab === 'phishing' ? 'active' : ''}`} onClick={() => setActiveTab('phishing')}>
          <LinkIcon /> Phishing Detector
        </div>
        <div className={`nav-item ${activeTab === 'extension' ? 'active' : ''}`} onClick={() => setActiveTab('extension')} style={{marginTop: 'auto', borderTop: '1px solid rgba(255,255,255,0.1)', borderRadius: '0 0 12px 12px'}}>
          <Globe /> Extension Integration
        </div>
      </div>

      {/* Main Content Area */}
      <div className="main-content">
        <div className="glass-panel" style={{minHeight: '600px'}}>
          {activeTab === 'dashboard' && renderDashboard()}
          {activeTab === 'vault' && renderVault()}
          {activeTab === 'breach' && renderBreach()}
          {activeTab === 'osint' && renderOsint()}
          {activeTab === 'phishing' && renderPhishing()}
          {activeTab === 'extension' && renderExtensionIntegration()}
        </div>
      </div>

      {renderDocsModal()}
    </div>
  );
}

export default App;
