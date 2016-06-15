var map_data;
var userId = 1;
var width, height;

function init(){
	initUserInfo();
    initWidthAndHeight();
    
    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)

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
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"})

        var color_scaler = d3.scale.ordinal().range(["#aec7e8", "#ffbb78", "#98df8a", "#c5b0d5", "#f7b6d2", "#c7c7c7", "#ffffff"])

        var rects = units.append("rect")
            .attr("id", function(d){ return d.boothId; })
            .attr("width", function(d){ return d.width; })
            .attr("height", function(d){ return d.height; })
            .attr("fill", function(d){ return color_scaler(d.theme); })
            .on("click", visitBooth);

        var text = units.append("text")
            .attr("class", "label")
            .attr("x", function(d){ return d.width / 2 ;})
            .attr("y", function(d){ return d.height / 2 ;})
            .attr("dy", ".35em")
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

function initUserInfo(){
    $.post("/init/", { uid: userId });
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
        resultCell.theme = group["theme"];
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
    var boothId = d.boothId;
    console.log("visit the booth:" + boothId);
    $.post("/trace/",
    {
        uid: userId,
        boothId: boothId
    },
    function(data){
        redrawNode(data);
        redrawPath();
    })
}
7
function redrawNode(routeList){  
	var units = d3.select("svg")
		.selectAll(".group_row")
		.selectAll(".group")
		.selectAll(".unit");

	var nodes = units.selectAll(".node")
		.data(function(d) { return checkNode(d, routeList); });

	var nodeEnter = nodes.enter()
		.append("circle")
		.attr("class", "node")
		.attr("cx", function(d){
			return ($(this).siblings("rect").attr("width")) / 2;
		})
		.attr("cy", function(d){
			return ($(this).siblings("rect").attr("height")) / 2;
		})

	var nodeUpdate = d3.transition(nodes)
		//.duration(1500)
		.attr("r", 7)
		.style("fill-opacity", 1);

	var nodeExit = d3.transition(nodes.exit())
		.attr("r", 0)
		.style("fill-opacity", 0)
		.remove();
}

function checkNode(d, routeList){
	var boothId = d.boothId
	if(routeList.indexOf(boothId) != -1)
		return [boothId];
	else
		return [];
	
}

function redrawPath(){
	$("path").remove();

	var nodes = d3.selectAll(".node");
	var pathData = nodes[0].map(getCoord).sort(compareNode);

	console.log(pathData);
	var line = d3.svg.line()
		.x(function(d) { return d.x; })
		.y(function(d) { return d.y; })
		.interpolate("linear");//monotone

	var path = d3.select("svg").append("g")
		.append("path")
		.attr("class", "path")
		.attr("d", line(pathData));
}

function getCoord(d){
	var x = 0;
	var y = 0;
	var reg = /[(,)]/;

	var rect = $(d).siblings("rect");
	x += rect.attr("width") / 2;
	y += rect.attr("height") / 2;

	var unit = $(d).parent();
	var tokens = unit.attr("transform").split(reg);
	x += parseFloat(tokens[1]);
	y += parseFloat(tokens[2]);

	var group = unit.parent();
	var tokens = group.attr("transform").split(reg);
	x += parseFloat(tokens[1]);

	var group_row = group.parent();
	var tokens = group_row.attr("transform").split(reg);
	y += parseFloat(tokens[2]);

	var id = rect.attr("id");
	id = (id == -1)? 100 : parseInt(id);
	result = { "x" : x, "y" : y, "boothId" : id};
	return result;
}

function compareNode(a, b){
	if(a.boothId > b.boothId)
		return 1;
	else if(a.boothId < b.boothId)
		return -1;
	else
		return 0;
}


$(document).ready(function(){
    init();
});