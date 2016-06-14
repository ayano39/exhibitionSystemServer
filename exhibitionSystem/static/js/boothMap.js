var map_data;
var width, height;

function init(){
    initWidthAndHeight();
    
    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
      //.append("g")
        //.attr("transform", "translate(" + margin.left + "," + margin.right + ")");

    d3.json("/map_data/", function(error, data){
        if (error)
            console.warn(error);
        map_data = data;

        var grow_scaler = d3.scale.ordinal()
            .domain(normObjArr(map_data))
            .rangeRoundBands([0,height], 0.1, 0.05);

        var row_height = grow_scaler.rangeBand();

        var group_rows = svg.selectAll(".group_row")
            .data(map_data)
          .enter().append("g")
            .attr("class", "group_row")
            .attr("transform", function(d, index) { return "translate(0," + grow_scaler(index)+ ")" });

        var gp_scaler = d3.scale.ordinal()
            .domain(normObjArr(map_data[0]))
            .rangeRoundBands([0, width], 0.1, 0.05);

        var col_width = gp_scaler.rangeBand();

        var groups = group_rows.selectAll(".group")
            .data(function(d) { return d; })
          .enter().append("g")
            .attr("class", "group")
            .attr("transform", function(d, index){
                return "translate(" + gp_scaler(index) + ",0)";
            });
        
        var units = groups.selectAll(".unit")
            .data(function(d) { return parseGroup2Cell(d.group, col_width, row_height, d.x_pad*0.1*col_width, d.y_pad*0.1*row_height); })
          .enter().append("g")
            .attr("class", "unit")
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"});

        var rects = units.append("rect")
            .attr("id", function(d){ return d.boothId; })
            .attr("width", function(d){ return d.width; })
            .attr("height", function(d){ return d.height; })
            .on("click", visitBooth);
            //.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"});

        var text = units.append("text")
            .attr("class", "label")
            .attr("x", function(d){ return d.width / 2 ;})
            .attr("y", function(d){ return d.height / 2 ;})
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .text(function(d){ 
                if(d.boothId == -1)
                    return "出口";
                else
                    return "第" + d.boothId + "展台"; 
            });
    });
}

function initWidthAndHeight(){
    var margin = {top: 30, right: 30, bottom: 25, left: 25};
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
}

function normObjArr(array){
    normArr = []
    for(var i = 0; i < array.length; i++){
        normArr.push(i);
    }
    return normArr;
}

function parseGroup2Cell(groups, width, height, x_pad, y_pad){
    var unitWidth = (width - x_pad) / 2;
    var unitHeight = (height - y_pad) / 2;
    var result = [];
    for(var i = 0; i < groups.length; i ++){
        var resultCell = {};
        var group = groups[i];

        resultCell.boothId = group["boothId"];
        var cells = group["cell"];

        var up_left = false;
        var up_right = false;
        var down_left = false;
        var down_right = false;
        for(var j = 0; j < cells.length; j ++){
            switch(cells[j]){
                case 1:
                up_left = true;
                break;
                case 2:
                up_right = true;
                break;
                case 3:
                down_left = true;
                break;
                case 4:
                down_right = true;
                break;
            }
        }

        if((up_left && up_right) || (down_left && down_right)){
            resultCell.width = width;
            resultCell.x = 0;
        }
        else{
            resultCell.width = unitWidth;
            resultCell.x = (up_left || down_left)? 0 : (unitWidth + x_pad);
        }

        if((up_left && down_left) || (up_right && down_right)){
            resultCell.height = height;
            resultCell.y = 0;
        }
        else{
            resultCell.height = unitHeight;
            resultCell.y = (up_left|| up_right)? 0 : unitHeight + y_pad;
        }
        result.push(resultCell);
    }
    return result;
}

function visitBooth(d){
    var userId = 1;
    var boothId = d.boothId;
    //d3.json("/trace/")
        //.header("Content-Type", "application/x-www-form-urlencoded")
        //.post("uid=" + userId + "&boothId" + boothId, function(error, data){
            //console.log(data);
        //});
    $.post("/trace/",
    {
        uid: userId,
        boothId: boothId
    },
    function(data){
        console.log(data);
    })
}

$(document).ready(function(){
    init();
});