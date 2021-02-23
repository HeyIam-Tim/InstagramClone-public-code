console.log('edit profile works')

// let mode = localStorage.getItem('mode')
// if mode == none


// Get Edit Profile url from the hidden input from edit_profile.html 
let editUrl = document.querySelector('#edit_profile').value;
// Get Csrf Token from edit_profile.html
let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
// Get Data from the hidden input from edit_profile.html 
let user_id = document.querySelector('#user_id').value;

// fetch call to backend, sending data to backend, receiving messaged data back, setting Local Storage, setting Color Theme to an appropriate one
let switchMode = (url, token, user_id) => {
  fetch(editUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    body: JSON.stringify({'user': user_id})
  })
  .then(res => res.json())
  .then(data => {
    // Set localStorage with whatever style sheet is returned
    localStorage.setItem('mode', data.theme)
    // setting href to one that fetch returns back from view
    document.querySelector('#swap_theme_css').href = data.theme
  })
}


document.querySelector('#switch_theme').addEventListener('click', () => {
  switchMode(editUrl, csrf_token, user_id)
})