let currentWatchlist = [];
async function renderWatchlist() {
    const watchlistContainer = document.querySelector('.watchlist');
    const timeDisplay = document.querySelector('.time');
    const loginPrompt = document.getElementById('login-prompt');
    const searchContainer = document.querySelector('.search-container');

    try {
        const response = await fetch('/api/watchlist');
        const result = await response.json();
        if (result.error) {
            loginPrompt.style.display = 'flex';
            watchlistContainer.style.display = 'none';
            searchContainer.style.display = 'none';
            currentWatchlist = [];

            const trigger = loginPrompt.querySelector('.login-trigger');
            trigger.onclick = () => {
                const login_box = document.getElementById("login");
                const opacity = document.querySelector(".opacity");
                if (login_box && opacity) {
                    login_box.style.display = "block";
                    opacity.style.display = "block";
                }
            };
            return;
        }
        loginPrompt.style.display = 'none';
        watchlistContainer.style.display = 'grid';
        currentWatchlist = result.data || [];
        if (currentWatchlist.length === 0) {
            watchlistContainer.innerHTML = `<p style="text-align: center; grid-column: 1/-1; color: #b2b5be; padding: 50px;">您的觀察名單目前是空的，快去搜尋股票加入吧！</p>`;
            return;
        }
        if (currentWatchlist[0].time) {
            timeDisplay.textContent = `資料日期：${currentWatchlist[0].time}`;
        }
        watchlistContainer.innerHTML = '';
        currentWatchlist.forEach(stock => {
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
                <div class="delete-btn" data-number="${stock.number}" onclick="deleteStock(event)">&times;</div>
        
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
const searchInput = document.querySelector('.stock-search');
const resultsContainer = document.getElementById('search-results');
let debounceTimer;

searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const keyword = searchInput.value.trim();

    if (keyword.length < 1) {
        resultsContainer.style.display = 'none';
        return;
    }

    // 防抖：停止輸入 300 毫秒後才發送 API
    debounceTimer = setTimeout(async () => {
        try {
            const response = await fetch(`/api/searchstock?keyword=${encodeURIComponent(keyword)}`);
            const data = await response.json();

            if (data && data.length > 0) {
                renderSuggestions(data);
            } else {
                resultsContainer.style.display = 'none';
            }
        } catch (error) {
            console.error("搜尋出錯:", error);
        }
    }, 300);
});

function renderSuggestions(stocks) {
    resultsContainer.innerHTML = '';
    stocks.forEach(stock => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        
        const isObserved = currentWatchlist.some(s => String(s.number).trim() === String(stock.number).trim());
        const actionText = isObserved 
            ? '<span class="status-added">已加入</span>' 
            : '<span class="status-add">選取加入</span>';

        item.innerHTML = `
            <div class="info">
                <span class="stock-no">${stock.number}</span> 
                <span class="stock-nm">${stock.name}</span>
            </div>
            ${actionText}
        `;
        
        item.onclick = async (e) => {
            if (isObserved) {
                alert(`ℹ️ 提示：股票 ${stock.number} 已經在您的觀察名單中了`);
                return;
            }
            try {
                const response = await fetch('/api/watchlist', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ "number": stock.number })
                });
                const result = await response.json();

                if (result.ok) {
                    alert(`✅ 成功！股票 ${stock.number} 已加入觀察名單`);
                    window.location.reload(); 
                } else if (result.error) {
                    if (result.message.includes("未登入") || result.message.includes("憑證")) {
                        const login_box = document.getElementById("login");
                        const opacity = document.querySelector(".opacity");
                        if (login_box && opacity) {
                            login_box.style.display = "block";
                            opacity.style.display = "block";
                        }
                    } else {
                        alert(result.message);
                    }
                }
            } catch (err) {
                console.error("加入失敗", err);
            }
        };
        resultsContainer.appendChild(item);
    });
    resultsContainer.style.display = 'block';
}

document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-box')) {
        resultsContainer.style.display = 'none';
    }
});
async function deleteStock(event) {

    event.stopPropagation();
    event.preventDefault();

    const deleteBtn = event.currentTarget;
    const stockNumber = deleteBtn.dataset.number;

    if (!confirm(`確定要將股票 ${stockNumber} 從觀察名單中移除嗎？`)) {
        return;
    }

    try {
        const response = await fetch(`/api/watchlist/${stockNumber}`, {
            method: 'DELETE',
        });
        const result = await response.json();

        if (result.ok) {
            alert(`✅ 成功移除股票 ${stockNumber}`);
            window.location.reload(); 
        } else if (result.error) {
            alert(`❌ 移除失敗：${result.message}`);
        }
    } catch (error) {
        console.error("刪除失敗", error);
        alert("⚠️ 系統連線異常，請稍後再試");
    }
}

document.addEventListener('DOMContentLoaded', renderWatchlist);