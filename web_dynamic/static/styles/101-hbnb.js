$(document).ready(function () {
  let myAmenities = [];
  let myStates = [];
  let myCities = [];

  // Update amenities list when checkboxes are clicked
  $('.amenities .popover input[type=checkbox]').click(function () {
    const myListName = [];
    myAmenities = [];

    $('.amenities .popover input[type=checkbox]:checked').each(function () {
      myListName.unshift($(this).attr('data-name'));
      myAmenities.unshift($(this).attr('data-id'));
    });

    if (myListName.length === 0) {
      $('.amenities h4').html('&nbsp;');
    } else {
      $('.amenities h4').text(myListName.join(', '));
    }
    console.log(myAmenities);
  });

  // Update states list when checkboxes are clicked
  $('.locations .popover h2 input[type=checkbox]').click(function () {
    const myListName = [];
    myStates = [];

    $('.locations .popover h2 input[type=checkbox]:checked').each(function () {
      myListName.unshift($(this).attr('data-name'));
      myStates.unshift($(this).attr('data-id'));
    });

    if (myListName.length === 0) {
      $('.locations h6.myStates').html('&nbsp;');
    } else {
      $('.locations h6.myStates').text(myListName.join(', '));
    }
    console.log(myStates);
  });

  // Update cities list when checkboxes are clicked
  $('.locations .popover ul ul input[type=checkbox]').click(function () {
    const myListName = [];
    myCities = [];

    $('.locations .popover ul ul input[type=checkbox]:checked').each(function () {
      myListName.unshift($(this).attr('data-name'));
      myCities.unshift($(this).attr('data-id'));
    });

    if (myListName.length === 0) {
      $('.locations h6.myCities').html('&nbsp;');
    } else {
      $('.locations h6.myCities').text(myListName.join(', '));
    }
    console.log(myCities);
  });

  // Search button functionality
  $('.filters button').click(function (event) {
    event.preventDefault();

    $('.places').text('');

    const obj = {
      amenities: myAmenities,
      states: myStates,
      cities: myCities
    };

    listPlaces(JSON.stringify(obj));
  });

  // Check API status
  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/status/',
    type: 'GET',
    dataType: 'json',
    success: function (json) {
      $('#api_status').addClass('available');
    },
    error: function (xhr, status) {
      console.log('error ' + xhr);
    }
  });

  // Fetch and display places
  listPlaces();

  // Toggle reviews visibility
  $('#show-reviews').click(function () {
    const $this = $(this);
    const showReviews = $this.attr('data-show') === 'true';

    if (showReviews) {
      fetchReviews();
      $this.text('hide');
      $this.attr('data-show', 'false');
    } else {
      $('.places .reviews').remove();
      $this.text('show');
      $this.attr('data-show', 'true');
    }
  });
});

// Fetch and display reviews
function fetchReviews() {
  $.ajax({
    type: 'GET',
    url: 'http://0.0.0.0:5001/api/v1/reviews/',  // Adjust the URL as needed
    dataType: 'json',
    success: function (reviews) {
      const reviewsSection = $('<section class="reviews"></section>');
      reviews.forEach(review => {
        reviewsSection.append(`
          <article>
            <h3>${review.title}</h3>
            <p><strong>${review.user_name}:</strong> ${review.text}</p>
            <p><em>${new Date(review.date).toLocaleDateString()}</em></p>
          </article>
        `);
      });
      $('.places').append(reviewsSection);
    },
    error: function (xhr, status) {
      console.log('error ' + status);
    }
  });
}

// Fetch and display places
function listPlaces(consult = '{}') {
  console.log(consult);
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search',
    dataType: 'json',
    data: consult,
    contentType: 'application/json; charset=utf-8',
    success: function (places) {
      console.log(places);
      for (let i = 0; i < places.length; i++) {
        $('.places').append(`
          <article>
            <div class="title_box">
              <h2>${places[i].name}</h2>
              <div class="price_by_night">${places[i].price_by_night}</div>
            </div>
            <div class="information">
              <div class="max_guest">${places[i].max_guest}
                ${places[i].max_guest > 1 ? 'Guests' : 'Guest'}
              </div>
              <div class="number_rooms">${places[i].number_rooms}
                ${places[i].number_rooms > 1 ? 'Bedrooms' : 'Bedroom'}
              </div>
              <div class="number_bathrooms">${places[i].number_bathrooms}
                ${places[i].number_bathrooms > 1 ? 'Bathrooms' : 'Bathroom'}
              </div>
            </div>
            <div class="user"></div>
            <div class="description">
              ${places[i].description}
            </div>
          </article>
        `);
      }
    },
    error: function (xhr, status) {
      console.log('error ' + status);
    }
  });
}
