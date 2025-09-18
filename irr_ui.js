/**
 * IRR 計算器 UI 交互邏輯
 * 保留原有的界面功能，移除計算邏輯
 */

// --------------------------------------------------
// 用戶界面交互函數
// --------------------------------------------------

/**
 * 切換輸入模式（每年不同 vs 年份範圍攤平 vs 以KW計算）
 * @param {string} type - 模式類型（income, interest, rent等）
 */
function toggle_mode(type) {
    const yearly_div = document.getElementById(`${type}_yearly`);
    const range_div = document.getElementById(`${type}_range`);
    const kw_div = document.getElementById(`${type}_kw_based`);
    const selected_mode = document.querySelector(`input[name="${type}_mode"]:checked`).value;

    console.log(`切換 ${type} 模式到: ${selected_mode}`);

    // 隱藏所有模式
    if (yearly_div) yearly_div.classList.add('hidden');
    if (range_div) range_div.classList.add('hidden');
    if (kw_div) kw_div.classList.add('hidden');

    // 顯示選中的模式
    if (selected_mode === 'yearly' && yearly_div) {
        yearly_div.classList.remove('hidden');
    } else if (selected_mode === 'range' && range_div) {
        range_div.classList.remove('hidden');
        initializeRangeSliders(type);
    } else if (selected_mode === 'kw_based' && kw_div) {
        kw_div.classList.remove('hidden');
        initializeRangeSliders(`${type}_kw`);
    }
}

/**
 * 初始化年份範圍調整桿
 * @param {string} prefix - 前綴名稱
 */
function initializeRangeSliders(prefix) {
    const startYear = parseInt(document.getElementById('start_year').value) || 2025;
    const endYear = parseInt(document.getElementById('end_year').value) || 2030;

    // 更新調整桿的最小最大值
    const startRange = document.getElementById(`${prefix}_start_range`);
    const endRange = document.getElementById(`${prefix}_end_range`);
    const startInput = document.getElementById(`${prefix}_start_year`);
    const endInput = document.getElementById(`${prefix}_end_year`);

    if (startRange && endRange && startInput && endInput) {
        [startRange, endRange].forEach(slider => {
            slider.min = startYear;
            slider.max = endYear;
            slider.value = slider.id.includes('start') ? startYear : endYear;
        });

        startInput.min = startYear;
        startInput.max = endYear;
        startInput.value = startYear;

        endInput.min = startYear;
        endInput.max = endYear;
        endInput.value = endYear;
    }
}

/**
 * 更新範圍顯示（調整桿改變時）
 * @param {string} prefix - 前綴名稱
 */
function updateRangeDisplay(prefix) {
    const startRange = document.getElementById(`${prefix}_start_range`);
    const endRange = document.getElementById(`${prefix}_end_range`);
    const startInput = document.getElementById(`${prefix}_start_year`);
    const endInput = document.getElementById(`${prefix}_end_year`);

    if (startRange && endRange && startInput && endInput) {
        let startVal = parseInt(startRange.value);
        let endVal = parseInt(endRange.value);

        // 確保開始年份不超過結束年份
        if (startVal > endVal) {
            if (startRange === document.activeElement) {
                endVal = startVal;
                endRange.value = startVal;
            } else {
                startVal = endVal;
                startRange.value = endVal;
            }
        }

        // 更新輸入框
        startInput.value = startVal;
        endInput.value = endVal;

        console.log(`${prefix} 年份範圍: ${startVal} - ${endVal}`);
    }
}

/**
 * 從輸入框更新調整桿（輸入框改變時）
 * @param {string} prefix - 前綴名稱
 */
function updateRangeFromInput(prefix) {
    const startRange = document.getElementById(`${prefix}_start_range`);
    const endRange = document.getElementById(`${prefix}_end_range`);
    const startInput = document.getElementById(`${prefix}_start_year`);
    const endInput = document.getElementById(`${prefix}_end_year`);

    if (startRange && endRange && startInput && endInput) {
        let startVal = parseInt(startInput.value);
        let endVal = parseInt(endInput.value);

        const minYear = parseInt(startInput.min);
        const maxYear = parseInt(startInput.max);

        // 驗證輸入範圍
        startVal = Math.max(minYear, Math.min(maxYear, startVal || minYear));
        endVal = Math.max(minYear, Math.min(maxYear, endVal || maxYear));

        // 確保開始年份不超過結束年份
        if (startVal > endVal) {
            if (startInput === document.activeElement) {
                endVal = startVal;
                endInput.value = startVal;
            } else {
                startVal = endVal;
                startInput.value = endVal;
            }
        }

        // 更新調整桿
        startRange.value = startVal;
        endRange.value = endVal;

        console.log(`${prefix} 年份範圍更新: ${startVal} - ${endVal}`);
    }
}

// --------------------------------------------------
// 頁面初始化和事件處理
// --------------------------------------------------

/**
 * 頁面載入完成後的初始化函數
 */
document.addEventListener('DOMContentLoaded', function() {
    // 初始化設備費用計算
    calculate_equipment_cost();

    console.log('IRR 計算器載入完成 - API 版本');

    // 檢查 API 連接狀態
    checkAPIConnection();
});

/**
 * 檢查 API 連接狀態
 */
async function checkAPIConnection() {
    try {
        await apiClient.healthCheck();
        console.log('✅ Flask API 連接正常');
    } catch (error) {
        console.warn('⚠️ Flask API 連接失敗:', error);

        // 在界面上顯示警告
        const result_container = document.getElementById('result_container');
        result_container.innerHTML = `
            <div class="error">
                <h3>⚠️ 後端連接異常</h3>
                <p>請確保 Flask 服務器正在運行 (http://localhost:5000)</p>
                <p>錯誤詳情: ${error.message}</p>
            </div>
        `;
    }
}

// --------------------------------------------------
// 調試和輔助函數
// --------------------------------------------------

/**
 * 輸出當前所有輸入數據（用於調試）
 */
function debug_print_all_inputs() {
    console.log('=== 當前輸入數據 ===');
    console.log('年度範圍:', {
        start: document.getElementById('start_year').value,
        end: document.getElementById('end_year').value
    });
    console.log('設備費用參數:', {
        capacity: document.getElementById('capacity').value,
        price_per_kw: document.getElementById('price_per_kw').value,
        profit_rate: document.getElementById('profit_rate').value,
        development_fee: document.getElementById('development_fee').value
    });
    console.log('所得稅率:', document.getElementById('tax_rate').value);
    console.log('==================');
}

/**
 * 測試 API 連接
 */
async function test_api_connection() {
    try {
        const response = await apiClient.healthCheck();
        console.log('API 健康檢查回應:', response);
        alert('API 連接正常！');
    } catch (error) {
        console.error('API 連接測試失敗:', error);
        alert(`API 連接失敗: ${error.message}`);
    }
}

/**
 * 切換利息計算模式（無利息 vs 銀行貸款）
 */
function toggle_interest_mode() {
    const checkbox = document.getElementById('no_interest_checkbox');
    const bankLoanParams = document.getElementById('bank_loan_params');

    if (checkbox.checked) {
        // 選擇無利息，隱藏銀行貸款參數
        bankLoanParams.style.display = 'none';
        console.log('利息模式: 無利息');
    } else {
        // 取消無利息，顯示銀行貸款參數
        bankLoanParams.style.display = 'block';
        console.log('利息模式: 銀行貸款');
    }
}

// 在全域添加測試函數，方便開發時調用
window.debug_print_all_inputs = debug_print_all_inputs;
window.test_api_connection = test_api_connection;