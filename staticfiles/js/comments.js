document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Add new comment to the list
                    const commentsList = document.getElementById('comments-list');
                    const newComment = `
                        <div class="comment card mb-3">
                            <div class="card-body">
                                <p class="card-text">${data.comment.content}</p>
                                <small class="text-muted">
                                    By ${data.comment.author} on ${data.comment.created_at}
                                </small>
                            </div>
                        </div>
                    `;
                    commentsList.insertAdjacentHTML('afterbegin', newComment);
                    commentForm.reset();
                }
            });
        });
    }
});