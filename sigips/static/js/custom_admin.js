document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.print-button');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var url = this.dataset.url;
            var iframe = document.createElement('iframe');
            iframe.src = url;
            iframe.style.display = 'none';
            document.body.appendChild(iframe);

            iframe.onload = function() {
                iframe.contentWindow.print();
            };
        });
    });
});
