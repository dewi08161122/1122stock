async function fetchCategories() {
    const response = await fetch("/api/stockcategory",{
        method:"GET"
    });
    const data = await response.json();
    const container = document.getElementById("category-container");
    container.innerHTML = ""; 

    data.forEach(item => {
        const div = document.createElement("div");
        div.className = "category-item";
        div.textContent = item.category_name; 
        div.onclick = async() => {
            const response = await fetch(`/api/categorystock?category_name=${item.category_name}`);
            const data = await response.json();
            if (data.error) {
                alert(data.message);
                return;
            }
            const resultArea = document.getElementById("stock-result-area");
            resultArea.style.display = "block";
            const titleBox = document.getElementById("category-title");
            titleBox.textContent = `${item.category_name}：共 ${data.length} 檔`;
            renderStocks(data);
        };

        container.appendChild(div);
    });

}
fetchCategories()

function renderStocks(stocks) {
    const stockContainer = document.getElementById("stock-container");
    stockContainer.innerHTML = "";
    stocks.forEach(s => {
        const stockDiv = document.createElement("div");
        stockDiv.className = "stock-item";
        stockDiv.textContent = `${s.number} ${s.name}`;
        stockDiv.onclick = () => {
            window.location.href = `/stock/${s.number}`;
        };
        stockContainer.appendChild(stockDiv);
    });
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
        item.innerHTML = `<span>${stock.number}</span> <span>${stock.name}</span>`;
        
        // 點擊後跳轉到該股票 K 線頁面
        item.onclick = () => {
            window.location.href = `/stock/${stock.number}`;
        };
        resultsContainer.appendChild(item);
    });
    resultsContainer.style.display = 'block';
}

// 點擊頁面其他地方時隱藏選單
document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-box')) {
        resultsContainer.style.display = 'none';
    }
});