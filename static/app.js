var res = $('body').attr('data-res');


function getData1() {
    var rp = JSON.parse(res);
    var data = [];
    for (const item of rp.reverse()) {
        var obj = {
            t: item.timestamp,
            o: item.opening_price,
            h: item.high_price,
            l: item.low_price,
            c: item.trade_price
        }
        data.push(obj);
    }
    return data;
}


var ctx = document.getElementById('chart').getContext('2d');
ctx.canvas.width = 1000;
ctx.canvas.height = 350;
var chart = new Chart(ctx, {
    type: 'candlestick',
    data: {
        datasets: [{
            label: 'Exchange: Huobi',
            data: getData1()
        }]
    }
});


var update = function () {
    var dataset = chart.config.data.datasets[0];

    // candlestick vs ohlc
    var type = document.getElementById('type').value;
    dataset.type = type;

    // linear vs log
    var scaleType = document.getElementById('scale-type').value;
    chart.config.options.scales.y.type = scaleType;

    // color
    var colorScheme = document.getElementById('color-scheme').value;
    if (colorScheme === 'neon') {
        dataset.color = {
            up: '#01ff01',
            down: '#fe0000',
            unchanged: '#999',
        };
    } else {
        delete dataset.color;
    }

    // border
    var border = document.getElementById('border').value;
    var defaultOpts = Chart.defaults.elements[type];
    if (border === 'true') {
        dataset.borderColor = defaultOpts.borderColor;
    } else {
        dataset.borderColor = {
            up: defaultOpts.color.up,
            down: defaultOpts.color.down,
            unchanged: defaultOpts.color.up
        };
    }

    chart.update();
};


var socket = io.connect('http://' + document.domain + ':' + location.port);

 socket.on('test', function (msg) {
     console.log('ok')
 })