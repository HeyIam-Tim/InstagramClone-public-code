console.log('user page works')
// Get url from the hidden input from html 
let userUrl = document.querySelector('#user_page').value;

// fetch API call
let colorTheme = (url) => {
  fetch(url, {
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(res => res.json())
  .then(data => {
    // Set localStorage with whatever style sheet is returned
    localStorage.setItem('mode', data.theme)
  })
}

colorTheme(userUrl)
