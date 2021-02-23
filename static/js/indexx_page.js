console.log('index works')

// 
// Like Handler
// 

// Set And Get Heart-looking Icons From LocalStorage
localStorage.setItem('like_icon', 'https://timbucketaws.s3.amazonaws.com/static/images/likeheart.png')
const likeIcon = localStorage.getItem('like_icon');

localStorage.setItem('unlike_icon', 'https://timbucketaws.s3.amazonaws.com/static/images/hearticonunlike.png')
const unlikeIcon = localStorage.getItem('unlike_icon');

// Get Index Url from index.html
let indexUrl = document.querySelector('#index_url').value;

// Wrapper of Heart-looking icons, Number of likes and Wheather User liked Publication or Not
let likeUnlikeWrapper = document.querySelectorAll('#like_unlike_icon_wrapper');

// For each Wrapper in each Publication
for (let i=0; likeUnlikeWrapper.length > i; i++){
  likeUnlikeIcon(likeUnlikeWrapper[i])

  // Ajax Handler
  likeUnlikeWrapper[i].addEventListener('click', function(){
    let like_image = this.children[2];
    let num_likes = this.children[3];
    $.ajax({
      type: 'post',
      url: indexUrl,
      data: {
        csrfmiddlewaretoken:this.children[0].getAttribute("value"),
        publication_id:this.children[1].getAttribute("value")
      },
      success:function(response){
        if (response.pub_liked.liked.includes(response.user_id)){
          like_image.src = likeIcon;
        }
        else{
          like_image.src = unlikeIcon;
        }
        // Pluralize Handler
        if (response.likes_number <= 1)
          num_likes.innerText = response.likes_number + ' like';
        else 
          num_likes.innerText = response.likes_number + ' likes';
      }
    });
  })
}

// Set 'Unlike' Icon initially and Set 'Like' Icon if User liked Publication
function likeUnlikeIcon(heartIcon){
  if(heartIcon.children[2].src = null){
    heartIcon.children[2].src = unlikeIcon;
  }
  let userId = heartIcon.children[4].getAttribute("value");
  let likedArray = heartIcon.children[5].getAttribute("value");
  if (likedArray.includes(userId)){
    heartIcon.children[2].src = likeIcon;
  }
  else{
    heartIcon.children[2].src = unlikeIcon;
  }
}


// 
// Comment Handler
// 

console.log('Comment works')

// Grab all 'add new comment' forms from each publication 
let commentForm = document.querySelectorAll('.comment');

// CSRF token
let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

// Url for fetching
let url = document.querySelector('#index_url').value;

// Grab all publications' ids 
let publication_ids = document.querySelectorAll('#publication_id');

// All comment containers from each publication
let all_comments_con = document.querySelectorAll('.comments_con');


// Comment Functionality
let commentHandler = (publication_ids, all_comments_con) => {

  // Loop through all 'add new comment' forms
  for (let i = 0; commentForm.length > i; i++) {

    // Comment Button gets clicked
    commentForm[i].children[1].addEventListener('click', () => {

      // Publication Id for a current 'add new comment' form
      publ_id = publication_ids[i].value;

      // Comment Container for a current 'add new comment' form
      comments_con = all_comments_con[i]

      // Comment Body
      comment_text = commentForm[i].children[0].value

      // Current iteration of 'add new comment' forms
      comForm = commentForm[i]

      // Fetch API Call
      commentHandlerFetch(csrf_token, comment_text, publ_id, comments_con, comForm)

    })
  }
}


// Fetching Data
let commentHandlerFetch = (csrf_token, comment_text, publ_id, comments_con, comForm) => {
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    body: JSON.stringify({'comment_text': comment_text, 'id_publication':publ_id}),
  })
  .then(res => res.json())
  .then(data => {
    console.log('datadata', data)

    let three_comments = '';

    for ( let i = 0; data.length > i; i++ ) {
      // Display Author and Body for each comment
      comment = `

        <div class="comments">
          <span id="author_comm" class="u_fullname">${data[i].author}</span>
          <span id="body_comm">${data[i].body}</span>
        </div>
      
      `
      // Collecting Comments
      three_comments += comment
    }

    // Display last 3 comments on the page
    comments_con.innerHTML = three_comments

    // Reset Form
    comForm.reset()
  })
}


commentHandler(publication_ids, all_comments_con)