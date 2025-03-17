document.addEventListener("DOMContentLoaded", function () {
    const rejectButton = document.getElementById("reject-button");

    if (rejectButton) {
        rejectButton.addEventListener("click", function () {
            if (!eventId || !rejectUrl || !csrfToken) {
                console.error("Error: Missing eventId, rejectUrl, or csrfToken.");
                return;
            }

            if (confirm("Are you sure you want to block this activity?？")) {
                fetch(rejectUrl, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "Content-Type": "application/json",
                    },
                })
                .then(response => {
                    if (response.ok) {
                        alert("Activity has been blocked");
                        window.location.href = "/admin_home/events/";  
                    } else {
                        alert("Operation failed, please try again");
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("An error has occurred. Please try again later.");
                });
            }
        });
    }
});
