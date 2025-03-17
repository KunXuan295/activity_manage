// static/js/comments.js

document.addEventListener('DOMContentLoaded', function() {
    const commentButton = document.getElementById('comment-button');
    const commentInput = document.getElementById('comment-input');
    const commentList = document.getElementById('comment-list');

    if (commentButton && commentInput && commentList) {
        commentButton.addEventListener('click', function() {
            const commentText = commentInput.value.trim();

            if (commentText) {
                
                const url = `/event/${eventId}/add_comment/`;

                
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}' 
                    },
                    body: JSON.stringify({
                        content: commentText
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        
                        const newComment = document.createElement('div');
                        newComment.className = 'mb-3 border-bottom pb-3';

                        const commentContent = `
                            <div class="d-flex justify-content-between">
                                <div>
                                    <p class="mb-1"><strong>${data.username}:</strong> ${data.content}</p>
                                </div>
                                <div>
                                    <p class="mb-0 text-muted">${data.created_at}</p>
                                </div>
                            </div>
                        `;

                        newComment.innerHTML = commentContent;
                        commentList.prepend(newComment); 
                        commentInput.value = ''; 
                    } else {
                        alert('Failed to add comment: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    }
});