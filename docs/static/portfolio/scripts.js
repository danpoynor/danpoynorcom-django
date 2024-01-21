// Check if the page is being served over HTTPS
// In the local Django development server this will be false, so the Django
// Python code will be used to update the URL dynamically.
if (window.location.protocol === 'https:') {
    var orderElement = document.getElementById('order');

    if (orderElement) {
        orderElement.addEventListener('change', function () {
            // Get the current URL
            var currentUrl = window.location.href;
            // Replace '/asc/' or '/desc/' in the URL with the selected value
            var newUrl = currentUrl.replace(/\/(asc|desc)\//, '/' + this.value + '/');
            // Navigate to the new URL
            window.location.href = newUrl;
        });
    }
}
