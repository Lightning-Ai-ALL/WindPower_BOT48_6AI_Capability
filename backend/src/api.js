// backend/src/api.js (僅展示新增路由)

// --- 風力預測 (公開) ---
app.post('/api/wind/forecast', async (req, res) => {
  try {
    const { windSpeed, turbineId } = req.body;
    // 呼叫私有風力核心 (不洩漏模型細節)
    const forecast = await windCore.predict({ windSpeed, turbineId });
    res.json({
      status: 'ok',
      recommended_angle: forecast.bestAngle,
      estimated_power: forecast.powerKw,
      note: '此為模擬建議，實際調整請依現場規範'
    });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// --- 派單請求 (需要轉述決策，但不直接控制) ---
app.post('/api/dispatch/request', async (req, res) => {
  try {
    const { mode, params } = req.body;
    
    // 執行派單演算法 (私有核心)
    const decision = await dispatchCore.schedule({
      targetPower: params.targetPower,
      preferredTime: params.preferredTime
    });

    // ✅ 回傳「轉述結果」：建議、風險評估、待審批狀態
    res.json({
      status: 'pending_approval',   // 核心：不直接執行
      dispatch_id: decision.id,
      suggested_units: decision.units,
      estimated_time: decision.eta,
      risk_level: decision.risk,
      approval_required: true
    });
    
    // ❌ 此時「絕對不」發送任何實體控制訊號
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// --- 內部審批回調 (僅供內部系統呼叫，非公開) ---
app.post('/internal/approve_dispatch', async (req, res) => {
  // 此路由僅接受內部 Token，且記錄操作員身份
  // 通過後才呼叫安全聯鎖層
});
// backend/src/api.js (Private Server)
import express from 'express';
import cors from 'cors';
import { runHeavySimulation } from './services/gravity_float_v4.js';

const app = express();
const PORT = process.env.PORT || 3000;

// 嚴格的 CORS 設定（僅開放你的前端域名）
const allowedOrigins = ['https://your-frontend-domain.com', 'http://localhost:3000'];
app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
}));
app.use(express.json({ limit: '1mb' }));

// ---------- 公開路由（前端使用，無需 Key） ----------
// 僅供一般查詢，做速率限制（此處示意，實際可用 express-rate-limit）
app.post('/api/simulation', async (req, res) => {
  try {
    const { mode } = req.body;
    // 僅允許安全模式，阻擋極端耗時請求
    if (mode !== 'REAL' && mode !== 'SIMULATION' && mode !== 'NONPHYSICAL') {
      return res.status(400).json({ error: 'Invalid mode' });
    }

    // 呼叫輕量級或預先計算的模擬（避免暴露核心邏輯細節）
    const result = await runHeavySimulation(mode, { scale: 1 }); // 僅供展示
    res.json({ status: 'success', data: result });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ---------- 私有自動化路由（Workflow 使用，需 Bearer Token） ----------
app.post('/api/automation/run', async (req, res) => {
  // 驗證 Bearer Token
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid token' });
  }

  const token = authHeader.split(' ')[1];
  if (token !== process.env.INTERNAL_API_KEY) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  try {
    const { mode, scale } = req.body;
    // 這裡可以執行完整的 10,000× 極端實驗
    const result = await runHeavySimulation(mode, { scale: scale || 10000 });
    res.json({ status: 'success', data: result, triggered_by: 'workflow' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Private backend running on port ${PORT}`);
});
