$(document).ready(function () {
    var $container = $('#profileContainer');

    $container.isotope({
        itemSelector: '.profile-card',
        masonry: {
            columnWidth: 40,
            isFitWidth: true
        }
    });

    // Search functionality
    $('#searchInput').on('keyup', function () {
        var searchValue = $(this).val().toLowerCase();
        $container.isotope({ filter: '.profile-card:contains("' + searchValue + '")' });
    });

    function toggleVisibility(element) {
        var $profileCard = $(element).closest('.profile-card');
        var $hiddenContent = $profileCard.find('.hidden-content');
        
        $hiddenContent.toggle();

        // Toggle a class to handle the closed state with max-height
        $profileCard.toggleClass('closed', !$hiddenContent.is(':visible'));
        $container.isotope('layout');

        // Save toggle state to localStorage
        var cardIndex = $('.profile-card').index($(element).closest('.profile-card'));
        var toggleState = $hiddenContent.is(':visible');
        localStorage.setItem('toggleState_' + cardIndex, toggleState);
        $container.isotope('layout');
    }

    // Add an event listener for the toggle switch
    $('#toggleSwitch').on('change', function () {
        $('.hidden-content').toggle();
        updateToggleStates();
    });

    // Check toggle state on page load
    $(document).ready(function () {
        var isToggleChecked = JSON.parse(localStorage.getItem('isToggleChecked')) || false;

        // Set the checkbox state based on the localStorage value
        $('#toggleSwitch').prop('checked', isToggleChecked);

        if (isToggleChecked) {
            $('.hidden-content').show();
            $container.isotope('layout'); // load lại layout
        } else {
            $('.hidden-content').hide();
            $container.isotope('layout');
        }
    });

    // Update toggle states on page load
    function updateToggleStates() {
        var isToggleChecked = $('#toggleSwitch').prop('checked');
        localStorage.setItem('isToggleChecked', isToggleChecked);

        $('.profile-card').each(function (index) {
            var $hiddenContent = $(this).find('.hidden-content');
            if (isToggleChecked) {
                $hiddenContent.show();
                $container.isotope('layout');
            } else {
                $hiddenContent.hide();
                $container.isotope('layout');
            }
        });
    }

    // Attach click event to the profile pictures and profile info
    $('.profile-picture').on('click', function (e) {
        e.preventDefault();
        toggleVisibility(this);
        $container.isotope('layout');
    });

    // Custom jQuery :contains case-insensitive selector
    $.expr[":"].contains = $.expr.createPseudo(function (arg) {
        return function (elem) {
            return $(elem).text().toLowerCase().indexOf(arg.toLowerCase()) >= 0;
        };
    });
});
