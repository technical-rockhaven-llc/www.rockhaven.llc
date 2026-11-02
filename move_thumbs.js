// Move the #albums thumbnails into the side-by-side layout
document.addEventListener('DOMContentLoaded', function() {
  const albumsDiv = document.getElementById('albums');
  const placeholder = document.querySelector('.rh-thumbs-placeholder');

  if (albumsDiv && placeholder) {
    // Move the albums div into the placeholder
    placeholder.appendChild(albumsDiv);
  }
});
