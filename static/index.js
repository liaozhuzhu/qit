function like(postId) {
  const likeCount = document.getElementById(`likes-count-${postId}`);
  const likeButton = document.getElementById(`like-button-${postId}`);
  
  fetch(`/like/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.className = "fa-solid fa-heart";
      } else {
        likeButton.className = "fa-regular fa-heart";
      }
    })
    .catch((e) => alert("Could not like post"));
}

let commentsShowing = false;
function commentToggle(postId) {
  const commentDiv = document.getElementById(`comments-${postId}`);
  if (commentsShowing == false) {
    commentDiv.style.display = "block";
    commentsShowing = true;
  }
  else {
    commentDiv.style.display = "none";
    commentsShowing = false;
  }
}

// function deleteComment(commentId) {
//   const commentDeleteBtn = document.getElementById(`comment-delete-button-${commentId}`);
//   const commentToDelete = document.getElementById(`comments-delete-${commentId}`);
//   console.log("before", commentToDelete);
//   fetch(`/delete-comment/${commentId}`, { method: "POST" })
//   .then((res) => res.json())
//   .then((data) => {
//     if (data["deleted"]) {
//       commentToDelete.style.display = "none";
//     }
//     else {
//       return console.log("returned");
//     }
//   }).catch((e) => alert("Could Not Delete Comment"));
// }