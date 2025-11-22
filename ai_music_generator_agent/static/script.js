const messagesContainer = document.getElementById('messages');
const promptInput = document.getElementById('promptInput');
const sendBtn = document.getElementById('sendBtn');

function addMessage(text, sender, isHtml = false) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}`;

  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'avatar';
  avatarDiv.innerHTML = sender === 'agent' ? '<i class="fa-solid fa-robot"></i>' : '<i class="fa-solid fa-user"></i>';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'content';
  if (isHtml) {
    contentDiv.innerHTML = text;
  } else {
    contentDiv.textContent = text;
  }

  messageDiv.appendChild(avatarDiv);
  messageDiv.appendChild(contentDiv);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addLoading() {
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'message agent loading-msg';
  loadingDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="content">
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
  messagesContainer.appendChild(loadingDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  return loadingDiv;
}

async function generateMusic(prompt) {
  const loadingMsg = addLoading();
  sendBtn.disabled = true;
  promptInput.disabled = true;

  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to generate music');
    }

    const data = await response.json();
    loadingMsg.remove();

    const resultHtml = `
            <p>${data.message}</p>
            <div class="audio-card">
                <audio controls>
                    <source src="${data.audio_url}" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
                <a href="${data.audio_url}" download="generated_music.wav" class="download-btn">
                    <i class="fa-solid fa-download"></i> Download
                </a>
            </div>
        `;
    addMessage(resultHtml, 'agent', true);

  } catch (error) {
    loadingMsg.remove();
    addMessage(`Error: ${error.message}`, 'agent');
    console.error(error);
  } finally {
    sendBtn.disabled = false;
    promptInput.disabled = false;
    promptInput.focus();
  }
}

sendBtn.addEventListener('click', () => {
  const prompt = promptInput.value.trim();
  if (prompt) {
    addMessage(prompt, 'user');
    promptInput.value = '';
    generateMusic(prompt);
  }
});

promptInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendBtn.click();
  }
});
