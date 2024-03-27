const chatBody = document.getElementById('chat-body');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const confirmBtn = document.getElementById('confirm-btn'); // Assuming you've added this button in your HTML
const jdActionDropdown = document.getElementById('jd-action');

function showInPopup(message) {
  const popupElement = document.createElement('div');
  popupElement.style.position = 'fixed';
  popupElement.style.top = '0';
  popupElement.style.left = '0';
  popupElement.style.width = '60%'; // Set width to 60% of the viewport
  popupElement.style.height = '100%'; // Take full height of the viewport
  popupElement.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
  popupElement.style.color = 'white';
  popupElement.style.display = 'flex';
  popupElement.style.flexDirection = 'column'; // Stack children vertically
  popupElement.style.justifyContent = 'center'; // Center content vertically
  popupElement.style.alignItems = 'flex-start'; // Align content to the left
  popupElement.style.padding = '20px';
  popupElement.style.zIndex = '1000';
  popupElement.style.cursor = 'pointer';
  popupElement.style.overflowY = 'auto'; // Enable scrolling for long content
  popupElement.innerText = message;

  // Close the popup when clicked
  popupElement.onclick = function() {
    document.body.removeChild(popupElement);
  };

  document.body.appendChild(popupElement);
}



function appendMessage(message, sender) {
  const messageElement = document.createElement('div');
  messageElement.classList.add(sender === 'user' ? 'user-message' : 'ai-message');
  
  // Create a span to hold the message text
  const messageText = document.createElement('span');
  messageText.innerText = message;

  // Create a button for showing the message in a popup
  const showButton = document.createElement('button');
  showButton.innerText = 'Show';
  showButton.classList.add('show-button'); // Apply the CSS class for styling
  showButton.onclick = function() {
    showInPopup(message);
  };

  // Append the text and button to the message element
  messageElement.appendChild(messageText);
  messageElement.appendChild(showButton);

  chatBody.appendChild(messageElement);
  chatBody.scrollTop = chatBody.scrollHeight;
  console.log(`Appended ${sender} message:`, message);
}



function toggleConfirmButton() {
  const message = userInput.value.trim().toUpperCase();
  if (message === 'CONFIRM') {
    sendBtn.style.display = 'none';
    confirmBtn.style.display = ''; // Show the confirm button
  } else {
    sendBtn.style.display = ''; // Show the send button
    confirmBtn.style.display = 'none'; // Hide the confirm button
  }
}

function sendMessage() {
  const message = userInput.value.trim();
  const selectedAction = jdActionDropdown.value;

  console.log('Sending message:', message, 'with action:', selectedAction);

  if (message !== '') {
    appendMessage(message, 'user');
    userInput.value = '';
    toggleConfirmButton(); // Call to reset the button display after sending

    fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        action: selectedAction
      })
    })
    .then(response => {
      console.log('HTTP Response status:', response.status);
      return response.json();
    })
    .then(data => {
      console.log('Received data:', data);
      if (data && data.data) {
          appendMessage(data.data, 'ai');
      } else {
          console.error('Unexpected response structure:', data);
          appendMessage('Sorry, something went wrong.', 'ai');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      appendMessage('Sorry, something went wrong.', 'ai');
    });
  }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('input', toggleConfirmButton); // Listen for input changes to toggle the Confirm button

userInput.addEventListener('keyup', (event) => {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

confirmBtn.addEventListener('click', function() {
  window.location.href = '/confirm-screen';
});


