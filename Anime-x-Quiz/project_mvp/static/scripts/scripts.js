$(document).ready(function() {
    $('.category').click(function(e) {
        e.preventDefault();
        var category = $(this).data('category');
        $('#quiz-category-heading').text('Choose a Quiz Level for "' + category.replace(/-/g, ' ') + '"');
        $('#quiz-levels').addClass('show');
        // Pass selected category to backend or perform other actions
    });

    $('.level').click(function(e) {
        e.preventDefault();
        var level = $(this).data('level');
        $('#doneButton').addClass('show');
        // Pass selected level to backend or perform other actions
    });
});
