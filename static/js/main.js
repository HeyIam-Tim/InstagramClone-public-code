console.log('main works')

// 
// Switching Color Theme
// 

// Get Style Sheet From LocalStorage and Put It Into #swap_theme_css's Href
let colorMode = localStorage.getItem('mode');
document.querySelector('#swap_theme_css').href = colorMode;