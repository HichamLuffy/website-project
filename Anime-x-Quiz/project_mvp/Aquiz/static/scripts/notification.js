document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message) {
        // Automatically close the message after 5 seconds
        setTimeout(function() {
            message.remove();
        }, 5000);
        
        // Close the message when the close button is clicked
        const closeButton = message.querySelector('.close');
        closeButton.addEventListener('click', function() {
            message.remove();
        });
    });
}); 
