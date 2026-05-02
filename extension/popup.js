document.addEventListener('DOMContentLoaded', () => {
  scanCurrentTab();
  
  document.getElementById('scan-btn').addEventListener('click', () => {
    scanCurrentTab();
  });
});

function scanCurrentTab() {
  const loadingDiv = document.getElementById('loading');
  const resultDiv = document.getElementById('result');
  const errorDiv = document.getElementById('error');
  
  loadingDiv.classList.remove('hidden');
  resultDiv.classList.add('hidden');
  errorDiv.classList.add('hidden');

  // Get current active tab
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs || !tabs[0]) {
      showError("Could not determine current tab.");
      return;
    }
    
    const currentUrl = tabs[0].url;
    
    // Send to background script
    chrome.runtime.sendMessage({ action: "checkPhishing", url: currentUrl }, (response) => {
      loadingDiv.classList.add('hidden');
      
      if (!response) {
        showError("Backend not responding. Is Flask running?");
        return;
      }
      
      if (response.error || response.status === "Error connecting to KAWACH Backend") {
        showError(response.error || response.status);
        return;
      }
      
      displayResult(response);
    });
  });
}

function displayResult(data) {
  const resultDiv = document.getElementById('result');
  const statusText = document.getElementById('status-text');
  const riskScore = document.getElementById('risk-score');
  const reasonsList = document.getElementById('reasons-list');
  
  resultDiv.classList.remove('hidden');
  
  statusText.textContent = data.status;
  riskScore.textContent = data.risk_score;
  
  // Color coding
  if (data.risk_score > 60) {
    statusText.style.color = '#ef4444'; // Red
    riskScore.style.color = '#ef4444';
  } else if (data.risk_score > 30) {
    statusText.style.color = '#f59e0b'; // Orange
    riskScore.style.color = '#f59e0b';
  } else {
    statusText.style.color = '#10b981'; // Green
    riskScore.style.color = '#10b981';
  }
  
  // Populate reasons
  reasonsList.innerHTML = '';
  if (data.reasons && data.reasons.length > 0) {
    data.reasons.forEach(reason => {
      const li = document.createElement('li');
      li.textContent = reason;
      reasonsList.appendChild(li);
    });
  } else {
    const li = document.createElement('li');
    li.textContent = "Passed all OWASP checks.";
    reasonsList.appendChild(li);
  }
}

function showError(msg) {
  document.getElementById('loading').classList.add('hidden');
  const errorDiv = document.getElementById('error');
  errorDiv.textContent = msg;
  errorDiv.classList.remove('hidden');
}
