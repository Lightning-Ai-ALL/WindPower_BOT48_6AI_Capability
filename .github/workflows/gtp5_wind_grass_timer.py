#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTP 5.0g 風吹草動模擬器｜倒數計時啟動版 (5級風真實物理)
© Hus Chih Li. 主權發明人 — 嚴禁外部使用、複製或商用。
僅供主權帳戶 Wshao777opscenter@gmail.com 內部測試。
"""

import pygame
import math
import random
import sys
import time

# ----- 視窗與顯示設定 -----
WIDTH, HEIGHT = 900, 600
FPS = 60
SKY_COLOR = (25, 40, 60)
GROUND_COLOR = (35, 65, 25)
GRASS_GREEN = (70, 170, 70)
GRASS_DARK = (50, 130, 50)

# ----- 物理常數 (對應真實風力) -----
# 5級風平均風速 9 m/s，此處映射為 wind_force 0.0~1.0
# 陣風強度 (變異範圍)
GUST_AMPLITUDE = 0.25
GUST_FREQUENCY = 0.15   # Hz

class GrassBlade:
    """單根草葉（彈簧‑質量模型 + 風力驅動）"""
    def __init__(self, x, base_y, height, stiffness, damping, phase_offset):
        self.x = x
        self.base_y = base_y
        self.height = height
        self.angle = 0.0
        self.angular_vel = 0.0
        self.stiffness = stiffness          # 回復力係數
        self.damping = damping              # 阻尼係數
        self.phase_offset = phase_offset    # 用於波浪傳播

    def update(self, wind_force, dt, gust_factor=0.0):
        """
        wind_force: 主風力 (0~1)
        gust_factor: 陣風瞬時增量 (-0.2 ~ +0.2)
        """
        # 有效風力 = 主風力 + 陣風擾動，並考慮相位延遲 (波浪)
        effective_wind = wind_force + gust_factor * 0.5
        # 加上相位偏移，產生由左至右的波浪
        phase_wind = effective_wind * (1.0 + 0.3 * math.sin(self.phase_offset))
        # 風力產生的力矩 (與草高成正比)
        torque = phase_wind * (self.height / 35.0) * 1.2
        # 彈性回復力矩
        rest_torque = -self.angle * self.stiffness * 25.0
        # 加速度
        accel = torque + rest_torque
        self.angular_vel += accel * dt
        self.angular_vel *= self.damping
        self.angle += self.angular_vel * dt
        # 限制最大彎曲 (-70° ~ 70°)
        self.angle = max(-1.2, min(1.2, self.angle))

    def draw(self, surface, offset_x=0, offset_y=0):
        """繪製彎曲草葉 (分段直線)"""
        points = []
        steps = 12
        for i in range(steps + 1):
            t = i / steps
            # 彎曲隨高度增加而累積
            bend = math.sin(self.angle * t) * self.height * t * 0.7
            px = self.x + bend + offset_x
            py = self.base_y - math.cos(self.angle * t) * self.height * t + offset_y
            points.append((px, py))
        if len(points) > 1:
            for i in range(len(points)-1):
                # 漸變顏色：根部深綠 → 頂部亮綠
                ratio = i / len(points)
                r = int(GRASS_GREEN[0] + 40 * ratio)
                g = int(GRASS_GREEN[1] + 30 * ratio)
                b = int(GRASS_GREEN[2] - 20 * ratio)
                pygame.draw.line(surface, (r, g, b), points[i], points[i+1], 2)

class GrassField:
    def __init__(self, num_blades=500):
        self.blades = []
        for _ in range(num_blades):
            x = random.randint(20, WIDTH - 20)
            base_y = HEIGHT - random.randint(10, 50)
            h = random.randint(20, 50)
            stiff = random.uniform(0.8, 1.2)   # 剛性差異
            damp = random.uniform(0.90, 0.97)  # 阻尼差異
            phase = random.uniform(0, 2*math.pi)  # 初始相位
            self.blades.append(GrassBlade(x, base_y, h, stiff, damp, phase))

        # 風力狀態
        self.main_wind = 0.0          # 目標主風力 (0~1)
        self.current_wind = 0.0       # 實際平滑後風力
        self.gust_time = 0.0

    def set_wind_level(self, level):
        """設定風力等級 (0~10)，此處使用 0~1 映射"""
        self.main_wind = max(0.0, min(1.0, level / 10.0))

    def update(self, dt, elapsed_time):
        # 陣風產生 (利用正弦波模擬)
        self.gust_time += dt
        gust = GUST_AMPLITUDE * math.sin(2 * math.pi * GUST_FREQUENCY * self.gust_time)
        # 額外高頻抖動 (湍流)
        gust += 0.08 * math.sin(12.7 * self.gust_time)

        # 平滑追蹤目標風力 (避免突變)
        self.current_wind += (self.main_wind - self.current_wind) * 0.015

        # 更新每一根草
        for blade in self.blades:
            blade.update(self.current_wind, dt, gust)

    def draw(self, surface):
        # 繪製地面
        pygame.draw.rect(surface, GROUND_COLOR, (0, HEIGHT-25, WIDTH, 25))
        # 繪製草 (依 x 排序可優化，此處不排序)
        for blade in self.blades:
            blade.draw(surface)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GTP 5.0g 風吹草動 · 300秒倒數啟動 (5級風)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 22)

    field = GrassField(num_blades=600)

    # ----- 倒數計時參數 -----
    COUNTDOWN_SECONDS = 300   # 5 分鐘
    start_time = time.monotonic()
    countdown_active = True
    wind_started = False

    running = True
    while running:
        dt = clock.tick(FPS) / 16.667   # 標準化增量

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 手動重置倒數 (測試用)
                    start_time = time.monotonic()
                    countdown_active = True
                    wind_started = False
                    field.set_wind_level(0)
                elif event.key == pygame.K_SPACE:
                    # 強制立即啟動 (跳過倒數)
                    countdown_active = False
                    wind_started = True
                    field.set_wind_level(5)

        # 計算已過時間
        now = time.monotonic()
        elapsed = now - start_time

        # 倒數邏輯
        if countdown_active:
            remaining = max(0, COUNTDOWN_SECONDS - elapsed)
            if remaining <= 0:
                countdown_active = False
                wind_started = True
                field.set_wind_level(5)   # 設定為 5 級風
                # 並將主風力逐步提升 (由 update 平滑過渡)
        else:
            remaining = 0

        # 若尚未啟動，風力保持 0
        if not wind_started:
            field.set_wind_level(0)

        # 更新物理 (每幀)
        field.update(dt, elapsed)

        # ----- 繪製 -----
        screen.fill(SKY_COLOR)
        field.draw(screen)

        # ----- UI 資訊 -----
        if countdown_active:
            # 顯示倒數秒數
            count_text = f"⏳ 倒數啟動: {int(remaining)} 秒 (5級風待機)"
            color = (255, 200, 100)
        else:
            if wind_started:
                count_text = "🌀 5級風運作中 (陣風 + 波浪)"
                color = (100, 255, 180)
            else:
                count_text = "⚡ 風力關閉"
                color = (150, 150, 150)

        # 風力強度指示
        wind_level = int(field.current_wind * 10)
        wind_text = f"風力等級: {wind_level} / 10"

        # 顯示文字
        line1 = font.render(count_text, True, color)
        line2 = font.render(wind_text, True, (200, 200, 220))
        line3 = font.render("按 R 重置倒數 | SPACE 強制啟動", True, (160, 160, 180))
        line4 = font.render("© Hus Chih Li 主權私有", True, (100, 100, 140))

        screen.blit(line1, (20, 20))
        screen.blit(line2, (20, 50))
        screen.blit(line3, (20, 80))
        screen.blit(line4, (WIDTH - 220, HEIGHT - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()