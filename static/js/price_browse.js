var slider_browse = document.getElementById("price_browse_range");
var output_browse = document.getElementById("price_browse");
output_browse.innerHTML = slider_browse.value;
slider_browse.oninput = function() {
    output_browse.innerHTML = this.value;
    };