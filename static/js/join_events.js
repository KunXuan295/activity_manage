document.addEventListener("DOMContentLoaded", function () {
    const joinButton = document.getElementById("join-button");
    if (joinButton) {
        joinButton.addEventListener("click", function () {
            const eventEndTime = new Date(joinButton.getAttribute("data-end-time"));
            const currentTime = new Date();

            if (currentTime > eventEndTime) {
                alert("This event has expired.");
                return;
            }

            fetch(joinButton.getAttribute("data-url"), {
                method: "POST",
                headers: {
                    "X-CSRFToken": joinButton.getAttribute("data-csrf"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("You have successfully joined this event!");
                    window.location.reload();
                } else {
                    alert(data.message);
                }
            });
        });
    }
});
