 document.querySelector('form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission

  // Get the entered username and password
  var username = document.querySelector('input[name="uname"]').value;
  var password = document.querySelector('input[name="psw"]').value;

  // Perform your login validation here
  // Replace the condition below with your actual validation logic
  if ((username === 'moss' && password === 'password') || (username === 'deepak' && password === 'password')){
    // Redirect to second.html
    window.location.href = '/configure';
  } else {
    alert('Invalid credentials. Please try again.');
  }
});


// login.js
