
const rasaEndpoint = "https://your-ngrok-or-server-url/webhooks/rest/webhook";

document.getElementById('chat-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const inputField = document.getElementById('user-input');
  const message = inputField.value.trim();
  if (!message) return;

  appendMessage(message, 'user');
  inputField.value = '';
  scrollToBottom();

  try {
    const response = await fetch(rasaEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sender: 'demo-user',
        message: message
      })
    });

    const data = await response.json();
    if (data && data.length > 0) {
      data.forEach(msg => {
        if (msg.text) appendMessage(msg.text, 'bot');
      });
    } else {
      appendMessage("Sorry, I didn't get that.", 'bot');
    }
  } catch (error) {
    appendMessage("Error contacting the server.", 'bot');
    console.error(error);
  }

  scrollToBottom();
});

function appendMessage(text, sender) {
  const messageEl = document.createElement('div');
  messageEl.className = `message ${sender}`;
  messageEl.innerText = text;
  document.getElementById('chat-window').appendChild(messageEl);
}

function scrollToBottom() {
  const chatWindow = document.getElementById('chat-window');
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
