document.addEventListener('DOMContentLoaded', function() {
  setupFetchOperation();
});

document.getElementById('reload-button').addEventListener('click', function() {
  setupFetchOperation();
});

function setupFetchOperation() {
  const spinner = document.querySelector('.loading-circle');
  const scoringMethodDisplay = document.getElementById('scoring-method-display');
  const confirmationContainer = document.getElementById('confirmation-container');

  spinner.classList.add('show');
  hideNextButton();

  fetch('/confirm', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log('Confirmation processed:', data);

    spinner.classList.remove('show');

    if (data.scoringMethod) {
      scoringMethodDisplay.innerText = 'Successfully created Scoring Method for provided job description';
      scoringMethodDisplay.classList.add('success');
      showNextButton(confirmationContainer);
    } else {
      scoringMethodDisplay.innerText = 'Scoring Method data not found';
      scoringMethodDisplay.classList.add('error');
    }
  })
  .catch(error => {
    console.error('Error during confirmation:', error);
    spinner.classList.remove('show');
    scoringMethodDisplay.innerText = 'Error in fetching Scoring Method data';
    scoringMethodDisplay.classList.add('error');
  });
}

function showNextButton(container) {
  if (!document.getElementById('next-button')) {
    const nextButton = document.createElement('button');
    nextButton.id = 'next-button';
    nextButton.innerText = 'Next';
    nextButton.title = 'Go to the next step';
    nextButton.classList.add('next-button');

    nextButton.addEventListener('click', function() {
      console.log('Next button clicked');
      fetch('/trigger-scrap', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          console.log(data.message);
      })
      .catch((error) => {
          console.error('Error:', error);
      });
    });

    container.appendChild(nextButton);
  }
}

function hideNextButton() {
  const nextButton = document.getElementById('next-button');
  if (nextButton) {
    nextButton.remove();
  }
}

// Assuming the second part of your code does not need to change for this specific issue
document.getElementById('reload-button').addEventListener('click', function() {
  fetch('/confirm', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
  })
  .then(response => response.json())
  .then(data => {
      console.log('Confirmation processed:', data);
      // Similar handling as above might be needed here
  })
  .catch((error) => {
      console.error('Error:', error);
  });
});
document.getElementById('reload-button').addEventListener('click', function() {
    fetch('/confirm', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // No need to send chathistory as it's maintained on the server
    })
    .then(response => response.json())
    .then(data => {
        console.log('Confirmation processed:', data);
        // Process the response here, e.g., display a message to the user
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});