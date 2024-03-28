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

  if (data.scoringMethod) {
    const correctedJSON = data.scoringMethod.replace(/'/g, '"');
    try {
      const scoringMethodObject = JSON.parse(correctedJSON);
      console.log('Parsed Scoring Method Object:', scoringMethodObject); // Debugging output

      // Attempt to access the 'name' property
      const scoringMethodName = scoringMethodObject.total_points;
      console.log('Scoring Method Name:', scoringMethodName); // Debugging output

      if (scoringMethodName) {
        scoringMethodDisplay.innerText = `Scoring Method: ${scoringMethodName}`;
        scoringMethodDisplay.style.display = 'block';
      } else {
        // Handle the case where 'name' is undefined
        console.error('Name property is undefined in the parsed object:', scoringMethodObject);
        scoringMethodDisplay.innerText = 'Scoring Method: Name not found';
      }
    } catch (e) {
      console.error('Error parsing scoring method:', e);
    }
  }
})

  })
  .catch(error => {
    console.error('Error during confirmation:', error);
    spinner.style.display = 'none'; // Ensure spinner is hidden on error
  });


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