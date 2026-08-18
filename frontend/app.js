// frontend/app.js
// ✅ 公開，不含任何 Secret
// ⚠️ 此 API 端點為「公開模擬查詢」，僅供一般使用者觸發輕量級任務。

const API_BASE = "https://api.your-private-domain.com";

async function runSimulation() {
  const mode = document.getElementById("modeSelect").value; // "NONPHYSICAL"

  const response = await fetch(`${API_BASE}/api/simulation`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode: mode })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || `HTTP ${response.status}`);
  }

  const data = await response.json();
  document.getElementById("result").textContent = JSON.stringify(data, null, 2);
}

// 綁定按鈕事件（假設 HTML 中有對應元素）
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("runBtn");
  if (btn) btn.addEventListener("click", runSimulation);
});
const API_BASE = "https://api.example.com";

async function runSimulation() {
  const response = await fetch(
    `${API_BASE}/api/simulation`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        mode: "NONPHYSICAL"
      })
    }
  );

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return response.json();

}
// frontend/app.js (新增風力與派單功能)
const API_BASE = "https://api.your-private-domain.com";

// --- 風力預測 (公開查詢) ---
async function getWindForecast() {
  const params = {
    windSpeed: document.getElementById("windSpeed").value,
    turbineId: document.getElementById("turbineId").value
  };
  
  const res = await fetch(`${API_BASE}/api/wind/forecast`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  const data = await res.json();
  // 顯示「建議調整值」與「預估電量」
  document.getElementById("forecastResult").textContent = JSON.stringify(data, null, 2);
}

// --- 派單請求 (需使用者動作觸發) ---
async function requestDispatch() {
  const payload = {
    mode: "NONPHYSICAL", // 或 REAL / SIM
    params: {
      targetPower: document.getElementById("targetPower").value,
      preferredTime: document.getElementById("timeSlot").value
    }
  };

  const res = await fetch(`${API_BASE}/api/dispatch/request`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  
  // 顯示「待審批」狀態與建議明細
  document.getElementById("dispatchResult").textContent = JSON.stringify(data, null, 2);
  // ⚠️ 前端只顯示「請求已送出」，不直接觸發設備
}
