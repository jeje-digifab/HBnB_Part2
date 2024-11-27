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
          const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
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

// Check user authentication
function checkAuthentication() {
  const token = getCookie('token');
  return token ? token : null;
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
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, 'text/html');
      const placeCards = doc.querySelectorAll('.place-card');
      console.log('Number of place cards found:', placeCards.length);
      const placesListSection = document.querySelector('#places-list');
      placesListSection.innerHTML = '';
      placeCards.forEach(card => {
        placesListSection.appendChild(card);
      });
    })
    .catch(error => console.error('Error loading cards:', error));
});

// Change rating note in stars
const ratingLinks = document.querySelectorAll('.rating a');
ratingLinks.forEach(link => {
  link.addEventListener('click', function (event) {
    event.preventDefault();
    const ratingValue = this.getAttribute('href').substring(1);
    console.log(`${ratingValue} stars!`);
  });
});

// Get placeID from URL
function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

// Fetch place details
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }
    const data = await response.json();
    displayPlaceDetails(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

// Display place details
function displayPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  detailsSection.innerHTML = `
    <h1>${place.name}</h1>
    <p><strong>Host:</strong> ${place.host}</p>
    <p><strong>Price per night:</strong> $${place.price}</p>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
  `;

  const reviewsSection = document.getElementById('reviews');
  reviewsSection.innerHTML = '<h2>Reviews:</h2>';
  place.reviews.forEach(review => {
    reviewsSection.innerHTML += `
      <div class="review-card">
        <p><strong>${review.user}:</strong> "${review.text}" Rating: ${review.rating}/5</p>
      </div>
    `;
  });
}

// Event listener for review form submission
document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (placeId) {
    if (token) {
      fetchPlaceDetails(token, placeId);
      if (reviewForm) {
        reviewForm.style.display = 'block';
      }
    } else {
      console.log('User is not authenticated');
      if (reviewForm) {
        reviewForm.style.display = 'none';
      }
    }
  } else {
    console.error('No place ID found in URL');
  }

  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (token && placeId) {
        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;
        await submitReview(token, placeId, reviewText, rating);
      } else {
        alert('You must be logged in to submit a review');
      }
    });
  }
});

// Fetch API to submit review
async function submitReview(token, placeId, reviewText, rating) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ text: reviewText, rating: parseInt(rating) })
    });
    if (response.ok) {
      alert('Review submitted successfully!');
      fetchPlaceDetails(token, placeId); // Refresh place details
    } else {
      alert('Failed to submit review');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while submitting the review');
  }
}

// Implement client-side filtering
document.getElementById('price-filter').addEventListener('change', (event) => {
  // Get the selected price value
  // Iterate over the places and show/hide them based on the selected price
});