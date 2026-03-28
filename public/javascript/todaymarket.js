function fmt(n) { return Number(n).toLocaleString(undefined, {minimumFractionDigits: 2}); }

async function fetchTodayMarket() {
    try {
        const response = await fetch("/api/todaymarket");
        const data = await response.json();
        if (data.error) return;
        renderMarketData("taiex", data.TAIEX_information, data.TAIEX_market);
        renderMarketData("tpex", data.TPEX_information, data.TPEX_market);
        document.querySelector('.time').innerText = `最後更新：${data.TAIEX_information.time}`;
    } catch (e) { console.error(e); }
}

function renderMarketData(prefix, info, market) {
    const priceEl = document.getElementById(`${prefix}-price`);
    const trendEl = document.getElementById(`${prefix}-trend`);
    
    priceEl.innerText = fmt(info.close);
    document.getElementById(`${prefix}-value`).innerText = `${(info.value / 1e8).toFixed(0)} 億`;
    trendEl.querySelector('.change-point').innerText = fmt(Math.abs(info.change_price));
    trendEl.querySelector('.change-percent').innerText = `${fmt(Math.abs(info.percent))}%`;

    priceEl.classList.remove('up', 'down');
    trendEl.classList.remove('up', 'down');
    
    let symbol = info.change_price > 0 ? "▲ " : (info.change_price < 0 ? "▼ " : "─ ");
    if (info.change_price > 0) {
        trendEl.classList.add('up');
        priceEl.classList.add('up');
    } else if (info.change_price < 0) {
        trendEl.classList.add('down');
        priceEl.classList.add('down');
    }
    trendEl.querySelector('span:first-child').textContent = symbol;

    document.getElementById(`${prefix}-rise`).innerText = market.rise;
    document.getElementById(`${prefix}-fall`).innerText = market.fall;
    document.getElementById(`${prefix}-flat`).innerText = market.flat;

    const canvas = document.getElementById(`${prefix}-k-canvas`);
    if (canvas) {
        drawCandle(canvas, info);
    }
}

function drawCandle(canvas, data) {
    const ctx = canvas.getContext('2d');
    const { open, high, low, close } = data;
    const width = canvas.width;
    const height = canvas.height;
    
    ctx.clearRect(0, 0, width, height);

    const padding = 10;
    const chartHeight = height - padding * 2;
    const range = high - low;
    const safeRange = range === 0 ? 1 : range;
    const getY = (price) => padding + (high - price) / safeRange * chartHeight;

    const color = close >= open ? '#ef5350' : '#26a69a';
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 3;

    ctx.beginPath();
    ctx.moveTo(width / 2, getY(high));
    ctx.lineTo(width / 2, getY(low));
    ctx.stroke();

    const rectWidth = 18; 
    const rectX = (width / 2) - (rectWidth / 2);
    const rectTop = getY(Math.max(open, close));
    let rectHeight = Math.abs(getY(open) - getY(close));
    if (rectHeight < 1) rectHeight = 1;

    ctx.fillRect(rectX, rectTop, rectWidth, rectHeight);
}

fetchTodayMarket();