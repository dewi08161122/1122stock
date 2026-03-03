function fmt(n) { return Number(n).toLocaleString(undefined, {minimumFractionDigits: 2}); }

async function fetchTodayMarket() {
    try {
        const response = await fetch("/api/todaymarket");
        const data = await response.json();
        if (data.error) return;

        // 渲染上市 (TAIEX)
        renderMarketData("taiex", data.TAIEX_information, data.TAIEX_market);
        // 渲染上櫃 (TPEX)
        renderMarketData("tpex", data.TPEX_information, data.TPEX_market);

        document.querySelector('.time').innerText = `最後更新：${data.TAIEX_information.time}`;
    } catch (e) { console.error(e); }
}

function renderMarketData(prefix, info, market) {
    // 填入基礎數值
    document.getElementById(`${prefix}-price`).innerText = fmt(info.close);
    document.getElementById(`${prefix}-value`).innerText = `${(info.value / 1e8).toFixed(0)} 億`;
    
    const trendEl = document.getElementById(`${prefix}-trend`);
    trendEl.querySelector('.change-point').innerText = fmt(Math.abs(info.change_price));
    trendEl.querySelector('.change-percent').innerText = `${fmt(Math.abs(info.percent))}%`;

    // 處理顏色與符號
    trendEl.classList.remove('up', 'down');
    let symbol = info.change_price > 0 ? "▲ " : (info.change_price < 0 ? "▼ " : "─ ");
    if (info.change_price > 0) trendEl.classList.add('up');
    if (info.change_price < 0) trendEl.classList.add('down');
    
    // 更新符號 (假設你在 trend 內部的最前面手動加一個文字或 span)
    trendEl.firstChild.textContent = symbol;

    // 填入家數統計
    document.getElementById(`${prefix}-rise`).innerText = market.rise;
    document.getElementById(`${prefix}-fall`).innerText = market.fall;
    document.getElementById(`${prefix}-flat`).innerText = market.flat;
}
fetchTodayMarket()