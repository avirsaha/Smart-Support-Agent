const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const RASA_ENDPOINT = "https://e766-103-218-171-102.ngrok-free.app/webhooks/rest/webhook";

function appendMessage(content, sender = "user") {
  const wrapper = document.createElement("div");
  wrapper.classList.add("message", sender);

  const text = document.createElement("div");
  text.innerText = content;

  const timestamp = document.createElement("div");
  timestamp.classList.add("timestamp");

  // Set color based on sender
  if (sender === "user") {
    timestamp.style.color = "white";
  }

  timestamp.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  wrapper.appendChild(text);
  wrapper.appendChild(timestamp);

  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
  const typing = document.createElement("div");
  typing.classList.add("message", "bot", "typing");
  typing.id = "typing";
  typing.innerHTML = `
    Bot is typing<span class="typing-dots">
      <span></span><span></span><span></span>
    </span>
  `;
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
}
function removeTypingIndicator() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

sendBtn.addEventListener("click", async () => {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  userInput.value = "";

  showTypingIndicator();

  try {
    const res = await fetch(RASA_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender: "user", message }),
    });
    const data = await res.json();

    removeTypingIndicator();

    if (data.length === 0) {
      appendMessage("🤖 (No response)", "bot");
    } else {
      data.forEach((item) => {
        appendMessage(item.text || "(no text)", "bot");
      });
    }
  } catch (err) {
    removeTypingIndicator();
    appendMessage("❌ ERROR connecting to server!\n Bot maybe offline", "bot");
    console.error(err);
  }
});

// Send on Enter key
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendBtn.click();
});

const RASA_STATUS_ENDPOINT = "https://e766-103-218-171-102.ngrok-free.app/status";

async function checkRasaStatus() {
  const statusDiv = document.querySelector('.status');

  try {
    const response = await fetch(RASA_STATUS_ENDPOINT);
    if (response.ok) {
      statusDiv.textContent = 'Online';
      statusDiv.classList.add('online');
      statusDiv.classList.remove('offline');
    } else {
      statusDiv.textContent = 'Offline';
      statusDiv.classList.add('offline');
      statusDiv.classList.remove('online');
    }
  } catch {
    statusDiv.textContent = 'Offline';
    statusDiv.classList.add('offline');
    statusDiv.classList.remove('online');
  }
}

window.addEventListener("load", () => {
  checkRasaStatus();
  setInterval(checkRasaStatus, 30000);
});
window.addEventListener('DOMContentLoaded', () => {
  const chatBox = document.getElementById('chat-box');

  const startMsg = document.createElement('div');
  startMsg.className = 'bot-message start-message';
  startMsg.innerHTML = `
    <strong>👋 Welcome!</strong><br />
    You're chatting with a demo AI agent for a fictional e-commerce brand.<br /><br />
    This bot is part of my freelancing work — need a custom NLP bot for your business?<br /><br />
    👉 <a href="https://www.fiverr.com/yourprofile" target="_blank">Fiverr</a> | 
    <a href="https://www.upwork.com/freelancers/~yourprofile" target="_blank">Upwork</a><br />
    🔧 <a href="https://github.com/yourgithub" target="_blank">GitHub</a><br /><br />
    💬 Type a message to get started.
  ` 
  
  chatBox.appendChild(startMsg);
});

