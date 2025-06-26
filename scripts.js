const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const RASA_ENDPOINT = "https://7e40-103-218-171-102.ngrok-free.app/webhooks/rest/webhook";

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
     wrapper.classList.add("pending-reply");
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
      // Remove glow from last pending user message
const pendingMessages = document.querySelectorAll('.message.user.pending-reply');
if (pendingMessages.length) {
  pendingMessages[pendingMessages.length - 1].classList.remove('pending-reply');
}
    }
  } catch (err) {
    removeTypingIndicator();
    appendMessage(`⚠️ ERROR:
    Agent temporarily unavailable. This may be due to server downtime, network or tunnel interruption, or the agent undergoing maintenance. Please try again later.

    If the issue persists for an unusually long time or you'd like to report a bug, feel free to contact me via the email provided above.`, "bot");
    }
    console.error(err);
});

// Send on Enter key
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendBtn.click();
});

const RASA_STATUS_ENDPOINT = "https://7e40-103-218-171-102.ngrok-free.app/status";

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
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<h1 style="margin: 0 0 10px 0; font-size: 30px; text-align: left;"><strong>👋 Welcome!</strong></h1>
This is a demo AI agent for a fictional e-commerce brand.<br><br>

📂 Features & custom options: <a href="https://github.com/avirsaha/smart-agent/" target="_blank">GitHub</a><br>
🤖 Works with WhatsApp, Insta, Telegram, Slack, Discord & more.<br>
💻 Easy to integrate into any site or app.<br><br>
📧 <a href="mailto:aviraj.saha@outlook.com">aviraj.saha@outlook.com</a><br>
📞 <a href="tel:+918335827412">+91 83358 27412</a><br><br>
📢 Follow me on: 
<br>
<a href="https://x.com/lemorymeak" target="_blank" style="margin-right: 10px;">
  <i class="fab fa-x-twitter"> </i>
</a>
<a href="https://linkedin.com/in/aviraj-saha-ai" target="_blank" style="margin-right: 10px;">
  <i class="fab fa-linkedin"> </i>
</a>
<a href="https://github.com/avirsaha" target="_blank">
  <i class="fab fa-github"></i>
</a>
<br><br>
💬 Type a message to get started.

` 
/*
<h1 style="margin: 0 0 10px 0; font-size: 30px; text-align: left;"><strong>👋 Welcome!</strong></h1>
This is a demo AI agent for a fictional e-commerce brand.<br><br>

Need a AI chatbot like this for your business?<br>
Hire me on 👉 <a href="" target="_blank">Fiverr</a> | <a href="" target="_blank">Upwork</a><br><br>

📂 Features & custom options: <a href="https://github.com/avirsaha/smart-agent/" target="_blank">GitHub</a><br>
🤖 Works with WhatsApp, Insta, Telegram, Slack, Discord & more.<br>
💻 Easy to integrate into any site or app.<br><br>
📧 <a href="mailto:aviraj.saha@outlook.com">aviraj.saha@outlook.com</a><br>
📞 <a href="tel:+918335827412">+91 83358 27412</a><br><br>
💬 Type a message to get started.
*/
  chatBox.appendChild(startMsg);
});

// Scroll to latest chat button logic
const scrollButton = document.getElementById("scroll-to-latest");

// Toggle button visibility when user scrolls up
chatBox.addEventListener("scroll", () => {
  const nearBottom = chatBox.scrollHeight - chatBox.scrollTop <= chatBox.clientHeight + 20;
  scrollButton.style.display = nearBottom ? "none" : "block";
});

// Scroll to bottom when clicked
scrollButton.addEventListener("click", () => {
  chatBox.scrollTop = chatBox.scrollHeight;
});

