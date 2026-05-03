// 🔹 Phishing detection on page load
const currentUrl = window.location.href;

if (!currentUrl.startsWith("chrome://") &&
    !currentUrl.startsWith("http://localhost") &&
    !currentUrl.startsWith("http://127.0.0.1")) {

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
  warningDiv.style.width = "100%";
  warningDiv.style.backgroundColor = "#ef4444";
  warningDiv.style.color = "white";
  warningDiv.style.padding = "15px";
  warningDiv.style.zIndex = "999999";

  const reasonsText = reasons ? reasons.join(" | ") : "";

  warningDiv.innerHTML = `
    🚨 KAWACH ALERT: <b>${status}</b>
    <div style="font-size:12px;">${reasonsText}</div>
    <button id="kawach-close">Dismiss</button>
  `;

  document.body.appendChild(warningDiv);

  document.getElementById("kawach-close").onclick = () => warningDiv.remove();
}


// 🔹 PASSWORD FEATURE
document.addEventListener('focusin', (e) => {

  if (e.target.tagName === 'INPUT' && e.target.type === 'password') {

    const passwordInput = e.target;

    if (passwordInput.dataset.kawachInjected) return;
    passwordInput.dataset.kawachInjected = "true";

    const container = document.createElement("div");
    container.style.position = "absolute";
    container.style.zIndex = "9999999";

    const saveBtn = document.createElement("button");
    saveBtn.innerText = "🛡️ Save to KAWACH";
    saveBtn.style.background = "#6366f1";
    saveBtn.style.color = "white";
    saveBtn.style.padding = "6px 10px";
    saveBtn.style.border = "none";
    saveBtn.style.cursor = "pointer";

    container.appendChild(saveBtn);
    document.body.appendChild(container);

    const updatePosition = () => {
      const rect = passwordInput.getBoundingClientRect();
      container.style.top = (window.scrollY + rect.top - 40) + "px";
      container.style.left = (window.scrollX + rect.right - 150) + "px";
    };

    updatePosition();
    window.addEventListener('scroll', updatePosition);

    saveBtn.onclick = () => {

      let password = passwordInput.value;
      let website = window.location.hostname;
      let username = "Unknown";

      const form = passwordInput.closest('form');
      if (form) {
        const userInput = form.querySelector('input[type="text"], input[type="email"]');
        if (userInput) username = userInput.value;
      }

      if (!password) {
        saveBtn.innerText = "❌ Enter password first";
        return;
      }

      saveBtn.innerText = "⏳ Saving...";

      chrome.runtime.sendMessage({
        action: "savePassword",
        data: { website, username, password }
      }, (response) => {

        console.log("📥 Save Response:", response);

        if (response && response.status === "Success") {
          saveBtn.innerText = "✅ Saved!";
          saveBtn.style.background = "#10b981";
        } else {
          saveBtn.innerText = "❌ Failed!";
          saveBtn.style.background = "#ef4444";
        }

        setTimeout(() => {
          container.remove();
          window.removeEventListener('scroll', updatePosition);
        }, 3000);

      });
    };
  }
});
