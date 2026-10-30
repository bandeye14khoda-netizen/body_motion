import tkinter as tk
import tkinter.font as tkfont
import os
import sys
import math
import random

# رنگ‌ها
PISTACHIO = "#7FA65A" 
WHITE     = "#FFFFFF"
BLACK     = "#000000"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App:
    def __init__(self, root):
        self.root = root
        root.title("حرکت بدن")
        root.geometry("800x600")
        root.configure(bg=PISTACHIO)
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=800, height=600, bg=PISTACHIO, highlightthickness=0)
        self.canvas.pack()

        # 🌟 روش مطمئن برای بارگذاری فونت در Tkinter
        font_path = resource_path("Vazirmatn-Bold.ttf")
        self.font_family = "Arial" 
        
        if os.path.exists(font_path):
            try:
                # استفاده از addfont در Tkinter
                self.root.tk.call('font', 'create', 'vazir', '-family', 'Vazirmatn')
                # ثبت فونت در سیستم ویندوز/Wine
                self.root.tk.call('font', 'configure', 'vazir', '-file', font_path)
                self.font_family = "Vazirmatn"
            except Exception as e:
                print(f"Font error: {e}")

        # متن اولیه
        self.text_item = self.canvas.create_text(400, 300, text="حرکت بدن", fill=PISTACHIO, font=(self.font_family, 80, "bold"))
        
        self.alpha = 0.0
        self.fade_in()

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.05
            r = int(0x7F + (0xFF - 0x7F) * self.alpha)
            g = int(0xA6 + (0xFF - 0xA6) * self.alpha)
            b = int(0x5A + (0xFF - 0x5A) * self.alpha)
            self.canvas.itemconfig(self.text_item, fill=f"#{r:02x}{g:02x}{b:02x}")
            self.root.after(50, self.fade_in)
        else:
            self.root.after(800, self.start_morph)

    def start_morph(self):
        self.morph_step = 0
        self.morph_total_steps = 30
        self.run_morph()

    def run_morph(self):
        if self.morph_step <= self.morph_total_steps:
            progress = self.morph_step / self.morph_total_steps
            
            # 1. متن به سیاه تغییر رنگ می‌دهد و کوچک می‌شود
            r = int(0xFF - (0xFF - 0x00) * progress)
            self.canvas.itemconfig(self.text_item, fill=f"#{r:02x}{r:02x}{r:02x}")
            current_size = int(80 - (80 * progress))
            if current_size > 1:
                self.canvas.itemconfig(self.text_item, font=(self.font_family, current_size, "bold"))
            else:
                self.canvas.delete(self.text_item)
            
            # 2. آدمک نقطه‌ای (Hologram) کم کم ظاهر می‌شود
            self.draw_dot_stickman(400, 350, progress)
            
            self.morph_step += 1
            self.root.after(30, self.run_morph)
        else:
            self.canvas.delete("stickman")
            self.root.after(1000, self.start_running)

    def draw_dot_stickman(self, x, y, progress, running=False, step=0):
        self.canvas.delete("stickman")
        if progress < 0.1: return
        
        color = BLACK
        # مختصات مفاصل
        head_y = y - 100
        neck_y = y - 70
        hip_y = y
        shoulder_y = y - 60
        
        # اندازه نقاط
        r = 4 * progress
        
        # حرکت پاها و دست‌ها اگر در حال دویدن باشد
        swing = 0
        if running:
            swing = math.sin(step * 0.4) * 25

        # لیست نقاط (سر، گردن، شانه‌ها، آرنج‌ها، دست‌ها، لگن، زانوها، پاها)
        points = [
            (x, head_y), # سر
            (x, neck_y), # گردن
            (x, hip_y),  # لگن
            (x - 25*progress, shoulder_y), # شانه چپ
            (x + 25*progress, shoulder_y), # شانه راست
            (x - 45*progress, shoulder_y + 20*progress + swing), # دست چپ
            (x + 45*progress, shoulder_y + 20*progress - swing), # دست راست
            (x - 20*progress, hip_y + 40*progress + swing), # زانوی چپ
            (x + 20*progress, hip_y + 40*progress - swing), # زانوی راست
            (x - 30*progress, hip_y + 80*progress), # پای چپ
            (x + 30*progress, hip_y + 80*progress)  # پای راست
        ]
        
        # خطوط اتصال (با نقاط کوچک پر می‌کنیم)
        lines = [(0,1), (1,2), (1,3), (1,4), (3,5), (4,6), (2,7), (2,8), (7,9), (8,10)]
        
        for start, end in lines:
            x1, y1 = points[start]
            x2, y2 = points[end]
            steps = 10 # تعداد نقاط روی خط
            for i in range(steps + 1):
                px = x1 + (x2 - x1) * (i / steps)
                py = y1 + (y2 - y1) * (i / steps)
                # اضافه کردن یک لرزش کوچک تصادفی برای حس هولوگرام
                jitter = random.uniform(-1, 1) if running else 0
                self.canvas.create_oval(px - r + jitter, py - r + jitter, px + r + jitter, py + r + jitter, fill=color, outline="", tags="stickman")
        
        # کشیدن سر
        self.canvas.create_oval(x - 20*progress, head_y - 20*progress, x + 20*progress, head_y + 20*progress, outline=color, width=3, tags="stickman")

    def start_running(self):
        self.run_step = 0
        self.run_x = 400
        self.run()

    def run(self):
        if self.run_x < 900:
            self.run_x += 12
            self.draw_dot_stickman(self.run_x, 350, 1.0, running=True, step=self.run_step)
            self.run_step += 1
            self.root.after(30, self.run)
        else:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
