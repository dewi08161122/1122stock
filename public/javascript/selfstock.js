let activeStockNumber = null;

function getTodayDate() {
    const today = new Date();
    return today.toISOString().split('T')[0];
}

async function renderHoldlist() {
    const holdlistBody = document.getElementById('holdlist-body');
    const loginPrompt = document.getElementById('login-prompt');
    const container = document.querySelector('.container');
    const totalValueDisplay = document.getElementById('total-value');
    const totalPnlDisplay = document.getElementById('total-pnl');

    try {
        const response = await fetch('/api/holdlist');
        const result = await response.json();

        if (result.error) {
            loginPrompt.style.display = 'flex';
            container.style.display = 'none';
            setupLoginTrigger(loginPrompt);
            return;
        }

        loginPrompt.style.display = 'none';
        container.style.display = 'block';
        
        const data = result.data;
        holdlistBody.innerHTML = '';

        if (!data || data.length === 0) {
            holdlistBody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding:50px; color:#888;">目前沒有持股，請點擊下方按鈕新增</td></tr>';
            totalValueDisplay.textContent = '0 TWD';
            totalPnlDisplay.textContent = '+0';
            totalPnlDisplay.className = 'value pnl-positive';
            return;
        }

        let grandTotalValue = 0;
        let grandTotalPnl = 0;

        data.forEach(stock => {
            grandTotalValue += stock.value;
            grandTotalPnl += stock.pnl;

            const trendClass = stock.pnl >= 0 ? 'up' : 'down';
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="font-weight:bold;">${stock.number} ${stock.name}</td>
                <td>${Number(stock.total_volume).toLocaleString()}</td>
                <td class="${trendClass}">${stock.pnl >= 0 ? '+' : ''}${Number(Math.round(stock.pnl)).toLocaleString()}</td>
                <td class="${trendClass}">${stock.roi >= 0 ? '+' : ''}${stock.roi.toFixed(2)}%</td>
                <td>${stock.avg_cos.toFixed(2)}</td>
                <td>${Number(Math.round(stock.cost)).toLocaleString()}</td>
                <td>${stock.close.toFixed(2)}</td>
                <td>${Number(Math.round(stock.value)).toLocaleString()}</td>
                <td>
                    <button class="btn-adjust" onclick="openAdjustModal('${stock.number}')">成本調整</button>
                    <button class="btn-delete-all" onclick="deleteStockAll('${stock.number}')">全刪</button>
                </td>
            `;
            holdlistBody.appendChild(row);
        });

        totalValueDisplay.textContent = `${Number(Math.round(grandTotalValue)).toLocaleString()} TWD`;
        totalPnlDisplay.className = `value ${grandTotalPnl >= 0 ? 'up' : 'down'}`;
        totalPnlDisplay.textContent = `${grandTotalPnl >= 0 ? '+' : ''}${Number(Math.round(grandTotalPnl)).toLocaleString()}`;

    } catch (error) {
        console.error("渲染持股列表錯誤:", error);
    }
}

async function openAdjustModal(number) {
    activeStockNumber = number;
    const modal = document.getElementById('adjust-modal');
    const overlay = document.getElementById('modal-overlay');
    const detailBody = document.getElementById('detail-list-body');
    const title = document.getElementById('adjust-title');

    title.textContent = `${number} 買進資訊明細`;
    detailBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">載入中...</td></tr>';

    modal.style.display = 'block';
    overlay.style.display = 'block';

    try {
        const response = await fetch(`/api/holdlist/stock/${number}`);
        const result = await response.json();

        if (result.ok) {
            detailBody.innerHTML = '';
            result.data.forEach(record => {
                const row = document.createElement('tr');
                row.id = `record-row-${record.id}`;
                row.innerHTML = `
                    <td class="col-vol">${Number(record.hold_volume).toLocaleString()}</td>
                    <td class="col-price">${Number(record.hold_price).toFixed(2)}</td>
                    <td class="col-date">${record.trade_date}</td>
                    <td class="action-cell">
                        <button class="btn-edit" onclick="editRecordRow(${record.id})">修改</button>
                        <button class="btn-delete-single" onclick="deleteSingleRecord(${record.id})">刪除</button>
                    </td>
                `;
                detailBody.appendChild(row);
            });
        }
    } catch (error) {
        console.error("獲取明細錯誤:", error);
    }
}

function editRecordRow(id) {
    const row = document.getElementById(`record-row-${id}`);
    const vol = row.querySelector('.col-vol').textContent.replace(/,/g, '');
    const price = row.querySelector('.col-price').textContent;
    const date = row.querySelector('.col-date').textContent;

    row.innerHTML = `
        <td><input type="number" class="edit-vol" value="${vol}"></td>
        <td><input type="number" step="0.1" class="edit-price" value="${price}"></td>
        <td><input type="date" class="edit-date" value="${date}" max="${getTodayDate()}"></td>
        <td class="action-cell">
            <button class="btn-confirm-edit" onclick="updateRecord(${id})">確認</button>
            <button class="btn-cancel-edit" onclick="openAdjustModal(activeStockNumber)">取消</button>
        </td>
    `;
}

async function updateRecord(id) {
    const row = document.getElementById(`record-row-${id}`);
    const newVol = row.querySelector('.edit-vol').value;
    const newPrice = row.querySelector('.edit-price').value;
    const newDate = row.querySelector('.edit-date').value;

    if (!newVol || !newPrice || !newDate) {
        alert("欄位不可空白");
        return;
    }
    
    if (newDate > getTodayDate()) {
        alert("❌ 錯誤：日期不能超過今天！");
        return;
    }

    const body = { id: id, hold_volume: parseInt(newVol), hold_price: parseFloat(newPrice), trade_date: newDate };

    try {
        const response = await fetch('/api/holdlist', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const result = await response.json();

        if (result.ok) {
            if (parseInt(newVol) === 0) alert("股數為 0，已自動刪除該筆紀錄");
            openAdjustModal(activeStockNumber); 
            renderHoldlist();
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert("更新失敗");
    }
}
async function deleteSingleRecord(id) {
    if (!confirm("確定要刪除這筆買進紀錄嗎？")) return;
    try {
        const response = await fetch(`/api/holdlist/single/${id}`, { method: 'DELETE' });
        const result = await response.json();
        if (result.ok) {
            openAdjustModal(activeStockNumber);
            renderHoldlist();
        }
    } catch (error) {
        alert("刪除失敗");
    }
}
async function deleteStockAll(number) {
    if (!confirm(`確定要刪除所有 ${number} 的持股紀錄嗎？`)) return;
    try {
        const response = await fetch(`/api/holdlist/stock/${number}`, { method: 'DELETE' });
        const result = await response.json();
        if (result.ok) {
            renderHoldlist();
        }
    } catch (error) {
        alert("刪除失敗");
    }
}

const addSearchInput = document.getElementById('add-number');
const addResultsContainer = document.getElementById('add-search-results');
let addDebounceTimer;

if (addSearchInput) {
    addSearchInput.addEventListener('input', () => {
        clearTimeout(addDebounceTimer);
        const keyword = addSearchInput.value.trim();
        if (keyword.length < 1) {
            addResultsContainer.style.display = 'none';
            return;
        }
        addDebounceTimer = setTimeout(async () => {
            const response = await fetch(`/api/searchstock?keyword=${encodeURIComponent(keyword)}`);
            const data = await response.json();
            if (data && data.length > 0) renderAddSuggestions(data);
            else addResultsContainer.style.display = 'none';
        }, 300);
    });
}
function renderAddSuggestions(stocks) {
    addResultsContainer.innerHTML = '';
    stocks.forEach(stock => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.innerHTML = `<span>${stock.number}</span> <span style="color:#aaa; font-size:12px;">${stock.name}</span>`;
        item.onclick = () => {
            addSearchInput.value = stock.number;
            addResultsContainer.style.display = 'none';
        };
        addResultsContainer.appendChild(item);
    });
    addResultsContainer.style.display = 'block';
}
function openAddModal() {
    const addDateInput = document.getElementById('add-date');
    document.getElementById('add-number').value = '';
    document.getElementById('add-volume').value = '';
    document.getElementById('add-price').value = '';
    
    const today = getTodayDate();
    addDateInput.value = today;
    addDateInput.setAttribute('max', today);
    
    if (addResultsContainer) addResultsContainer.style.display = 'none';
    document.getElementById('add-modal').style.display = 'block';
    document.getElementById('modal-overlay').style.display = 'block';
}
async function submitAddHold() {
    const number = document.getElementById('add-number').value.trim();
    const volume = document.getElementById('add-volume').value;
    const price = document.getElementById('add-price').value;
    const date = document.getElementById('add-date').value;

    if (!number || !volume || !price || !date) {
        alert("請填寫完整資訊");
        return;
    }
    
    if (date > getTodayDate()) {
        alert("❌ 錯誤：交易日期不能超過今天！");
        return;
    }

    const body = { number, hold_volume: parseInt(volume), hold_price: parseFloat(price), trade_date: date };
    const response = await fetch('/api/holdlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const result = await response.json();
    if (result.ok) {
        alert("新增成功");
        closeModals();
        renderHoldlist();
    } else alert(result.message);
}
function closeModals() {
    document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
    document.getElementById('modal-overlay').style.display = 'none';
}
function setupLoginTrigger(loginPrompt) {
    const trigger = loginPrompt.querySelector('.login-trigger');
    trigger.onclick = () => {
        const loginBox = document.getElementById("login");
        const opacity = document.querySelector(".opacity");
        if (loginBox && opacity) {
            loginBox.style.display = "block";
            opacity.style.display = "block";
        }
    };
}
document.getElementById('modal-overlay').onclick = closeModals;
document.addEventListener('click', (e) => {
    if (addResultsContainer && !e.target.closest('.input-group')) {
        addResultsContainer.style.display = 'none';
    }
});
document.addEventListener('DOMContentLoaded', renderHoldlist);