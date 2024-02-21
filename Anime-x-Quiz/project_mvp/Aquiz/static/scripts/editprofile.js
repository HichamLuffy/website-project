$(document).ready(function() {
    $('#edit-profile-link').click(function(event) {
        event.preventDefault();
        $('#edit-profile-div').toggle();
    
        if ($('#edit-profile-div').is(':visible')) {
            // Populate the edit fields with current user's details
            $('#username-edit').val('{{ current_user.username }}');
            $('#email-edit').val('{{ current_user.email }}');
        // Show the edit fields
        $('#username-edit').show();
        $('#email-edit').show();
        } else {
        // Hide the edit fields if the edit profile div is hidden
        $('#username-edit').hide();
        $('#email-edit').hide();
    }
    });
});