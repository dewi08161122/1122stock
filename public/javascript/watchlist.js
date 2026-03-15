async function renderHotStocks() {
    const watchlistContainer = document.querySelector('.watchlist');
    const timeDisplay = document.querySelector('.time');

    try {
        const response = await fetch('/api/hotstock/value');
        const result = await response.json();

        if (!result.ok || result.error) {
            watchlistContainer.innerHTML = `<p style="color: red;">資料載入失敗: ${result.message}</p>`;
            return;
        }
        const stocksArray = result.data;
        watchlistContainer.innerHTML = '';

        // 更新頁面上的資料日期 (顯示最後取得資料的日期)
        if (stocksArray.length > 0) {
            timeDisplay.textContent = `資料日期：${stocksArray[0].time}`;
        }

        // 渲染 30 筆資料
       stocksArray.forEach(stock => {
            const stockContent = document.createElement('div');
            stockContent.className = 'stock-content';

            // 判斷漲跌顏色與符號
            let trendClass = 'draw';
            let trendSymbol = '─';
            if (stock.change_price > 0) {
                trendClass = 'up';
                trendSymbol = '▲';
            } else if (stock.change_price < 0) {
                trendClass = 'down';
                trendSymbol = '▼';
            }

            // 建立內部 HTML
            stockContent.innerHTML = `
                <div class="stock-main">
                    <a href="/stock/${stock.number}" class="stock-name">${stock.number} &nbsp; ${stock.name}</a>
                    <div class="stock-price ${trendClass}">${stock.close.toFixed(2)}</div>
                    <div class="stock-trend ${trendClass}">
                        ${trendSymbol} 
                        <span class="change-point">${Math.abs(stock.change_price).toFixed(2)}</span>
                        <span class="change-percent">${Math.abs(stock.percent).toFixed(2)}%</span>
                    </div>
                </div>
            `;
            watchlistContainer.appendChild(stockContent);
        });

    } catch (error) {
        console.error("渲染錯誤:", error);
        watchlistContainer.innerHTML = `<p>伺服器連線異常</p>`;
    }
}

// 頁面載入後執行
document.addEventListener('DOMContentLoaded', renderHotStocks);