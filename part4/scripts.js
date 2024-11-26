// nav-loader
document.addEventListener('DOMContentLoaded', function () {
  fetch('static/element.html')
    .then(response => response.text())
    .then(data => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, 'text/html');
      document.querySelector('nav').innerHTML = doc.querySelector('nav').innerHTML;
    })
    .catch(error => console.error('Nav loading error:', error));
});


// footer-loader
document.addEventListener('DOMContentLoaded', function () {
  fetch('static/element.html')
    .then(response => response.text())
    .then(data => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, 'text/html');
      document.querySelector('footer').innerHTML = doc.querySelector('footer').innerHTML;
    })
    .catch(error => console.error('Footer loading error:', error));
});


// login-loader
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
  loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {  // modify fetch url if necessary
          const response = await fetch('http://localhost:5000/api/v1/auth/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ email, password })
          });

          if (response.ok) {
              const data = await response.json();
              document.cookie = `token=${data.access_token}; path=/; max-age=3600; SameSite=Strict`;
              window.location.href = 'index.html';
          } else {
              const errorData = await response.json();
              alert('Login failed : ' + (errorData.message || response.statusText));
          }
      } catch (error) {
          console.error('Login failed:', error);
          alert('An error occurred while logging in');
      }
  });
  }
});


