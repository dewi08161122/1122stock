async function renderHotStocks() {
    const marketContainer = document.querySelector('.market');
    const timeDisplay = document.querySelector('.time');

    try {
        const response = await fetch('/api/hotstock/value');
        const result = await response.json();

        if (!result.ok || result.error) {
            marketContainer.innerHTML = `<p style="color: red;">資料載入失敗: ${result.message}</p>`;
            return;
        }
        const stocksArray = result.data;
        marketContainer.innerHTML = '';

        if (stocksArray.length > 0) {
            timeDisplay.textContent = `資料日期：${stocksArray[0].time}`;
        }

       stocksArray.forEach(stock => {
            const stockContent = document.createElement('div');
            stockContent.className = 'stock-content';

            let trendClass = 'draw';
            let trendSymbol = '─';
            if (stock.change_price > 0) {
                trendClass = 'up';
                trendSymbol = '▲';
            } else if (stock.change_price < 0) {
                trendClass = 'down';
                trendSymbol = '▼';
            }

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
            marketContainer.appendChild(stockContent);
        });

    } catch (error) {
        console.error("渲染錯誤:", error);
        marketContainer.innerHTML = `<p>伺服器連線異常</p>`;
    }
}

document.addEventListener('DOMContentLoaded', renderHotStocks);