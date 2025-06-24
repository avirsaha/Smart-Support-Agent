const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook";

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

