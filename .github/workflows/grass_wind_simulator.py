#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTP 5.0g 風吹草動模擬器｜私有主權版本
© Hus Chih Li. 嚴禁外部使用、複製或商用。
僅供主權帳戶 Wshao777opscenter@gmail.com 內部測試。
"""

import pygame
import math
import random
import sys

# 視窗設定
WIDTH, HEIGHT = 800, 600
FPS = 60

# 顏色
SKY = (20, 30, 50)
GRASS_COLOR = (80, 180, 80)
GRASS_DARK = (50, 130, 50)
GROUND = (40, 70, 30)

class GrassBlade:
    """單根草葉，具備慣性與風力反應"""
    def __init__(self, x, base_y, height=30):
        self.x = x
        self.base_y = base_y          # 根部 y 座標
        self.height = height
        self.angle = 0.0              # 當前彎曲角度 (弧度)
        self.angular_velocity = 0.0
        self.damping = 0.92           # 慣性阻尼
        self.stiffness = 0.03         # 回復力係數
        self.base_height = height
        # 隨機特性，讓草有自然差異
        self.stiffness += random.uniform(-0.01, 0.01)
        self.damping += random.uniform(-0.05, 0.05)

    def update(self, wind_force, dt=1.0):
        """風力影響角度，模擬擺動"""
        # 風力對草的力矩 (與高度成正比)
        torque = wind_force * (self.height / 30.0) * 0.8
        # 回復力 (彈性)
        rest_torque = -self.angle * self.stiffness * 20
        # 加速度
        acceleration = torque + rest_torque
        self.angular_velocity += acceleration * dt
        self.angular_velocity *= self.damping
        self.angle += self.angular_velocity * dt
        # 限制最大彎曲避免穿地
        self.angle = max(-0.8, min(0.8, self.angle))

    def draw(self, surface, offset_x=0, offset_y=0):
        """繪製草葉 (彎曲曲線)"""
        # 草頂座標 (根部 + 彎曲偏移)
        tip_x = self.x + math.sin(self.angle) * self.height
        tip_y = self.base_y - math.cos(self.angle) * self.height
        # 繪製一條曲線 (利用多點細分)
        points = []
        steps = 10
        for i in range(steps + 1):
            t = i / steps
            # 插值：根部到頂部，加上彎曲
            interp_x = self.x + math.sin(self.angle * t) * self.height * t
            interp_y = self.base_y - math.cos(self.angle * t) * self.height * t
            points.append((interp_x + offset_x, interp_y + offset_y))
        if len(points) > 1:
            # 漸變顏色 (根部深綠，頂部亮綠)
            for i in range(len(points)-1):
                color = (GRASS_COLOR[0] + int(40 * (i/len(points))),
                         GRASS_COLOR[1] + int(30 * (i/len(points))),
                         GRASS_COLOR[2] - int(20 * (i/len(points))))
                pygame.draw.line(surface, color, points[i], points[i+1], 2)

class GrassField:
    """一整片草地"""
    def __init__(self, num_blades=400):
        self.blades = []
        # 在視窗底部區域生成草
        for _ in range(num_blades):
            x = random.randint(20, WIDTH - 20)
            base_y = HEIGHT - random.randint(10, 40)
            height = random.randint(18, 45)
            self.blades.append(GrassBlade(x, base_y, height))
        # 風力參數 (0~1 對應 0~10 級，5 級為中風)
        self.wind_force = 0.5          # 預設 5 級
        self.target_wind = 0.5
        self.wind_smooth = 0.98

    def update(self, dt):
        # 平滑風力變化
        self.wind_force += (self.target_wind - self.wind_force) * 0.02
        for blade in self.blades:
            blade.update(self.wind_force, dt)

    def draw(self, surface):
        # 繪製地面
        pygame.draw.rect(surface, GROUND, (0, HEIGHT-20, WIDTH, 20))
        # 繪製每根草 (按 x 排序可優化，但數量不多)
        for blade in self.blades:
            blade.draw(surface)

    def set_wind_level(self, level):
        """設定風力等級 (1~10)"""
        self.target_wind = max(0.0, min(1.0, (level - 1) / 9.0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GTP 5.0g 風吹草動 (5級風) ｜私有主權")
    clock = pygame.time.Clock()

    field = GrassField(num_blades=500)
    field.set_wind_level(5)  # 初始 5 級風

    # 字體 (用於顯示風力資訊)
    font = pygame.font.SysFont("monospace", 18)

    running = True
    while running:
        dt = clock.tick(FPS) / 16.667   # 標準化時間

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # 增加風力
                    level = min(10, int((field.target_wind * 9) + 1) + 1)
                    field.set_wind_level(level)
                elif event.key == pygame.K_DOWN:
                    level = max(1, int((field.target_wind * 9) + 1) - 1)
                    field.set_wind_level(level)
                elif event.key == pygame.K_r:
                    # 重置為 5 級
                    field.set_wind_level(5)

        field.update(dt)

        # 繪製
        screen.fill(SKY)
        field.draw(screen)

        # 顯示風力資訊
        current_level = int((field.target_wind * 9) + 1)
        text = font.render(f"風力等級: {current_level}  (↑↓調整, R=重置5級)", True, (200, 200, 255))
        screen.blit(text, (20, 20))
        # 主權浮水印
        watermark = font.render("© Hus Chih Li 私有主權", True, (100, 100, 150))
        screen.blit(watermark, (WIDTH - 200, HEIGHT - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()