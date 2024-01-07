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