document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
  loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
          const response = await fetch('http://votre-api-url/login', {
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
              alert('Échec de la connexion : ' + errorData.message);
          }
      } catch (error) {
          console.error('Erreur lors de la connexion:', error);
          alert('Une erreur est survenue lors de la tentative de connexion.');
      }
  });
  }
});
