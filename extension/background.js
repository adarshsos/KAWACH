const BASE_URL = "https://kawach-ey6v.onrender.com";

console.log("✅ Background script loaded");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

  console.log("📩 Message received:", request);

  // 🔹 Phishing Check
  if (request.action === "checkPhishing") {
    fetch(`${BASE_URL}/api/phishing/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: request.url })
    })
    .then(res => res.json())
    .then(data => {
      console.log("🛡️ Phishing Response:", data);
      sendResponse(data);
    })
    .catch(err => {
      console.error("❌ Phishing Error:", err);
      sendResponse({ status: "Error" });
    });

    return true;
  }

  // 🔹 Save Password
  if (request.action === "savePassword") {
    console.log("🔐 Sending password:", request.data);

    fetch(`${BASE_URL}/api/vault`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request.data)
    })
    .then(res => res.json())
    .then(data => {
      console.log("✅ Vault Response:", data);
      sendResponse(data);
    })
    .catch(err => {
      console.error("❌ Save Error:", err);
      sendResponse({ status: "Error" });
    });

    return true;
  }

});
