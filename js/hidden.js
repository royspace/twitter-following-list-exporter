document.addEventListener("DOMContentLoaded", function() {
    hideParent('.related a[href="nan"]');
    hideParentIfContains('.nick', 'nan');
    hideParentIfContains('.description', 'nan');
    hideParentIfContains('.date', 'nan');
    hideParentIfContains('.url', 'nan', 'false');
});

function hideParent(selector, targetText) {
    var elementsToHide = document.querySelectorAll(selector);

    elementsToHide.forEach(function(element) {
        var parent = element.closest('p');
        if (parent) {
            parent.style.display = 'none';
        }
    });
}

    function hideParentIfContains(selector, ...targetTexts) {
        var elementsToHide = document.querySelectorAll(selector);

        elementsToHide.forEach(function(element) {
            var content = element.innerText || element.textContent;

            for (const targetText of targetTexts) {
                if (content.includes(targetText)) {
                    console.log(content);
                    var parent = element.closest('p');
                    if (parent) {
                        parent.style.display = 'none';
                    }
                    break;  // Stop checking other targetTexts once one is found
                }
            }
        });
    }

function handleImageError(img) {
    // You can set a default image source or hide the image entirely
    img.src = 'images/0.png'; // Set a default image source
    // OR
    // img.style.display = 'none'; // Hide the image
}


