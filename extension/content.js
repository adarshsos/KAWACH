// Real-time evaluation when a page loads
const currentUrl = window.location.href;

// Don't scan local pages or chrome extensions
if (!currentUrl.startsWith("chrome://") && !currentUrl.startsWith("http://localhost") && !currentUrl.startsWith("http://127.0.0.1")) {
  chrome.runtime.sendMessage({ action: "checkPhishing", url: currentUrl }, (response) => {
    if (response && response.risk_score > 60) {
      injectWarning(response.status, response.reasons);
    }
  });
}

function injectWarning(status, reasons) {
  const warningDiv = document.createElement("div");
  warningDiv.style.position = "fixed";
  warningDiv.style.top = "0";
  warningDiv.style.left = "0";
  warningDiv.style.width = "100%";
  warningDiv.style.backgroundColor = "#ef4444";
  warningDiv.style.color = "white";
  warningDiv.style.padding = "15px";
  warningDiv.style.zIndex = "999999";
  warningDiv.style.textAlign = "center";
  warningDiv.style.fontFamily = "sans-serif";
  warningDiv.style.fontSize = "16px";
  warningDiv.style.fontWeight = "bold";
  warningDiv.style.boxShadow = "0 4px 6px rgba(0,0,0,0.3)";
  
  const reasonsText = reasons ? reasons.join(" | ") : "";
  
  warningDiv.innerHTML = `
    🚨 KAWACH SECURITY ALERT: This website has been flagged as <b>${status}</b>! 
    <span style="font-size: 14px; font-weight: normal; display: block; margin-top: 5px;">Reasons: ${reasonsText}</span>
    <button id="kawach-dismiss-btn" style="margin-top: 10px; background: white; color: #ef4444; border: none; padding: 5px 15px; cursor: pointer; border-radius: 4px; font-weight: bold;">I understand the risks, dismiss</button>
  `;
  
  document.body.appendChild(warningDiv);
  
  document.getElementById("kawach-dismiss-btn").addEventListener("click", () => {
    warningDiv.remove();
  });
}

// ---------------------------------------------------------
// LASTPASS / 1PASSWORD STYLE PASSWORD CAPTURE & GENERATOR
// ---------------------------------------------------------

document.addEventListener('focusin', (e) => {
  if (e.target.tagName === 'INPUT' && e.target.type === 'password') {
    const passwordInput = e.target;
    
    // Prevent multiple injections
    if (passwordInput.dataset.kawachInjected) return;
    passwordInput.dataset.kawachInjected = "true";

    // Create a container for our buttons
    const container = document.createElement("div");
    container.style.position = "absolute";
    container.style.zIndex = "9999999";
    container.style.display = "flex";
    container.style.gap = "8px";
    
    // Generate Password Button
    const genBtn = document.createElement("button");
    genBtn.innerHTML = "🪄 Generate Strong";
    genBtn.style.background = "#3b82f6"; // Blue
    genBtn.style.color = "white";
    genBtn.style.border = "none";
    genBtn.style.borderRadius = "6px";
    genBtn.style.padding = "6px 12px";
    genBtn.style.fontSize = "13px";
    genBtn.style.cursor = "pointer";
    genBtn.style.fontWeight = "bold";
    genBtn.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";
    genBtn.style.transition = "all 0.2s ease";

    // Save Password Button
    const saveBtn = document.createElement("button");
    saveBtn.innerHTML = "🛡️ Save to KAWACH";
    saveBtn.style.background = "#6366f1"; // Indigo
    saveBtn.style.color = "white";
    saveBtn.style.border = "none";
    saveBtn.style.borderRadius = "6px";
    saveBtn.style.padding = "6px 12px";
    saveBtn.style.fontSize = "13px";
    saveBtn.style.cursor = "pointer";
    saveBtn.style.fontWeight = "bold";
    saveBtn.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";
    saveBtn.style.transition = "all 0.2s ease";

    container.appendChild(genBtn);
    container.appendChild(saveBtn);
    document.body.appendChild(container);

    // Position it slightly above and to the right of the password field
    const updatePosition = () => {
      const rect = passwordInput.getBoundingClientRect();
      container.style.top = (window.scrollY + rect.top - 40) + "px";
      container.style.left = (window.scrollX + rect.right - 270) + "px"; // Adjusted for two buttons
    };
    
    updatePosition();
    window.addEventListener('scroll', updatePosition);

    // Handle Generate Click
    genBtn.addEventListener('click', (ev) => {
      ev.preventDefault();
      
      // Cryptographically strong random generation
      const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+";
      let strongPass = "";
      for (let i = 0; i < 16; i++) {
        strongPass += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      
      passwordInput.value = strongPass;
      
      // Trigger React/Vue state updates
      passwordInput.dispatchEvent(new Event('input', { bubbles: true }));
      passwordInput.dispatchEvent(new Event('change', { bubbles: true }));
      
      // Show password momentarily so user can see it
      passwordInput.type = "text";
      setTimeout(() => passwordInput.type = "password", 2500);

      genBtn.innerHTML = "✅ Filled!";
      genBtn.style.background = "#10b981";
      setTimeout(() => {
        genBtn.innerHTML = "🪄 Generate Strong";
        genBtn.style.background = "#3b82f6";
      }, 2500);
    });

    // Handle Save Click
    saveBtn.addEventListener('click', (ev) => {
      ev.preventDefault();
      
      const form = passwordInput.closest('form');
      let username = "Unknown User";
      if (form) {
        let usernameInput = form.querySelector('input[type="text"], input[type="email"]');
        if (usernameInput && usernameInput.value) {
          username = usernameInput.value;
        }
      }
      
      let password = passwordInput.value;
      let website = window.location.hostname;

      if (!password) {
        saveBtn.innerHTML = "❌ Type password first!";
        saveBtn.style.background = "#ef4444";
        setTimeout(() => {
          saveBtn.innerHTML = "🛡️ Save to KAWACH";
          saveBtn.style.background = "#6366f1";
        }, 2000);
        return;
      }

      saveBtn.innerHTML = "⏳ Encrypting...";
      
      // Send to background script
      chrome.runtime.sendMessage({ 
        action: "savePassword", 
        data: { website, username, password } 
      }, (response) => {
        saveBtn.innerHTML = "✅ Saved to Vault!";
        saveBtn.style.background = "#10b981";
        setTimeout(() => {
          container.remove();
          window.removeEventListener('scroll', updatePosition);
        }, 3000);
      });
    });
  }
});
