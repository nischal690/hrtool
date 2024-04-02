document.addEventListener('DOMContentLoaded', function() {
  const platformSelect = document.getElementById('platform-select');

  if (platformSelect) { // Check if the element was found
      platformSelect.addEventListener('change', function() {
          console.log("Dropdown value changed to:", this.value); // Log the selected value

          var value = this.value;
          var fileUpload = document.getElementById('file-upload');
          var uploadBtn = document.getElementById('upload-btn'); // Get the upload button
          var resdexCredentials = document.getElementById('resdex-credentials');

          // Hide all fields initially
          fileUpload.classList.add('hidden');
          uploadBtn.classList.add('hidden'); // Ensure the upload button is also hidden initially
          resdexCredentials.classList.add('hidden');

          // Show the file input and upload button if 'manual' option is selected
          if (value === 'manual') {
              fileUpload.classList.remove('hidden');
              uploadBtn.classList.remove('hidden'); // Show the upload button for manual file upload
          } 
          // Show Resdex credentials input if 'naukri' option is selected
          else if (value === 'naukri') {
              resdexCredentials.classList.remove('hidden');
          }
      });
  } else {
      console.error("Error: 'platform-select' element not found"); // Log if the element is missing
  }
});
