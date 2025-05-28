document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.querySelector('form');
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const reviewText = reviewForm.querySelector('textarea[name="review_text"]').value.trim();
    if (!reviewText) {
      alert("Review cannot be empty!");
      return;
    }

    const bookId = window.location.pathname.split('/').pop();

    try {
      const response = await fetch(`/add_review/${bookId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ review_text: reviewText }),
      });

      if (response.redirected) {
        window.location.href = response.url; // Redirect if Flask sends a redirect
      } else if (response.ok) {
        // Append review to list without reload
        const reviewList = document.querySelector('.review-list');
        const newReview = document.createElement('li');
        newReview.textContent = reviewText;
        reviewList.prepend(newReview);
        reviewForm.reset();
      } else {
        const error = await response.text();
        alert('Error: ' + error);
      }
    } catch (err) {
      alert('Failed to submit review');
      console.error(err);
    }
  });
});
