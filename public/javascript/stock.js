const stockId = window.location.pathname.split('/').pop();
const KLine = document.querySelector('.KLine');

let allData = [];
let currentOffset = 0;
let isLoading = false;
let hasMoreData = true;

// ===== 左上資訊區 =====
const infoBar = document.createElement('div');
infoBar.className = 'kline-info-bar';
infoBar.style.position = 'absolute';
infoBar.style.top = '10px';
infoBar.style.left = '12px';
infoBar.style.zIndex = '20';
infoBar.style.color = '#d1d4dc';
infoBar.style.fontSize = '14px';
infoBar.style.lineHeight = '1.6';
infoBar.style.pointerEvents = 'none';
infoBar.style.fontFamily = 'sans-serif';
KLine.style.position = 'relative';
KLine.appendChild(infoBar);

// ===== 建立圖表 =====
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
        fixRightEdge: true,
        visible: false,
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
});

// ===== K線 =====
const candlestickSeries = chart.addSeries(LightweightCharts.CandlestickSeries, {
    upColor: '#ef5350',
    downColor: '#26a69a',
    borderVisible: false,
    wickUpColor: '#ef5350',
    wickDownColor: '#26a69a',
    priceLineVisible: false,
    lastValueVisible: false,      // 關掉右側最新價格
});

// ===== 成交量 =====
const volumeSeries = chart.addSeries(LightweightCharts.HistogramSeries, {
    priceFormat: { type: "volume" },
    priceScaleId: "vol",
    lastValueVisible: false,      // 關掉右側成交量最新值標籤
    priceLineVisible: false,
});

// ===== 主圖區 =====
chart.priceScale("right").applyOptions({
    visible: true,
    autoScale: true,
    scaleMargins: {
        top: 0.12,
        bottom: 0.25, // 上面主圖
    },
});

// ===== 成交量區 =====
chart.priceScale("vol").applyOptions({
    visible: true,
    autoScale: true,
    scaleMargins: {
        top: 0.82,   // 下面約 18~20%
        bottom: 0.02,
    },
});

// ===== MA =====
const maSeries = {
    ma5: chart.addSeries(LightweightCharts.LineSeries, {
        color: "#ffeb3b",
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
        crosshairMarkerVisible: false,
    }),
    ma10: chart.addSeries(LightweightCharts.LineSeries, {
        color: "#3bfff5",
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
        crosshairMarkerVisible: false,
    }),
    ma30: chart.addSeries(LightweightCharts.LineSeries, {
        color: "#b73bff",
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
        crosshairMarkerVisible: false,
    }),
    ma90: chart.addSeries(LightweightCharts.LineSeries, {
        color: "#ffffff",
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
        crosshairMarkerVisible: false,
    }),
};

// ===== 取得股票顯示名稱 =====
function getStockDisplayInfo(data) {
    if (stockId === "TAIEX") {
        return { number: "TAIEX", name: "加權指數" };
    }
    if (stockId === "TPEX") {
        return { number: "TPEX", name: "櫃買指數" };
    }

    const itemWithName = data.find(d => d.name || d.number);
    return {
        number: itemWithName?.number || stockId,
        name: itemWithName?.name || "",
    };
}

// ===== 格式化 =====
function formatPrice(val) {
    if (val == null || Number.isNaN(val)) return "--";
    return Number(val).toFixed(2);
}

function formatVolume(val) {
    if (val == null || Number.isNaN(val)) return "--";
    return Number(val).toLocaleString('zh-TW');
}

function formatDate(time) {
    if (!time) return "--";
    if (typeof time === "string") return time;
    if (typeof time === "object" && time.year && time.month && time.day) {
        return `${time.year}/${time.month}/${time.day}`;
    }
    return String(time);
}

// ===== 更新左上資訊 =====
function updateInfoBar(barData, data) {
    const stockInfo = getStockDisplayInfo(data);

    const latest = data[data.length - 1];
    const target = barData || latest;
    if (!target) return;

    const ma5 = getSingleMAValue(data, 5, target.time);
    const ma10 = getSingleMAValue(data, 10, target.time);
    const ma30 = getSingleMAValue(data, 30, target.time);
    const ma90 = getSingleMAValue(data, 90, target.time);

    const prev = findPreviousBar(data, target.time);
    const change = prev ? (target.close - prev.close) : 0;
    const changePercent = prev && prev.close ? (change / prev.close) * 100 : 0;

    const changeColor = change > 0 ? '#ef5350' : change < 0 ? '#26a69a' : '#d1d4dc';

    infoBar.innerHTML = `
        <div style="font-size: 20px; font-weight: 700; margin-bottom: 4px; color: #ffffff;">
            ${stockInfo.number} ${stockInfo.name}
        </div>
        <div>
            ${formatDate(target.time)}
           　開盤：${formatPrice(target.open)}
           　最高：${formatPrice(target.high)}
           　最低：${formatPrice(target.low)}
           　收盤：<span style="color:${changeColor}; font-weight:700;">${formatPrice(target.close)}</span>
        </div>
        <div>
            成交量：${formatVolume(target.value)}
            ${target.amount != null ? `　成交金額：${formatVolume(target.amount)}` : ""}
            <span style="color:${changeColor};">
                ${prev ? `　漲跌：${change > 0 ? '+' : ''}${formatPrice(change)}　漲跌幅：${change > 0 ? '+' : ''}${formatPrice(changePercent)}%` : ""}
            </span>
        </div>
        <div>
            <span style="color:#ffeb3b;">MA5：${formatPrice(ma5)}</span>
            <span style="color:#3bfff5; margin-left: 12px;">MA10：${formatPrice(ma10)}</span>
            <span style="color:#b73bff; margin-left: 12px;">MA30：${formatPrice(ma30)}</span>
            <span style="color:#ffffff; margin-left: 12px;">MA90：${formatPrice(ma90)}</span>
        </div>
    `;
}

function findPreviousBar(data, time) {
    const index = data.findIndex(d => d.time === time);
    if (index > 0) return data[index - 1];
    return null;
}

function getSingleMAValue(data, day, targetTime) {
    const index = data.findIndex(d => d.time === targetTime);
    if (index < day - 1 || index === -1) return null;

    let sum = 0;
    for (let i = 0; i < day; i++) {
        sum += data[index - i].close;
    }
    return sum / day;
}

// ===== API =====
async function fetchKLineData(isInitial = true) {
    if (isLoading || !hasMoreData) return;
    isLoading = true;

    try {
        const response = await fetch(`/api/stock/${stockId}?offset=${currentOffset}`);
        const newData = await response.json();

        if (!newData || newData.length === 0) {
            hasMoreData = false;
            return;
        }

        allData = [...newData, ...allData];
        currentOffset += 500;

        renderKLine(allData, isInitial);
        updateInfoBar(null, allData);

    } catch (error) {
        console.error(error);
    } finally {
        isLoading = false;
    }
}

// ===== 畫圖 =====
function renderKLine(data, isInitial) {
    candlestickSeries.setData(data);

    const candlestickData = data.map(d => {
        let color;

        if (d.close > d.open) {
            color = '#ef5350'; // 漲
        } else if (d.close < d.open) {
            color = '#26a69a'; // 跌
        } else {
            color = '#ffd54f'; // 👉 平盤（黃）
        }

        return {
            time: d.time,
            open: d.open,
            high: d.high,
            low: d.low,
            close: d.close,
            color,
            borderColor: color,
            wickColor: color,
        };
    });
    candlestickSeries.setData(candlestickData);

    const volumeData = data.map((d, i) => {
    let color;

    if (i === 0) {
        color = '#999999'; // 第一根
    } else {
        const prevClose = data[i - 1].close;

        if (d.close > prevClose) {
            color = '#ef5350'; // 漲
        } else if (d.close < prevClose) {
            color = '#26a69a'; // 跌
        } else {
            color = '#ffd54f'; // 👉 平盤（黃）
        }
    }

    return {
        time: d.time,
        value: d.value,
        color,
    };
});

volumeSeries.setData(volumeData);

    maSeries.ma5.setData(calculateMA(data, 5));
    maSeries.ma10.setData(calculateMA(data, 10));
    maSeries.ma30.setData(calculateMA(data, 30));
    maSeries.ma90.setData(calculateMA(data, 90));

    if (isInitial) {
        const N = 150;
        if (data.length > N) {
            chart.timeScale().setVisibleRange({
                from: data[data.length - N].time,
                to: data[data.length - 1].time,
            });
        } else {
            chart.timeScale().fitContent();
        }
    }
}

// ===== MA 計算 =====
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
            value: sum / day
        });
    }
    return result;
}

// ===== 滑鼠移動時更新左上資訊 =====
chart.subscribeCrosshairMove(param => {
    if (!param || !param.time || !allData.length) {
        updateInfoBar(null, allData);
        return;
    }

    const barData = allData.find(d => d.time === param.time);
    if (barData) {
        updateInfoBar(barData, allData);
    } else {
        updateInfoBar(null, allData);
    }
});

// ===== 無限滾動 =====
chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
    if (!range) return;
    const preloadThreshold = 120;
    if (range.from < preloadThreshold && !isLoading && hasMoreData) {
        fetchKLineData(false);
    }
});

// ===== Resize =====
const resizeObserver = new ResizeObserver(entries => {
    if (!entries.length) return;
    const { width, height } = entries[0].contentRect;
    chart.applyOptions({ width, height });
});
resizeObserver.observe(KLine);

// ===== 啟動 =====
fetchKLineData(true);