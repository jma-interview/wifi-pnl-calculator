var slider_txt = document.getElementById("price_text_range");
var output_txt = document.getElementById("price_text");
output_txt.innerHTML = slider_txt.value;
slider_txt.oninput = function() {
    output_txt.innerHTML = this.value;
    };