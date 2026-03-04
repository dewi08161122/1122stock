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