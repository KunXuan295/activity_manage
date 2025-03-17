// static/js/add_event.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-event-form');

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Blocking default form submission behavior

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value // 添加 CSRF 令牌
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message); // Pop-up Success Alert
                    window.location.href = eventsListUrl; // Jump to the event listing page
                } else {
                    alert('Failed to create event: ' + data.message); // pop-up error message
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting the form.');
            });
        });
    }
});