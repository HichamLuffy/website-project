$(document).ready(function() {
    // Function to update the background gradient
    function updateGradient() {
        const deg = $('#degRange').val();
        const color = $('#colorPicker').val();
        const percentage = $('#percentageRange').val();
        const gradient = `linear-gradient(${deg}deg, rgba(2,0,36,1) 0%, ${color} 0%, rgba(0,0,0,1) ${percentage}%)`;
        const gradient2 = `linear-gradient(${deg}deg, rgba(2,0,36,1) 0%, ${color} 0%, rgba(0,0,0,1) 100%)`;
        const followbackground = `linear-gradient(to top, rgba(2,0,36,1) 0%, rgba(${color}, 0.5) 0%, rgba(0,0,0,1) 100%);`
        const bordercolor = `5px solid ${color};`
        $('.container').css('background', gradient);
        $('.gradient-controls input[type="range"]').css('background', color);
        $('.gradient-overlay').css('background', gradient2);
        $('body').css('--sb-thumb-color', color);
        $('.modal-content').css('background-color', color);
        $('.user-detail').css('background', color);
        $('.create-quiz-button a').css('background-color', color);
        $('.delete-quiz-btn').css('background-color', color);
        $('.quiz-container').css('border', bordercolor);
        // Save the background gradient to localStorage
        localStorage.setItem('backgroundGradient', gradient);
        // Save the theme color to localStorage
        localStorage.setItem('themeColor', color);
        localStorage.setItem('imageGradient', gradient2)
        localStorage.setItem('bordertheme', bordercolor)
    };

    // Function to restore the background gradient and theme color from localStorage
    function restoreSettings() {
        const savedGradient = localStorage.getItem('backgroundGradient');
        const savedColor = localStorage.getItem('themeColor');
        const savedimg = localStorage.getItem('imageGradient');
        const borderthem = localStorage.getItem('bordertheme');
        if (savedGradient && savedColor && savedimg) {
            $('.container').css('background', savedGradient);
            $('#colorPicker').val(savedColor);
            $('#colorPicker').trigger('change'); // Trigger change event to update gradient
            $('.gradient-overlay').css('background', savedimg);
            $('body').css('--sb-thumb-color', savedColor);
            $('.user-detail').css('background', savedColor);
            $('.modal-content').css('background-color', savedColor);
            $('.create-quiz-button a').css('background-color', savedColor);
            $('.delete-quiz-btn').css('background-color', savedColor);
            $('.quiz-container').css('border', borderthem);
        }
    }

    // Restore the background gradient and theme color on page load
    restoreSettings();

    $('.gradient-controls input[type="range"]').hover(function() {
        $(this).find('::-webkit-slider-thumb, ::-moz-range-thumb, ::-ms-thumb').css('transform', 'scale(1.2)');
    }, function() {
        $(this).find('::-webkit-slider-thumb, ::-moz-range-thumb, ::-ms-thumb').css('transform', 'scale(1)');
    });
    
    $('#colorControlsButton').on('click', function() {
        const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' });
        if ($('.gradient-controls-container').hasClass('show')) {
            $('.gradient-controls-container').slideUp('slow', function() {
                $(this).removeClass('show');
            });
        } else {
            scrollToTop();
            $('.gradient-controls-container').slideDown('slow').addClass('show');
        }
    });

    $(document).on('click', function(event) {
        if (!$(event.target).closest('.gradient-controls-container').length && !$(event.target).is('#colorControlsButton')) {
            $('.gradient-controls-container').slideUp('slow', function() {
                $(this).removeClass('show');
            });
        }
    });

    $('#degRange, #percentageRange').on('input', function() {
        updateGradient();
    });

    $('#colorPicker').on('change', function() {
        updateGradient();
    });
});