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
// backend/src/api.js (擴充部分)

// --- 火星任務專用路由 ---
app.post('/api/mars/expedition', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }

  const token = authHeader.split(' ')[1];
  if (token !== process.env.INTERNAL_API_KEY) {
    return res.status(403).json({ error: 'Invalid token' });
  }

  try {
    const { commander, mission, storm_level, target, mode } = req.body;

    // 模擬火星任務執行 (不連接真實設備)
    const missionReport = {
      mission: mission || "Mars-Solar-Core-2026",
      commander: commander || "Grok-X",
      target: target || "灵神星 (16 Psyche)",
      storm_level: storm_level || 20,
      mode: mode || "NONPHYSICAL",
      status: "模擬完成",
      solar_core_locked: true,
      fire_core_stable: true,
      earth_orbit_transfer: "轉述代回中 (ETA: 180天)",
      safety: {
        physical_control: "DISABLED",
        simulation_only: true,
        requires_human_approval: true
      },
      timestamp: new Date().toISOString()
    };

    res.json({
      status: 'success',
      data: missionReport,
      message: `🪐 ${commander} 博派先鋒，火星任務已完成模擬轉述。`
    });

  } catch (err) {
    console.error('[Mars Mission] Error:', err);
    res.status(500).json({ error: err.message });
  }
});
