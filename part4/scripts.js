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


//Check user authentication
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
  }
}
function getCookie(cookie_name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${cookie_name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


// cards-loader
document.addEventListener('DOMContentLoaded', function () {
  fetch('./static/cards-index.html')
    .then(response => response.text())
    .then(data => {
      // Create a DOM object from the received text
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, 'text/html');

      // Find the content with the class 'place-card'
      const placeCards = doc.querySelectorAll('.place-card');

      // Log the number of cards found
      console.log('Number of place cards found:', placeCards.length);

      // Get the section where the cards will be inserted
      const placesListSection = document.querySelector('#places-list');

      // Clear existing content if needed
      placesListSection.innerHTML = '';

      // Insert each place card into the #places-list section
      placeCards.forEach(card => {
        placesListSection.appendChild(card);
      });
    })
    .catch(error => console.error('Error loading cards:', error));
});


//Fetch places data
async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function
}


//Populate places list
function displayPlaces(places) {
  // Clear the current content of the places list
  // Iterate over the places data
  // For each place, create a div element and set its content
  // Append the created element to the places list
}


//Implement client-side filtering
document.getElementById('price-filter').addEventListener('change', (event) => {
  // Get the selected price value
  // Iterate over the places and show/hide them based on the selected price
});
