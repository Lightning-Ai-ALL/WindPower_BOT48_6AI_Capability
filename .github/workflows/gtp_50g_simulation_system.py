#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ GTP 5.0g 多模組協作系統 (草皮物理模擬與超音波介面基準版)
© Hus Chih Li. 主權發明人 — 嚴禁外部使用、複製或商用（公開層範例）。
"""

import pygame
import math
import random
import sys
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 01_wind_model: 蒲福風級 5 級標準物理常數
# ==========================================
WIND_5_MIN = 8.0       # m/s (5級風下限)
WIND_5_MAX = 10.7      # m/s (5級風上限)
WIND_5_MEAN = 9.3      # m/s (5級風基準均值)

# 陣風與湍流參數
GUST_AMPLITUDE = 1.8   # 陣風振幅
GUST_FREQ_LOW = 0.12   # 低頻緩慢陣風 Hz
GUST_FREQ_HIGH = 0.45  # 高頻湍流抖動 Hz

# 持續運行時間設定 (連續 10 分鐘 = 600 秒)
WIND_DURATION_SEC = 600.0

# ==========================================
# 02_ultrasound_config: 超音波參數與安全佔位符
# ==========================================
SAMPLE_RATE = 96000          # 96 kHz 取樣率
FREQ_MIN = 20000             # 20 kHz (數位訊號下限)
FREQ_MAX = 40000             # 40 kHz (數位訊號上限)
GMAIL_USER = "Wshao777opscenter@gmail.com"
GMAIL_PASSWORD = "YOUR_APP_PASSWORD_PLACEHOLDER"  # ⚠️ 開源安全隔離：使用佔位符

# ==========================================
# 03_grass_physics: 簡化動壓與彈簧模型
# ==========================================
class GrassBlade:
    """單根草葉 (彈簧-質量-阻尼模型，受力來自相對動壓比例模型)"""
    def __init__(self, x, base_y):
        self.x = x
        self.base_y = base_y
        self.height = random.randint(22, 55)
        self.stiffness = random.uniform(0.9, 1.4)   
        self.damping = random.uniform(0.88, 0.96)   
        self.angle = 0.0          
        self.angular_vel = 0.0
        self.phase = random.uniform(0, 2 * math.pi)

    def update(self, wind_speed_mps, dt, gust_factor, spatial_offset):
        # 1. 空間波浪與陣風疊加
        spatial_wind = 1.0 + 0.25 * math.sin(self.phase + spatial_offset * 0.8)
        gust_wind = 1.0 + gust_factor * 0.35
        effective_wind = wind_speed_mps * spatial_wind * gust_wind

        # 2. 相對動壓比例模型：
        #    q = 1/2 * rho * v^2
        #    在 rho 固定時，q ∝ v^2
        pressure_ratio = (effective_wind / WIND_5_MEAN) ** 2
        pressure_ratio = max(0.0, min(2.5, pressure_ratio))

        # 3. 物理力矩與彈性回復
        torque = pressure_ratio * (self.height / 35.0) * 0.8 * 1.1
        rest_torque = -self.angle * self.stiffness * 22.0

        angular_accel = torque + rest_torque
        self.angular_vel += angular_accel * dt
        self.angular_vel *= self.damping
        self.angle += self.angular_vel * dt

        # 限制彎曲角度
        self.angle = max(-1.22, min(1.22, self.angle))

    def draw(self, surface):
        pts = []
        steps = 8
        for i in range(steps + 1):
            t = i / steps
            bend_angle = self.angle * t * 1.2
            px = self.x + math.sin(bend_angle) * self.height * t
            py = self.base_y - math.cos(bend_angle) * self.height * t
            pts.append((px, py))
        for i in range(len(pts) - 1):
            ratio = i / len(pts)
            r = int(60 + 45 * ratio)
            g = int(160 + 25 * ratio)
            b = int(60 - 15 * ratio)
            pygame.draw.line(surface, (r, g, b), pts[i], pts[i+1], 2)

class WindField:
    """風場模型 (計算 8.0–10.7 m/s 範圍內的動態數值)"""
    def __init__(self):
        self.time = 0.0

    def update(self, dt):
        self.time += dt

    def get_wind_speed(self, base_speed, x_pos):
        gust_low = GUST_AMPLITUDE * math.sin(2 * math.pi * GUST_FREQ_LOW * self.time)
        gust_high = 0.6 * math.sin(2 * math.pi * GUST_FREQ_HIGH * self.time + x_pos * 0.01)
        spatial_factor = 1.0 - 0.08 * (x_pos / 1000)
        instantaneous = (base_speed + gust_low + gust_high) * spatial_factor
        instantaneous = max(WIND_5_MIN, min(WIND_5_MAX, instantaneous)) # 嚴格夾在 5 級風區間
        gust_factor = (gust_low + gust_high) / GUST_AMPLITUDE
        return instantaneous, gust_factor

# ==========================================
# 04_visualization: Pygame 視覺化主程式
# ==========================================
def main():
    pygame.init()
    width, height = 1000, 650
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("GTP 5.0g · 5級風物理近似模擬器")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 18)

    # 初始化草皮
    field = [GrassBlade(random.randint(10, width - 10), height - random.randint(15, 55)) for _ in range(600)]
    wind = WindField()

    # 軟體計時器 (monotonic 確保連續 10 分鐘計時穩定)
    start_time = time.monotonic()
    current_smooth_speed = WIND_5_MEAN

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        if dt > 0.05: dt = 0.05

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                start_time = time.monotonic() # R 鍵重置 10 分鐘計時

        # 計算 10 分鐘持續計時
        elapsed = time.monotonic() - start_time
        remaining = max(0.0, WIND_DURATION_SEC - elapsed)

        if remaining <= 0:
            # 10 分鐘結束後自動停止或循環
            running = False

        wind.update(dt)

        for blade in field:
            wind_speed, gust_factor = wind.get_wind_speed(current_smooth_speed, blade.x)
            spatial_offset = blade.x / width * 4.0
            blade.update(wind_speed, dt, gust_factor, spatial_offset)

        # 畫面繪製
        screen.fill((30, 45, 65))
        pygame.draw.rect(screen, (35, 60, 30), (0, height-30, width, 30))

        for blade in field:
            blade.draw(screen)

        # UI 狀態顯示 (嚴格標註真實性範圍)
        status_text = f"🌀 5 級風視覺／物理近似模擬中 | 剩餘持續時間: {int(remaining)} 秒"
        speed_text = f"風速範圍: {WIND_5_MIN} ~ {WIND_5_MAX} m/s (均值 {WIND_5_MEAN} m/s)"
        note_text = "⚠️ 聲明：物理模擬並非 CFD，不會產生實際室內風；超音波硬體輸出取決於裝置能力。"

        screen.blit(font.render(status_text, True, (100, 255, 200)), (20, 20))
        screen.blit(font.render(speed_text, True, (180, 220, 255)), (20, 48))
        screen.blit(font.render(note_text, True, (255, 180, 100)), (20, 76))
        screen.blit(font.render("R 重置計時 | ESC 退出", True, (150, 150, 170)), (20, height - 35))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
