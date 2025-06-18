import ctypes
import tkinter as tk

# Windows APIの設定
user32 = ctypes.windll.user32
imm32 = ctypes.windll.imm32

WM_IME_CONTROL = 0x283
IME_GET_OPEN_STATUS = 0x0005

def get_ime_status():
    """アクティブウィンドウのIME状態を取得"""
    hwnd = user32.GetForegroundWindow()
    hIMEWnd = imm32.ImmGetDefaultIMEWnd(hwnd)
    if hIMEWnd:
        ime_status = user32.SendMessageW(hIMEWnd, WM_IME_CONTROL, IME_GET_OPEN_STATUS, 0)
        return f"IME: {'日本語入力ON' if ime_status else '日本語入力OFF'}"
    return "IME: 状態取得不可"

def get_key_status():
    """キーの状態を取得"""
    caps = user32.GetKeyState(0x14) & 0x0001  # Caps Lock
    num = user32.GetKeyState(0x90) & 0x0001  # Num Lock
    shift = user32.GetAsyncKeyState(0x10) & 0x8000  # Shift
    ctrl = user32.GetAsyncKeyState(0x11) & 0x8000  # Ctrl
    alt = user32.GetAsyncKeyState(0x12) & 0x8000  # Alt

    return f"Caps Lock: {'ON' if caps else 'OFF'}\n" \
           f"Num Lock: {'ON' if num else 'OFF'}\n" \
           f"Shift: {'押下中' if shift else 'OFF'}\n" \
           f"Ctrl: {'押下中' if ctrl else 'OFF'}\n" \
           f"Alt: {'押下中' if alt else 'OFF'}"

def update_status():
    """ステータス更新"""
    ime_label.config(text=get_ime_status())
    key_label.config(text=get_key_status())
    root.after(500, update_status)  # 500msごとに更新

# GUIセットアップ
root = tk.Tk()
root.title("IME & キーボードステータスモニター")
root.geometry("300x150")

ime_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
ime_label.pack(pady=5)

key_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
key_label.pack(pady=10)

update_status()
root.mainloop()
