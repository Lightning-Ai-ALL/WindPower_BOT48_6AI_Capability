#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ GTP 5.0g 防蟲震波產生器 (超音波掃頻) + Gmail 主權通知
© Hus Chih Li. 主權發明人 — 嚴禁外部使用、複製或商用。
僅供主權帳戶 Wshao777opscenter@gmail.com 內部測試。
"""

import numpy as np
import sounddevice as sd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import sys

# ===== 音頻參數 (超音波) =====
SAMPLE_RATE = 96000          # 96 kHz 取樣率 (可涵蓋 40kHz)
DURATION_SEC = 0.5           # 每次掃頻持續時間 (形成「震波脈衝」)
FREQ_MIN = 20000             # 20 kHz (人類聽不到)
FREQ_MAX = 40000             # 40 kHz (多數害蟲敏感)
AMPLITUDE = 0.5              # 音量 (0~1)，太大聲可能損壞喇叭，請謹慎

# ===== Gmail 設定 (使用應用程式密碼) =====
GMAIL_USER = "Wshao777opscenter@gmail.com"
GMAIL_PASSWORD = "你的應用程式密碼"   # ⚠️ 請替換為真實應用程式密碼 (非登入密碼)
GMAIL_TO = "Wshao777opscenter@gmail.com"

def send_gmail_alert(subject, body):
    """發送 Gmail 通知 (主權帳戶)"""
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"📧 Gmail 通知已寄出: {subject}")
    except Exception as e:
        print(f"❌ Gmail 發送失敗: {e}")

def generate_sweep(duration, fs, f_start, f_end):
    """生成線性掃頻震波 (超音波)"""
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    freq = np.linspace(f_start, f_end, len(t))
    wave = AMPLITUDE * np.sin(2 * np.pi * freq * t)
    return wave

def play_shield(stop_event):
    """播放防蟲震波 (循環掃頻)"""
    print("🛡️ 防蟲震波啟動中 (超音波 20k~40kHz 掃頻) ... 人類聽不到，請放心。")
    print("📢 按 Ctrl+C 停止並發送關閉通知。")

    while not stop_event.is_set():
        wave_up = generate_sweep(DURATION_SEC, SAMPLE_RATE, FREQ_MIN, FREQ_MAX)
        sd.play(wave_up, SAMPLE_RATE)
        sd.wait()
        if stop_event.is_set():
            break

        wave_down = generate_sweep(DURATION_SEC, SAMPLE_RATE, FREQ_MAX, FREQ_MIN)
        sd.play(wave_down, SAMPLE_RATE)
        sd.wait()
        if stop_event.is_set():
            break

        time.sleep(0.1)

def main():
    print("⚡ GTP 5.0g 防蟲震波產生器 (私有主權版)")
    print("=" * 50)

    send_gmail_alert(
        subject="🛡️ 防蟲震波已啟動 (主權帳戶)",
        body=f"時間: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
             f"頻率範圍: {FREQ_MIN/1000:.0f}kHz ~ {FREQ_MAX/1000:.0f}kHz\n"
             f"取樣率: {SAMPLE_RATE} Hz\n"
             f"狀態: 持續運作中，直到手動停止。"
    )

    stop_event = threading.Event()
    try:
        play_shield(stop_event)
    except KeyboardInterrupt:
        print("\n⏸️ 使用者中斷震波播放。")
        stop_event.set()
    finally:
        sd.stop()
        send_gmail_alert(
            subject="🛑 防蟲震波已關閉 (主權帳戶)",
            body=f"關閉時間: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                 f"總運作時長: 手動終止。"
        )
        print("✅ 防蟲震波已完全停止，Gmail 通知已發送。")

if __name__ == "__main__":
    main()
