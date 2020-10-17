var res = $('body').attr('data-res');


function getData1() {
    var rp = JSON.parse(res);
    console.log(res)
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
    console.log(data)
    return data;
}

function getData2() {
    var rp = JSON.parse(res);
    var data = [];
    for (const item of rp) {
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

// var ctx2 = document.getElementById('chart2').getContext('2d');
// ctx2.canvas.width = 1000;
// ctx2.canvas.height = 350;
// var chart2 = new Chart(ctx2, {
//     type: 'candlestick',
//     data: {
//         datasets: [{
//             label: 'Exchange: Binance',
//             data: getData2()
//         }]
//     }
// });

var getRandomInt = function (max) {
    return Math.floor(Math.random() * Math.floor(max));
};

function randomNumber(min, max) {
    return Math.random() * (max - min) + min;
}

function randomBar(date, lastClose) {
    var open = randomNumber(lastClose * 0.95, lastClose * 1.05).toFixed(2);
    var close = randomNumber(open * 0.95, open * 1.05).toFixed(2);
    var high = randomNumber(Math.max(open, close), Math.max(open, close) * 1.1).toFixed(2);
    var low = randomNumber(Math.min(open, close) * 0.9, Math.min(open, close)).toFixed(2);
    return {
        t: date.valueOf(),
        o: open,
        h: high,
        l: low,
        c: close
    };

}

function getRandomData(dateStr, count) {
    var date = luxon.DateTime.fromRFC2822(dateStr);
    var data = [randomBar(date, 30)];
    while (data.length < count) {
        date = date.plus({days: 1});
        if (date.weekday <= 5) {
            data.push(randomBar(date, data[data.length - 1].c));
        }
    }
    return data;
}

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

// document.getElementById('update').addEventListener('click', update);
//
// document.getElementById('randomizeData').addEventListener('click', function () {
//     chart.data.datasets.forEach(function (dataset) {
//         dataset.data = getRandomData(initialDateStr, barCount);
//     });
//     update();
// });