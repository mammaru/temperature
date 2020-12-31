var X, Y;
var d;
var step;

$("input[name='value_type']:radio").change(function(){
    background("white");
    colorMode(HSB, 360, 100, 100, 100);
    //console.log(getDataFile());
    $.getJSON(getDataFile(), function(data) {
        d = data;
        X = data["dates"].length;
        Y = data["years"].length;
        d["table"].map(function(v, i ,a) {
            v.map(function(vv, j, aa) {
                noStroke();
                fill(pickColor(vv - d["min"]));
                rect(j*step, i*step, step, step);
            });
        });
    })
//        .done(function() { alert('getJSON request succeeded!'); })
//        .fail(function(jqXHR, textStatus, errorThrown) { alert('getJSON request failed! ' + textStatus); console.log(jqXHR)})
//        .always(function() { alert('getJSON request ended!'); });
});

function getDataFile() {
    //console.log($("input[name='value_type']:radio:checked").val());
    if ($("input[name='value_type']:radio:checked").val() === "mean") {
        return "./data_daily_mean.json";
    } else if ($("input[name='value_type']:radio:checked").val() === "high") {
        return "./data_daily_high.json";
    } else if ($("input[name='value_type']:radio:checked").val() === "low") {
        return "./data_daily_low.json";
    }
}

function setup() {
    colorMode(HSB, 360, 100, 100, 100);
    $.getJSON(getDataFile(), (data) => {
        d = data;
        X = data["dates"].length;
        Y = data["years"].length;
        step = (($(window).height()-100) / Y) > ($(window).width() / X) ? $(window).width() / X : ($(window).height()-100) / Y;
        
        var canvas = createCanvas(X*step, Y*step);
        canvas.parent('canvas');
        background("white");

        d["table"].map(function(v, i ,a) {
            v.map(function(vv, j, aa) {
                noStroke();
                fill(pickColor(vv - d["min"]));
                rect(j*step, i*step, step, step);
            });
        });
    });
}


function draw(){
    if ((mouseX > 0) && (mouseY > 0) && (mouseX < X*step) && (mouseY < Y*step)) {
        x = Math.floor(mouseX / step);
        y = Math.floor(mouseY / step);
        //console.log(mouseX, mouseY);
        //$('#msg_box').css("transform", 'translate(' + (mouseX-$(window).scrollLeft()+50) + 'px, ' + (mouseY-$(window).scrollTop()+50) + 'px)');
        showDetail(d["years"][y] + "/" + d["dates"][x], d["table"][y][x]);
    } else {
        hideDetail();
    }
}


function pickColor(v) {
    var quotient = Math.floor(v / 2);
    return [360-28*quotient, 100, 100];
}

function showDetail(dt, v) {
    $('#msg_box').css("display", "flex");
    $('#msg_box').html(dt + "<br/>" + v + "℃");
}

function hideDetail(dt, v) {
    $('#msg_box').css("display", "none");
}
