
function init(){
    var margin = {top: -5, right: -5, bottom: -5, left: -5};

    var winWidth = -1, winHeight = -1;
    if (window.innerWidth)
        winWidth = window.innerWidth;
    else if ((document.body) && (document.body.clientWidth))
        winWidth = document.body.clientWidth;
    if (window.innerHeight)
        winHeight = window.innerHeight;
    else if ((document.body) && (document.body.clientHeight))
        winHeight = document.body.clientHeight;
    if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
        winHeight = document.documentElement.clientHeight;
        winWidth = document.documentElement.clientWidth;
    }

    var width, height;
    if (winWidth != -1) {
        width = winWidth - margin.left - margin.right;
    } else {
        width = 800 - margin.left - margin.right;
    }
    if (winHeight != -1) {
        height = winHeight - margin.top - margin.bottom;
    } else {
        height = 600 - margin.top - margin.bottom;
    }
    
    var svg = d3.select("body").append("svg")
        .attr("width", width)
      .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.right + ")");
}

$(document).ready(function(){
    init();
});