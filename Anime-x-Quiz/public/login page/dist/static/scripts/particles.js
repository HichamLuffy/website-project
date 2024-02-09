$(document).ready(function () {
  // Function to add snow
function addSnow () {
    const snowflake = '<div class="snow"></div>';
    $('body').append(snowflake);
}

  // Function to delete snow
function deleteSnow () {
    $('.snow:last').remove();
}

  // Function to clear snow
function clearSnow () {
    $('.snow').remove();
}

  // Add snow on button click
$('.add-snow').click(function () {
    addSnow();
});

  // Delete snow on button click
$('.delete-snow').click(function () {
    deleteSnow();
});

  // Clear snow on button click
$('.clear-snow').click(function () {
    clearSnow();
});
});
