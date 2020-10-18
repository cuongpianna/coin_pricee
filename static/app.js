var res = $('body').attr('data-res');
var upbits = $('body').attr('data-upbit');

var upbitExchangeData = []

var bar = "1m"


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
    return upbitExchangeData;
}

function parseData() {
    var rp = JSON.parse(upbits);
    var data = [];
    for (const item of rp.reverse()) {
        var obj = {
            t: item.timestamp,
            o: item.open,
            h: item.high,
            l: item.low,
            c: item.close
        }
        data.push(obj);
    }
    upbitExchangeData = data;
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
            data: parseData()
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

socket.on('coin', function (msg) {
    var data = JSON.parse(JSON.stringify(msg.ms));
    var dataUpbit = JSON.parse(data.upbit);

    if (bar == "1m") {
        var date1 = new Date(dataUpbit.timestamp);
        var date2 = new Date(upbitExchangeData[upbitExchangeData.length - 1].t);

        var objUpbit = {
            t: dataUpbit.timestamp,
            o: dataUpbit.opening_price,
            h: dataUpbit.high_price,
            l: dataUpbit.low_price,
            c: dataUpbit.trade_price
        };

        if (dataUpbit.timestamp != upbitExchangeData[upbitExchangeData.length - 1].t) {
            upbitExchangeData.push(objUpbit)
            upbitExchangeData.shift()

            chart.update()
        }
    }

    // console.log(upbitExchangeData)

})

$('.upbit-row').click(function () {
    socket.emit('currency', {value: $(this).attr('data-item')});

    $.post('/change_currency/', {
        data: $(this).attr('data-item'),
    }).done(function (response) {
        let data = [];
        for (const item of response.result.reverse()) {
            var obj = {
                t: item.timestamp,
                o: item.open,
                h: item.high,
                l: item.low,
                c: item.close
            }
            data.push(obj);
        }
        upbitExchangeData = data;

        chart.data.datasets.forEach(function (dataset) {
            dataset.data = upbitExchangeData;
        });

        chart.update()
    }).fail(function () {
    });

})


socket.on('price', function (msg) {
    var data = JSON.parse(JSON.stringify(msg.ms));

    for(const [index, value] of data.entries()) {
        var e = '.upbit' + (index + 1);
        $(e).html(value);
    }

})