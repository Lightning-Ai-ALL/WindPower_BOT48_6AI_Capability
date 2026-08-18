#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTP 5.0g 真實性驗證層 · 自動升風級視覺模擬器 v1.2
© Hus Chih Li. 主權發明人 — 嚴禁外部使用、複製或商用（公開層範例）。
"""

import pygame
import math
import random
import sys
import time

# ===== 視窗與畫面常數 =====
WIDTH, HEIGHT = 1000, 650
FPS = 60
SKY = (25, 40, 60)
GROUND = (30, 55, 25)
GREEN_BASE = (50, 150, 50)

# ===== 蒲福風級標準定義 (Beaufort Scale) =====
BEAUFORT_LEVELS = {
    1: {"name": "Beaufort 1 (Light Air)", "min": 0.3, "max": 1.5, "mean": 0.9},
    2: {"name": "Beaufort 2 (Light Breeze)", "min": 1.6, "max": 3.3, "mean": 2.4},
    3: {"name": "Beaufort 3 (Gentle Breeze)", "min": 3.4, "max": 5.4, "mean": 4.4},
    4: {"name": "Beaufort 4 (Moderate Breeze)", "min": 5.5, "max": 7.9, "mean": 6.7},
    5: {"name": "Beaufort 5 (Fresh Breeze)", "min": 8.0, "max": 10.7, "mean": 9.3},
}

SIM_DURATION_SEC = 600.0  # 10 分鐘軟體持續模擬時間

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

        # 2. 相對動壓比例模型：q proportional to v^2
        base_mean = max(0.5, wind_speed_mps)
        pressure_ratio = (effective_wind / base_mean) ** 2
        pressure_ratio = max(0.0, min(3.0, pressure_ratio))

        # 3. 物理力矩與彈性回復
        torque = pressure_ratio * (self.height / 35.0) * 0.8 * 1.1
        rest_torque = -self.angle * self.stiffness * 22.0

        angular_accel = torque + rest_torque
        self.angular_vel += angular_accel * dt
        self.angular_vel *= self.damping
        self.angle += self.angular_vel * dt

        self.angle = max(-1.3, min(1.3, self.angle))

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
            r = int(GREEN_BASE[0] + 45 * ratio)
            g = int(GREEN_BASE[1] + 25 * ratio)
            b = int(GREEN_BASE[2] - 15 * ratio)
            pygame.draw.line(surface, (r, g, b), pts[i], pts[i+1], 2)

class WindField:
    """動態風場模型 (支援動態風級計算)"""
    def __init__(self):
        self.time = 0.0

    def update(self, dt):
        self.time += dt

    def get_wind_speed(self, current_mode, x_pos):
        mode_info = BEAUFORT_LEVELS[current_mode]
        mean_speed = mode_info["mean"]
        min_speed = mode_info["min"]
        max_speed = mode_info["max"]

        gust_amplitude = 1.2 if current_mode <= 2 else 1.8
        gust_low = gust_amplitude * math.sin(2 * math.pi * 0.12 * self.time)
        gust_high = 0.5 * math.sin(2 * math.pi * 0.45 * self.time + x_pos * 0.01)
        spatial_factor = 1.0 - 0.06 * (x_pos / WIDTH)

        instantaneous = (mean_speed + gust_low + gust_high) * spatial_factor
        instantaneous = max(min_speed, min(max_speed * 1.2, instantaneous))
        
        gust_factor = (gust_low + gust_high) / max(0.1, gust_amplitude)
        return instantaneous, gust_factor

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GTP 5.0g Wind Simulation v1.2 (Auto Ramp)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    field = [GrassBlade(random.randint(10, WIDTH - 10), HEIGHT - random.randint(15, 55)) for _ in range(600)]
    wind = WindField()

    observed_level = "1–2 級"
    is_paused = False
    
    start_time = time.monotonic()
    paused_elapsed = 0.0
    pause_start = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        if dt > 0.05: dt = 0.05

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_escape:
                    running = False
                elif ev.key == pygame.K_r:
                    start_time = time.monotonic()
                    paused_elapsed = 0.0
                elif ev.key == pygame.K_space:
                    is_paused = not is_paused
                    if is_paused:
                        pause_start = time.monotonic()
                    else:
                        start_time += (time.monotonic() - pause_start)

        # 計時器邏輯
        if not is_paused:
            elapsed = (time.monotonic() - start_time) + paused_elapsed
        else:
            paused_elapsed = (pause_start - start_time)
            elapsed = paused_elapsed

        remaining = max(0.0, SIM_DURATION_SEC - elapsed)

        # ===== 自動升風級核心邏輯：10 分鐘內從 1 級線性爬升到 5 級 =====
        progress = min(1.0, elapsed / SIM_DURATION_SEC)
        dynamic_level = 1.0 + 4.0 * progress
        current_mode = int(round(dynamic_level))
        current_mode = max(1, min(5, current_mode))

        if not is_paused:
            wind.update(dt)
            mode_data = BEAUFORT_LEVELS[current_mode]
            for blade in field:
                wind_speed, gust_factor = wind.get_wind_speed(current_mode, blade.x)
                spatial_offset = blade.x / WIDTH * 4.0
                blade.update(wind_speed, dt, gust_factor, spatial_offset)
        else:
            wind_speed = BEAUFORT_LEVELS[current_mode]["mean"]

        # 畫面繪製
        screen.fill(SKY)
        pygame.draw.rect(screen, GROUND, (0, HEIGHT-30, WIDTH, 30))

        for blade in field:
            blade.draw(screen)

        # ===== 資訊面板 (英文版避免行動端亂碼) =====
        panel_rect = pygame.Rect(15, 15, 460, 230)
        pygame.draw.rect(screen, (15, 25, 40, 200), panel_rect)
        pygame.draw.rect(screen, (100, 150, 200), panel_rect, 2)

        mode_name = BEAUFORT_LEVELS[current_mode]["name"]
        m_min = BEAUFORT_LEVELS[current_mode]["min"]
        m_max = BEAUFORT_LEVELS[current_mode]["max"]

        lines = [
            ("GTP 5.0g Wind Simulation v1.2 (Auto Ramp)", (255, 220, 100)),
            (f"Observed:   {observed_level}", (180, 220, 255)),
            (f"Auto Mode:  {mode_name} ({int(progress*100)}%)", (100, 255, 200)),
            (f"Wind Range: {m_min} ~ {m_max} m/s", (180, 220, 255)),
            (f"Current V:  {wind_speed:.1f} m/s", (200, 255, 150)),
            ("Physics:    Relative Dynamic Pressure (q prop to v^2)", (220, 180, 255)),
            (f"Run Time:   {int(elapsed)} / {int(SIM_DURATION_SEC)} s {'(PAUSED)' if is_paused else ''}", (255, 150, 150)),
        ]

        y_offset = 25
        for text, color in lines:
            screen.blit(font.render(text, True, color), (25, y_offset))
            y_offset += 26

        warning_text = "WARN: Auto-ramping simulation. No real environment control."
        controls_text = "[R] Reset | [SPACE] Pause | [ESC] Exit (Auto 1->5 over 10m)"
        
        screen.blit(font.render(warning_text, True, (255, 180, 100)), (15, HEIGHT - 55))
        screen.blit(font.render(controls_text, True, (150, 150, 170)), (15, HEIGHT - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTP 5.0g 真實性驗證層 · 5 級風草皮視覺模擬器 v1.1
© Hus Chih Li. 主權發明人 — 嚴禁外部使用、複製或商用（公開層範例）。
"""

import pygame
import math
import random
import sys
import time

# ===== 視窗與畫面常數 =====
WIDTH, HEIGHT = 1000, 650
FPS = 60
SKY = (25, 40, 60)
GROUND = (30, 55, 25)
GREEN_BASE = (50, 150, 50)

# ===== 蒲福風級標準定義 (Beaufort Scale) =====
BEAUFORT_LEVELS = {
    1: {"name": "Beaufort 1 (輕風)", "min": 0.3, "max": 1.5, "mean": 0.9},
    2: {"name": "Beaufort 2 (微風)", "min": 1.6, "max": 3.3, "mean": 2.4},
    3: {"name": "Beaufort 3 (和風)", "min": 3.4, "max": 5.4, "mean": 4.4},
    4: {"name": "Beaufort 4 (清風)", "min": 5.5, "max": 7.9, "mean": 6.7},
    5: {"name": "Beaufort 5 (強風)", "min": 8.0, "max": 10.7, "mean": 9.3},
}

SIM_DURATION_SEC = 600.0  # 軟體持續模擬時間：600 秒 (10分鐘)

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

        # 2. 相對動壓比例模型：q ∝ v² (以當前模式均值為基準)
        base_mean = max(0.5, wind_speed_mps)
        pressure_ratio = (effective_wind / base_mean) ** 2
        pressure_ratio = max(0.0, min(3.0, pressure_ratio))

        # 3. 物理力矩與彈性回復
        torque = pressure_ratio * (self.height / 35.0) * 0.8 * 1.1
        rest_torque = -self.angle * self.stiffness * 22.0

        angular_accel = torque + rest_torque
        self.angular_vel += angular_accel * dt
        self.angular_vel *= self.damping
        self.angle += self.angular_vel * dt

        self.angle = max(-1.3, min(1.3, self.angle))

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
            r = int(GREEN_BASE[0] + 45 * ratio)
            g = int(GREEN_BASE[1] + 25 * ratio)
            b = int(GREEN_BASE[2] - 15 * ratio)
            pygame.draw.line(surface, (r, g, b), pts[i], pts[i+1], 2)

class WindField:
    """動態風場模型 (支援多級距切換)"""
    def __init__(self):
        self.time = 0.0

    def update(self, dt):
        self.time += dt

    def get_wind_speed(self, current_mode, x_pos):
        mode_info = BEAUFORT_LEVELS[current_mode]
        mean_speed = mode_info["mean"]
        min_speed = mode_info["min"]
        max_speed = mode_info["max"]

        # 陣風與湍流計算
        gust_amplitude = 1.2 if current_mode <= 2 else 1.8
        gust_low = gust_amplitude * math.sin(2 * math.pi * 0.12 * self.time)
        gust_high = 0.5 * math.sin(2 * math.pi * 0.45 * self.time + x_pos * 0.01)
        spatial_factor = 1.0 - 0.06 * (x_pos / WIDTH)

        instantaneous = (mean_speed + gust_low + gust_high) * spatial_factor
        instantaneous = max(min_speed, min(max_speed * 1.2, instantaneous))
        
        gust_factor = (gust_low + gust_high) / max(0.1, gust_amplitude)
        return instantaneous, gust_factor

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GTP 5.0g Wind Simulation v1.1 (Realism Verification Layer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)
    font_bold = pygame.font.SysFont("monospace", 18, bold=True)

    field = [GrassBlade(random.randint(10, WIDTH - 10), HEIGHT - random.randint(15, 55)) for _ in range(600)]
    wind = WindField()

    # 狀態變數
    current_mode = 5          # 預設 Beaufort 5 模擬模式
    observed_level = "1–2 級"  # 外部真實觀測值（模擬固定）
    is_paused = False
    
    start_time = time.monotonic()
    paused_elapsed = 0.0
    pause_start = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        if dt > 0.05: dt = 0.05

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_escape:
                    running = False
                elif ev.key == pygame.K_r:
                    start_time = time.monotonic()
                    paused_elapsed = 0.0
                elif ev.key == pygame.K_space:
                    is_paused = not is_paused
                    if is_paused:
                        pause_start = time.monotonic()
                    else:
                        start_time += (time.monotonic() - pause_start)
                elif ev.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    current_mode = int(ev.unicode)

        # 計時器邏輯
        if not is_paused:
            elapsed = (time.monotonic() - start_time) + paused_elapsed
        else:
            paused_elapsed = (pause_start - start_time)
            elapsed = paused_elapsed

        remaining = max(0.0, SIM_DURATION_SEC - elapsed)

        if not is_paused:
            wind.update(dt)
            mode_data = BEAUFORT_LEVELS[current_mode]
            current_mean = mode_data["mean"]

            for blade in field:
                wind_speed, gust_factor = wind.get_wind_speed(current_mode, blade.x)
                spatial_offset = blade.x / WIDTH * 4.0
                blade.update(wind_speed, dt, gust_factor, spatial_offset)
        else:
            wind_speed = BEAUFORT_LEVELS[current_mode]["mean"]

        # 畫面繪製
        screen.fill(SKY)
        pygame.draw.rect(screen, GROUND, (0, HEIGHT-30, WIDTH, 30))

        for blade in field:
            blade.draw(screen)

        # ===== 雙欄與狀態資訊面板 (UI Overlay) =====
        panel_rect = pygame.Rect(15, 15, 420, 230)
        pygame.draw.rect(screen, (15, 25, 40, 200), panel_rect)
        pygame.draw.rect(screen, (100, 150, 200), panel_rect, 2)

        mode_name = BEAUFORT_LEVELS[current_mode]["name"]
        m_min = BEAUFORT_LEVELS[current_mode]["min"]
        m_max = BEAUFORT_LEVELS[current_mode]["max"]

        lines = [
            ("GTP 5.0g Wind Simulation v1.1", (255, 220, 100)),
            (f"氣象觀測值: {observed_level} (外部來源)", (180, 220, 255)),
            (f"模擬模式:   {mode_name}", (100, 255, 200)),
            (f"模擬風速:   {m_min} ~ {m_max} m/s", (180, 220, 255)),
            (f"瞬時風速:   {wind_speed:.1f} m/s", (200, 255, 150)),
            ("物理模型:   Relative Dynamic Pressure (q ∝ v²)", (220, 180, 255)),
            (f"軟體運行時間: {int(elapsed)} / {int(SIM_DURATION_SEC)} s {'(PAUSED)' if is_paused else ''}", (255, 150, 150)),
        ]

        y_offset = 25
        for text, color in lines:
            screen.blit(font.render(text, True, color), (25, y_offset))
            y_offset += 26

        # 底部警示與操作提示
        warning_text = "⚠ 警告：純軟體模擬，不控制實體環境 | 20-40kHz 需視音訊硬體而定"
        controls_text = "[1-5] 切換風級 | [R] 重置計時 | [SPACE] 暫停/繼續 | [ESC] 離開"
        
        screen.blit(font.render(warning_text, True, (255, 180, 100)), (15, HEIGHT - 55))
        screen.blit(font.render(controls_text, True, (150, 150, 170)), (15, HEIGHT - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
