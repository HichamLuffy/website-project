$(document).ready(function() {
    $('#edit-profile-link').click(function(event) {
        event.preventDefault();
        $('#profile-details').toggle();
        $('#edit-profile-div').toggle();
    
        if ($('#edit-profile-div').is(':visible')) {
            $('profile-details').hide();
            // Populate the edit fields with current user's details
            // Assuming this is the ID of your update button
        }
    });
});