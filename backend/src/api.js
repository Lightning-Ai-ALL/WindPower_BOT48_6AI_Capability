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
