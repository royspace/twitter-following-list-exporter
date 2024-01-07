    // Function to extract username from the full URL based on the platform
    function extractUsername(fullUrl) {
        var parts = fullUrl.split('/');
        var usernamePart = parts.slice(3).join('/');
        var username = usernamePart.replace(/\/+$/, '');
        username = username.split('?')[0];
        return username;
    }

    // Update links to display only the username for Instagram, TikTok, and Facebook
    $(document).ready(function () {
        $('.url a, .related a').each(function () {
            var fullUrl = $(this).attr('href');
            var username = extractUsername(fullUrl);
            $(this).text(username);
        });
    });
    
    document.addEventListener('DOMContentLoaded', function() {
        var elementsToConvert = document.getElementsByClassName('friends_count');
    
        // Iterate through each element with the 'friends_count' class
        for (var i = 0; i < elementsToConvert.length; i++) {
            var element = elementsToConvert[i];
    
            // Parse the existing content, remove commas, convert to integer, and format with commas
            var value = parseInt(element.innerText.replace(/,/g, ''), 10);
            element.innerText = value.toLocaleString();
        }
    });
    