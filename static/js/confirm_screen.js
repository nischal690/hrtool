document.addEventListener('DOMContentLoaded', function() {
    const spinner = document.querySelector('.loading-circle');
    const scoringMethodDisplay = document.getElementById('scoring-method-display');
  
    spinner.style.display = 'block';
  
    fetch('/confirm', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log('Confirmation processed:', data);
      spinner.style.display = 'none'; // Hide spinner upon success
  
      if (data.scoring_method) {
        scoringMethodDisplay.innerText = `Scoring Method: ${data.scoring_method}`;
        scoringMethodDisplay.style.display = 'block'; // Show the scoring method
      }
    })
    .catch(error => {
      console.error('Error during confirmation:', error);
      spinner.style.display = 'none'; // Ensure spinner is hidden on error
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