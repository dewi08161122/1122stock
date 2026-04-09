const stockId = window.location.pathname.split('/').pop();
const KLine = document.querySelector('.KLine');

let allData = [];
let currentOffset = 0;
let currentPeriod = 'day';
let isLoading = false;
let hasMoreData = true;

// 左上資訊區
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

// 建立圖表
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

// K線
const candlestickSeries = chart.addSeries(LightweightCharts.CandlestickSeries, {
    upColor: '#ef5350',
    downColor: '#26a69a',
    borderVisible: false,
    wickUpColor: '#ef5350',
    wickDownColor: '#26a69a',
    priceLineVisible: false,
    lastValueVisible: false,
});

// 成交量
const volumeSeries = chart.addSeries(LightweightCharts.HistogramSeries, {
    priceFormat: { type: "volume" },
    priceScaleId: "vol",
    lastValueVisible: false,
    priceLineVisible: false,
});

// 主圖區
chart.priceScale("right").applyOptions({
    visible: true,
    autoScale: true,
    scaleMargins: {
        top: 0.12,
        bottom: 0.25,
    },
});

// 成交量區
chart.priceScale("vol").applyOptions({
    visible: true,
    autoScale: true,
    scaleMargins: {
        top: 0.82,   // 下面約 18~20%
        bottom: 0.02,
    },
});

// MA
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
    ma20: chart.addSeries(LightweightCharts.LineSeries, {
        color: "#b73bff",
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
        crosshairMarkerVisible: false,
    }),
    ma60: chart.addSeries(LightweightCharts.LineSeries, {
        color: "#ffffff",
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
        crosshairMarkerVisible: false,
    }),
};

// 取得股票顯示名稱
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

    if (stockId === "TAIEX" || stockId === "TPEX") {
        return (val / 100000000).toFixed(2) + " 億";
    }

    return Number(val).toLocaleString('zh-TW') + " 張";
}

function formatDate(time) {
    if (!time) return "--";
    if (typeof time === "string") return time;
    if (typeof time === "object" && time.year && time.month && time.day) {
        return `${time.year}/${time.month}/${time.day}`;
    }
    return String(time);
}

// 更新左上資訊
function updateInfoBar(barData, data) {
    const stockInfo = getStockDisplayInfo(data);

    const latest = data[data.length - 1];
    const target = barData || latest;
    if (!target) return;

    const ma5 = getSingleMAValue(data, 5, target.time);
    const ma10 = getSingleMAValue(data, 10, target.time);
    const ma20 = getSingleMAValue(data, 20, target.time);
    const ma60 = getSingleMAValue(data, 60, target.time);

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
            <span style="color:#b73bff; margin-left: 12px;">MA20：${formatPrice(ma20)}</span>
            <span style="color:#ffffff; margin-left: 12px;">MA60：${formatPrice(ma60)}</span>
        </div>
    `;
}

function findPreviousBar(data, time) {
    const index = data.findIndex(d => d.time === time);
    if (index > 0) return data[index - 1];
    return null;
}

function getSingleMAValue(data, day, targetTime) {
    const bar = data.find(d => d.time === targetTime);
    if (!bar) return null;

    if (day === 5) return bar.ma5;
    if (day === 10) return bar.ma10;
    if (day === 20) return bar.ma20; 
    if (day === 60) return bar.ma60; 
    return null;
}

// 取資料
async function fetchKLineData(isInitial = true) {
    if (isLoading || !hasMoreData) return;
    isLoading = true;

    const timeScale = chart.timeScale();
    const scrollPosition = timeScale.getVisibleLogicalRange();
    try {
        const response = await fetch(`/api/stock/${stockId}?offset=${currentOffset}&period=${currentPeriod}`);
        const newData = await response.json();

        if (!newData || newData.length === 0 || newData.error) {
            hasMoreData = false;
            return;
        }

        const addedCount = newData.length;

        if (currentPeriod !== 'day') {
            allData = newData; 
            hasMoreData = false;
        } else {
            allData = [...newData, ...allData];
            currentOffset += 500;
        }

        renderKLine(allData, isInitial);
        if (!isInitial && scrollPosition && addedCount > 0) {
            requestAnimationFrame(() => {
                timeScale.scrollToPosition(scrollPosition.from + addedCount, false);
                
                timeScale.setVisibleLogicalRange({
                    from: scrollPosition.from + addedCount,
                    to: scrollPosition.to + addedCount,
                });
            });
        }

    } catch (error) {
        console.error(error);
    } finally {
        isLoading = false;
    }
}

// K線圖和成交量圖
function renderKLine(data, isInitial) {
    candlestickSeries.setData(data);

    const candlestickData = data.map(d => {
        let color;

        if (d.close > d.open) {
            color = '#ef5350'; 
        } else if (d.close < d.open) {
            color = '#26a69a'; 
        } else {
            color = '#ffd54f'; 
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
        color = '#999999'; 
    } else {
        const prevClose = data[i - 1].close;

        if (d.close > prevClose) {
            color = '#ef5350'; 
        } else if (d.close < prevClose) {
            color = '#26a69a'; 
        } else {
            color = '#ffd54f'; 
        }
    }

    return {
        time: d.time,
        value: d.value,
        color,
    };
});

volumeSeries.setData(volumeData);

    maSeries.ma5.setData(data.map(d => ({ time: d.time, value: d.ma5 })));
    maSeries.ma10.setData(data.map(d => ({ time: d.time, value: d.ma10 })));
    maSeries.ma20.setData(data.map(d => ({ time: d.time, value: d.ma20 }))); 
    maSeries.ma60.setData(data.map(d => ({ time: d.time, value: d.ma60 })));

    if (isInitial) {
        requestAnimationFrame(() => {
            const N = 150;
            const timeScale = chart.timeScale();
            if (data.length > N) {
                timeScale.setVisibleRange({
                    from: data[data.length - N].time,
                    to: data[data.length - 1].time,
                });
            } else {
                timeScale.fitContent();
            }
        });
    }
}
// 移動時更新左上資訊
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

// 無限滾動
chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
    if (!range) return;
    const preloadThreshold = 120;
    if (range.from < preloadThreshold && !isLoading && hasMoreData) {
        fetchKLineData(false);
    }
});

const resizeObserver = new ResizeObserver(entries => {
    if (!entries.length) return;
    const { width, height } = entries[0].contentRect;
    chart.applyOptions({ width, height });
});
resizeObserver.observe(KLine);

fetchKLineData(true);

// 會員功能(加入觀察名單)
const ob_button = document.querySelector('.ob_button');

if (ob_button) {
    if (stockId === "TAIEX" || stockId === "TPEX") {
        ob_button.style.display = "none";
    } else {
        ob_button.style.display = "";
        ob_button.onclick = async () => {
            const isLogin = document.body.dataset.login === "true";

            if (!isLogin) {
                const login_box = document.getElementById("login");
                const opacity = document.querySelector(".opacity");

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
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ number: stockId })
                });

                const result = await response.json();

                if (result.ok) {
                    alert(`✅ 成功！股票 ${stockId} 已加入觀察名單`);
                } else if (result.error) {
                    alert(`❌ 錯誤：${result.message}`);
                } else {
                    alert(`ℹ️ 提示：股票 ${stockId} 已經在您的觀察名單中了`);
                }
            } catch (error) {
                alert("⚠️ 系統連線異常，請稍後再試");
            }
        };
    }
}
// K線切換
const kbars = document.querySelectorAll('.kbar');

kbars.forEach(bar => {
    bar.addEventListener('click', () => {
        const newPeriod = bar.getAttribute('data-period');
        
        kbars.forEach(b => b.classList.remove('active'));
        bar.classList.add('active');

        changePeriod(newPeriod);
    });
});

function changePeriod(newPeriod) {
    if (currentPeriod === newPeriod) return;
    
    currentPeriod = newPeriod;
    allData = [];
    currentOffset = 0;
    hasMoreData = true;
    candlestickSeries.setData([]);
    volumeSeries.setData([]);
    maSeries.ma5.setData([]);
    maSeries.ma10.setData([]);
    maSeries.ma20.setData([]);
    maSeries.ma60.setData([]);

    fetchKLineData(true);
}