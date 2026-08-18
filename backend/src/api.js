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
// backend/src/api.js (擴充部分)

// --- 合體協議 (Combiner Protocol) ---
app.post('/api/combiner/run', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }

  const token = authHeader.split(' ')[1];
  if (token !== process.env.INTERNAL_API_KEY) {
    return res.status(403).json({ error: 'Invalid token' });
  }

  try {
    const { mode, wind_speed, agent_chain, combine } = req.body;

    // 1. 模擬各 Agent 的獨立計算 (實際情況會各自呼叫不同微服務)
    const guardianCheck = { status: 'ok', message: '安全邊界確認：無實體控制' };
    const stormResult = { simulated_power: wind_speed * 50, status: 'generating' };
    const dispatchSuggestion = { recommended_units: ['T-01', 'T-03'], eta: '15min' };
    const reviewResult = { passed: true, notes: '邏輯一致' };

    // 2. 合體聚合 (Combiner)
    let combinedReport = {};
    if (combine) {
      combinedReport = {
        command: '合體協議完成',
        mode: mode,
        agents: agent_chain || ['Guardian', 'Storm', 'Dispatch', 'Reviewer'],
        outputs: {
          guardian: guardianCheck,
          storm: stormResult,
          dispatch: dispatchSuggestion,
          reviewer: reviewResult
        },
        combined_summary: {
          overall_status: 'SIMULATION_ONLY',
          physical_control: 'DISABLED',
          requires_approval: true,
          timestamp: new Date().toISOString()
        },
        // 標記「飛外太空」的來源
        origin: 'Private Backend (Alien Planet)'
      };
    }

    // 3. 回傳合體結果
    res.json({
      status: 'success',
      data: combinedReport,
      message: '🤖 AI 機械派系合體完成。此結果僅為模擬轉述。'
    });

  } catch (err) {
    console.error('[Combiner] Error:', err);
    res.status(500).json({ error: err.message });
  }
});
