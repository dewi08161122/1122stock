const stockId = window.location.pathname.split('/').pop();
const KLine = document.querySelector('.KLine');
const chart = LightweightCharts.createChart(KLine, {
    width: KLine.clientWidth,
    height: KLine.clientHeight,
    layout: {
    background: { type: "solid", color: "#1a1a1a" },
    textColor: "#d1d4dc",
    },
    grid: {
        vertLines: { color: "#2b2b2b" },
        horzLines: { color: "#2b2b2b" },
    },
    timeScale: {
        borderColor: "#2b2b2b",
    },
    rightPriceScale: {
        borderColor: "#2b2b2b",
    },
});

const candlestickSeries = chart.addSeries(LightweightCharts.CandlestickSeries,{
    upColor: '#ef5350',    
    downColor: '#26a69a',  
    borderVisible: false,
    priceLineVisible: false,
    wickUpColor: '#ef5350',
    wickDownColor: '#26a69a',
});
const volumeSeries = chart.addSeries(LightweightCharts.HistogramSeries, {
    priceFormat: { type: "volume" },
    lastValueVisible: false,
    priceLineVisible: false,
    priceScaleId: "vol", 
});
const ma5Series = chart.addSeries(LightweightCharts.LineSeries, {
    color: "#ffeb3b",  
    lineWidth: 1,
    priceLineVisible: false,
    lastValueVisible: false,
    crosshairMarkerVisible: false,
});
const ma10Series = chart.addSeries(LightweightCharts.LineSeries, {
    color: "#3bfff5",  
    lineWidth: 1,
    priceLineVisible: false,
    lastValueVisible: false,
    crosshairMarkerVisible: false,
});
const ma30Series = chart.addSeries(LightweightCharts.LineSeries, {
    color: "#b73bff",  
    lineWidth: 1,
    priceLineVisible: false,
    lastValueVisible: false,
    crosshairMarkerVisible: false,
});
const ma90Series = chart.addSeries(LightweightCharts.LineSeries, {
    color: "#ffffff",  
    lineWidth: 1,
    priceLineVisible: false,
    lastValueVisible: false,
    crosshairMarkerVisible: false,
});

chart.priceScale("right").applyOptions({
    scaleMargins: { top: 0.1, bottom: 0.3 },
});

chart.priceScale("vol").applyOptions({
    visible: false,
    scaleMargins: { top: 0.85, bottom: 0.0 },
});


async function KLineData() {
    const nameSpan = document.querySelector('.stock-name');
    let response=await fetch(`/api/stock/${stockId}`,{
        method:"GET"
    });
    let data = await response.json();   
    if (data && data.length > 0) {
        if (stockId === "TAIEX") {
            nameSpan.textContent = "加權指數 (TAIEX)";
        } else if (stockId === "TPEX") {
            nameSpan.textContent = "櫃買指數 (TPEX)";
        } else {
            const stockName = data[0].name || "";
            const stockNumber = data[0].number || stockId;
            nameSpan.textContent = `${stockNumber} ${stockName}`;
        }
    }
    candlestickSeries.setData(data);
    const ma5Data = calculateMA(data, 5);
    const ma10Data = calculateMA(data, 10);
    const ma30Data = calculateMA(data, 30);
    const ma90Data = calculateMA(data, 90);
    const volumeData = data.map((d, index) => {
        let color;
        if (index === 0) {
            color = "#999999";
        } else {
            const prevClose = data[index - 1].close;
            if (d.close > prevClose) {
                color = "#ef5350";
            } else if (d.close < prevClose) {
                color = "#26a69a";
            } else {
                color = "#ffa600";
            }
        }
        return {
            time: d.time,
            value: d.value,
            color: color,
        };
    });
    volumeSeries.setData(volumeData);
    ma5Series.setData(ma5Data);
    ma10Series.setData(ma10Data);
    ma30Series.setData(ma30Data);
    ma90Series.setData(ma90Data);
    const N = 160;
    if (data.length > N) {
        chart.timeScale().setVisibleRange({
        from: data[data.length - N].time,
        to: data[data.length - 1].time,
        });
    } else {
        chart.timeScale().fitContent();
    }
}
KLineData();

function calculateMA(data, day) {
    const result = [];

    for (let i = 0; i < data.length; i++) {
        if (i < day - 1) {
            result.push({ time: data[i].time, value: null });
            continue;
        }
        let sum = 0;
        for (let j = 0; j < day; j++) {
            sum += data[i - j].close;
        }
        result.push({
            time: data[i].time,
            value: sum / day,
        });
    }
    return result;
}

const resizeObserver = new ResizeObserver(entries => {
    const { width, height } = entries[0].contentRect;
    chart.applyOptions({ width, height });
});
const ob_button = document.querySelector('.ob_button');
const login_box = document.getElementById("login");
const opacity = document.querySelector(".opacity");
ob_button.onclick = async () => {
    const isLogin = document.body.dataset.login === "true";
    if (!isLogin) {
        if (login_box && opacity) {
            login_box.style.display = "block";
            opacity.style.display = "block";
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        return;
    }
    try {
        const response = await fetch('/api/watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "number": stockId })
        });
        const result = await response.json();
        if (result.ok) {
            alert(`✅ 成功！股票 ${stockId} 已加入觀察名單`);
            return;
        }
        if (result.error) {
            alert(`❌ 錯誤：${result.message}`);
        } else {
            alert(`ℹ️ 提示：股票 ${stockId} 已經在您的觀察名單中了`);
        }
    } catch (error) {
        console.error("加入觀察名單發生異常:", error);
        alert("⚠️ 系統連線異常，請稍後再試");
    }
};
resizeObserver.observe(KLine);