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
