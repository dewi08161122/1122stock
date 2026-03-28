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
            stockContent.style.cursor = 'pointer';
            stockContent.onclick = () => {
                window.location.href = `/stock/${stock.number}`;
            };

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
                    <div class="stock-name">${stock.number} &nbsp; ${stock.name}</div>
                    <div class="stock-price ${trendClass}">${stock.close.toFixed(2)}</div>
                    <div class="stock-trend ${trendClass}">
                        ${trendSymbol} 
                        <span class="change-point">${Math.abs(stock.change_price).toFixed(2)}</span>
                        <span class="change-percent">${Math.abs(stock.percent).toFixed(2)}%</span>
                    </div>
                </div>
                <canvas class="mini-k-chart" width="40" height="60"></canvas>
            `;
            marketContainer.appendChild(stockContent);

            const canvas = stockContent.querySelector('.mini-k-chart');
            drawCandle(canvas, stock);

            function drawCandle(canvas, data) {
                const ctx = canvas.getContext('2d');
                const { open, high, low, close } = data;
                const width = canvas.width;
                const height = canvas.height;
                const padding = 5;
                const chartHeight = height - padding * 2;
                const range = high - low;
                const safeRange = range === 0 ? 1 : range;
                const getY = (price) => {
                    return padding + (high - price) / safeRange * chartHeight;
                };

                const color = close >= open ? '#eb4d4b' : '#2ecc71'; 
                ctx.strokeStyle = color;
                ctx.fillStyle = color;
                ctx.lineWidth = 2;

                ctx.beginPath();
                ctx.moveTo(width / 2, getY(high));
                ctx.lineTo(width / 2, getY(low));
                ctx.stroke();

                const rectWidth = 12;
                const rectX = (width / 2) - (rectWidth / 2);
                const rectTop = getY(Math.max(open, close));
                const rectBottom = getY(Math.min(open, close));
                let rectHeight = Math.abs(rectTop - rectBottom);
                
                if (rectHeight < 1) rectHeight = 1;

                ctx.fillRect(rectX, rectTop, rectWidth, rectHeight);
            }
        });

    } catch (error) {
        console.error("渲染錯誤:", error);
        marketContainer.innerHTML = `<p>伺服器連線異常</p>`;
    }
}

document.addEventListener('DOMContentLoaded', renderHotStocks);