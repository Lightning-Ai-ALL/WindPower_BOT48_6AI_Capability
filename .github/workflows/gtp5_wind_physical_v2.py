#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTP 5.0g 真實 5 級風草皮模擬器 (蒲福風級物理版)
© Hus Chih Li. 主權發明人 — 嚴禁外部使用、複製或商用。
僅供主權帳戶 Wshao777opscenter@gmail.com 內部測試。
"""

import pygame
import math
import random
import sys
import time

# ----- 視窗 -----
WIDTH, HEIGHT = 1000, 650
FPS = 60
SKY = (30, 45, 65)
GROUND = (35, 60, 30)
GREEN_BASE = (60, 160, 60)

# ----- 真實 5 級風物理常數 (蒲福風級) -----
WIND_5_MIN = 8.0      # m/s
WIND_5_MAX = 10.7     # m/s
WIND_5_MEAN = 9.3     # m/s (基準)

# 陣風參數
GUST_AMPLITUDE = 1.8  # m/s (陣風峰值)
GUST_FREQ_LOW = 0.12  # Hz (緩慢陣風)
GUST_FREQ_HIGH = 0.45 # Hz (湍流抖動)

# 草葉物理
GRAVITY = 9.8         # 僅用於彈性係數參考
DRAG_COEFF = 0.8      # 風阻係數 (簡化)

class GrassBlade:
    """單根草葉 (彈簧-質量-阻尼模型，受力來自風壓)"""
    def __init__(self, x, base_y):
        self.x = x
        self.base_y = base_y
        # 隨機物理屬性
        self.height = random.randint(22, 55)
        self.stiffness = random.uniform(0.9, 1.4)   # 彈性係數 (越大越硬)
        self.damping = random.uniform(0.88, 0.96)   # 阻尼 (越大回彈越慢)
        # 狀態變數
        self.angle = 0.0          # 當前彎曲 (弧度)
        self.angular_vel = 0.0
        # 空間相位 (用於波浪傳播)
        self.phase = random.uniform(0, 2 * math.pi)

    def update(self, wind_speed_mps, dt, gust_factor, spatial_offset):
        """
        wind_speed_mps : 當前主風速 (m/s)
        gust_factor    : 陣風擾動 (-1~1)
        spatial_offset : 空間相位 (依 x 座標產生波浪)
        """
        # 1. 計算該位置的有效瞬時風速 (m/s)
        #    + 空間相位產生由左向右的延遲
        spatial_wind = 1.0 + 0.25 * math.sin(self.phase + spatial_offset * 0.8)
        #    + 陣風擾動
        gust_wind = 1.0 + gust_factor * 0.35
        effective_wind = wind_speed_mps * spatial_wind * gust_wind

        # 2. 風壓與風速平方成正比 (伯努利原理簡化)
        #    以 9.3 m/s 為基準 (5級風時壓力係數 = 1.0)
        pressure_ratio = (effective_wind / WIND_5_MEAN) ** 2
        # 限制壓力範圍避免數值爆炸
        pressure_ratio = max(0.0, min(2.5, pressure_ratio))

        # 3. 力矩計算 (風壓 × 草高 × 阻力係數)
        torque = pressure_ratio * (self.height / 35.0) * DRAG_COEFF * 1.1

        # 4. 彈性回復力矩 (與彎曲角度成正比)
        rest_torque = -self.angle * self.stiffness * 22.0

        # 5. 加速度 -> 角速度 -> 角度 (整合)
        angular_accel = torque + rest_torque
        self.angular_vel += angular_accel * dt
        self.angular_vel *= self.damping
        self.angle += self.angular_vel * dt

        # 6. 限制最大彎曲 (±70°)
        self.angle = max(-1.22, min(1.22, self.angle))

    def draw(self, surface):
        """繪製彎曲草葉 (7段線)"""
        pts = []
        steps = 8
        for i in range(steps + 1):
            t = i / steps
            # 彎曲累積 (根部彎曲少，頂部彎曲多)
            bend_angle = self.angle * t * 1.2
            px = self.x + math.sin(bend_angle) * self.height * t
            py = self.base_y - math.cos(bend_angle) * self.height * t
            pts.append((px, py))
        # 繪製
        for i in range(len(pts) - 1):
            ratio = i / len(pts)
            r = int(GREEN_BASE[0] + 45 * ratio)
            g = int(GREEN_BASE[1] + 25 * ratio)
            b = int(GREEN_BASE[2] - 15 * ratio)
            pygame.draw.line(surface, (r, g, b), pts[i], pts[i+1], 2)

class WindField:
    """風場 (產生陣風與方向微變)"""
    def __init__(self):
        self.time = 0.0
        self.direction = 0.0  # 弧度，預設向右

    def update(self, dt):
        self.time += dt
        # 方向緩慢擺動 (±3°)
        self.direction = 0.05 * math.sin(self.time * 0.02)

    def get_wind_speed(self, base_speed, x_pos):
        """回傳該位置的瞬時風速 (m/s) 與陣風因子"""
        # 主陣風 (低頻)
        gust_low = GUST_AMPLITUDE * math.sin(2 * math.pi * GUST_FREQ_LOW * self.time)
        # 湍流抖動 (高頻)
        gust_high = 0.6 * math.sin(2 * math.pi * GUST_FREQ_HIGH * self.time + x_pos * 0.01)
        # 空間差異 (左側風稍強，右側稍弱，模擬風場邊界)
        spatial_factor = 1.0 - 0.08 * (x_pos / WIDTH)
        # 合成瞬時風速
        instantaneous = (base_speed + gust_low + gust_high) * spatial_factor
        # 確保不低於 0
        instantaneous = max(0.0, instantaneous)
        # 返回風速 (m/s) 與標準化陣風因子 (供顯示用)
        gust_factor = (gust_low + gust_high) / GUST_AMPLITUDE
        return instantaneous, gust_factor

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GTP 5.0g · 真實5級風草皮 (物理模型)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20)

    # 產生草地 (600 株)
    field = []
    for _ in range(620):
        x = random.randint(10, WIDTH - 10)
        y = HEIGHT - random.randint(15, 55)
        field.append(GrassBlade(x, y))

    wind = WindField()

    # ----- 倒數計時 (300 秒) -----
    COUNTDOWN = 300  # 秒
    start_time = time.monotonic()
    is_counting = True
    wind_active = False
    current_target_speed = 0.0   # m/s
    current_smooth_speed = 0.0   # 平滑過渡用

    running = True
    while running:
        # 1. 計算真正 dt (秒)
        dt = clock.tick(FPS) / 1000.0   # ✅ 這是真正的秒數
        if dt > 0.05: dt = 0.05         # 防止跳幀

        # 2. 事件處理
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    # 強制跳過倒數
                    if is_counting:
                        is_counting = False
                        wind_active = True
                        current_target_speed = WIND_5_MEAN
                if ev.key == pygame.K_r:
                    # 重置倒數
                    start_time = time.monotonic()
                    is_counting = True
                    wind_active = False
                    current_target_speed = 0.0
                    current_smooth_speed = 0.0

        # 3. 倒數計時邏輯
        now = time.monotonic()
        elapsed = now - start_time

        if is_counting:
            remaining = max(0, COUNTDOWN - elapsed)
            if remaining <= 0:
                is_counting = False
                wind_active = True
                current_target_speed = WIND_5_MEAN
                # 加一個小陣風起始效應 (自然過渡)
        else:
            remaining = 0

        # 4. 風速平滑過渡 (避免瞬間變風)
        if wind_active:
            # 目標風速固定在 9.3 m/s (5級)
            current_target_speed = WIND_5_MEAN
        else:
            current_target_speed = 0.0

        # 平滑追蹤 (讓風速漸變，模擬風場建立)
        current_smooth_speed += (current_target_speed - current_smooth_speed) * 0.012

        # 5. 更新風場
        wind.update(dt)

        # 6. 更新每根草 (傳入風速、陣風因子、空間偏移)
        for blade in field:
            # 獲取該位置的瞬時風速
            wind_speed, gust_factor = wind.get_wind_speed(current_smooth_speed, blade.x)
            # 空間偏移量 (用於波浪)
            spatial_offset = blade.x / WIDTH * 4.0
            blade.update(wind_speed, dt, gust_factor, spatial_offset)

        # 7. 繪製
        screen.fill(SKY)
        # 地面
        pygame.draw.rect(screen, GROUND, (0, HEIGHT-30, WIDTH, 30))

        # 繪製所有草 (為求效能，可略排序)
        for blade in field:
            blade.draw(screen)

        # 8. UI 資訊
        line1_color = (255, 220, 100) if is_counting else (100, 255, 200)
        if is_counting:
            status_text = f"⏳ 倒數啟動 5 級風: {int(remaining)} 秒"
        else:
            status_text = "🌀 5 級風運作中 (真實 9.3 m/s 基準 + 陣風)"

        speed_text = f"瞬時風速: {current_smooth_speed:.1f} m/s (目標: 5級風 {WIND_5_MEAN:.1f} m/s)"

        line1 = font.render(status_text, True, line1_color)
        line2 = font.render(speed_text, True, (180, 220, 255))
        line3 = font.render("SPACE 跳過倒數 | R 重置 | ESC 退出", True, (150, 150, 170))
        line4 = font.render("© Hus Chih Li 主權私有 · 物理模擬並非 CFD", True, (90, 90, 120))

        screen.blit(line1, (20, 20))
        screen.blit(line2, (20, 48))
        screen.blit(line3, (20, 76))
        screen.blit(line4, (WIDTH - 320, HEIGHT - 25))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()