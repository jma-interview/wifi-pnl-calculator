var slider_stream = document.getElementById("price_stream_range");
var output_stream = document.getElementById("price_stream");
output_stream.innerHTML = slider_stream.value;
slider_stream.oninput = function() {
    output_stream.innerHTML = this.value;
    };