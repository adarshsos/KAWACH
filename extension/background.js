// Background service worker to make API calls to our Python backend
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "checkPhishing") {
    fetch('https://kawach-ey6v.onrender.com/api/phishing/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: request.url })
    })
    .then(response => response.json())
    .then(data => sendResponse(data))
    .catch(error => {
      console.error('Error checking URL:', error);
      sendResponse({ risk_score: 0, status: "Error connecting to KAWACH Backend" });
    });
    
    return true; 
  }
  
  if (request.action === "savePassword") {
    fetch('https://kawach-ey6v.onrender.com/api/vault', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request.data)
    })
    .then(response => response.json())
    .then(data => sendResponse(data))
    .catch(error => {
      console.error('Error saving password:', error);
      sendResponse({ status: "Error" });
    });
    
    return true;
  }
});

