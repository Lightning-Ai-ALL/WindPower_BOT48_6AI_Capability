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
