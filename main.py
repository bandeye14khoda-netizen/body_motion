import tkinter as tk
import tkinter.font as tkfont
import os
import sys
import math

# رنگ‌ها (سبز پسته‌ای پررنگ‌تر)
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

        # بارگذاری فونت وزیرمتن (دقیقاً با نام فایلی که آپلود کردید)
        font_path = resource_path("Vazirmatn-Bold.ttf")
        self.font_family = "Arial" # پیش‌فرض
        
        if os.path.exists(font_path):
            try:
                # ثبت فونت در سیستم برای استفاده در Tkinter
                tkfont.Font(file=font_path, size=10)
                self.font_family = "Vazirmatn"
            except Exception as e:
                print(f"Font loading error: {e}")

        # ایجاد متن اولیه با رنگ هم‌رنگ پس‌زمینه (برای فید شدن)
        self.text_item = self.canvas.create_text(400, 300, text="حرکت بدن", fill=PISTACHIO, font=(self.font_family, 80, "bold"))

        # شروع فید شدن (طول ۱ ثانیه = 1000 میلی‌ثانیه)
        self.alpha = 0.0
        self.fade_in()

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.05 # 20 مرحله * 50ms = 1 ثانیه
            # تبدیل تدریجی رنگ از سبز به سفید
            r = int(0x7F + (0xFF - 0x7F) * self.alpha)
            g = int(0xA6 + (0xFF - 0xA6) * self.alpha)
            b = int(0x5A + (0xFF - 0x5A) * self.alpha)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.itemconfig(self.text_item, fill=color)
            self.root.after(50, self.fade_in)
        else:
            # متن ظاهر شد، کمی صبر می‌کنیم و بعد تبدیل (Morph) را شروع می‌کنیم
            self.root.after(500, self.start_morph)

    def start_morph(self):
        # مختصات اولیه آدمک در وسط صفحه (جایی که متن بود)
        self.stickman_x = 400
        self.stickman_y = 320 # کمی پایین‌تر برای جا شدن پاها
        
        self.morph_step = 0
        self.morph_total_steps = 20 # تعداد فریم‌های انیمیشن تبدیل
        self.run_morph()

    def run_morph(self):
        if self.morph_step <= self.morph_total_steps:
            progress = self.morph_step / self.morph_total_steps
            
            # 1. رنگ متن از سفید به سیاه تغییر می‌کند
            r = int(0xFF - (0xFF - 0x00) * progress)
            g = int(0xFF - (0xFF - 0x00) * progress)
            b = int(0xFF - (0xFF - 0x00) * progress)
            self.canvas.itemconfig(self.text_item, fill=f"#{r:02x}{g:02x}{b:02x}")
            
            # 2. متن کم کم محو می‌شود (اندازه فونت کم می‌شود)
            current_size = int(80 - (80 * progress))
            if current_size > 1:
                self.canvas.itemconfig(self.text_item, font=(self.font_family, current_size, "bold"))
            else:
                self.canvas.delete(self.text_item)
            
            # 3. آدمک (به رنگ مشکی) کم کم ظاهر می‌شود
            self.draw_stickman(self.stickman_x, self.stickman_y, progress, color=BLACK)
            
            self.morph_step += 1
            self.root.after(50, self.run_morph)
        else:
            # بعد از اتمام تبدیل، ۱ ثانیه مکث و سپس دویدن
            self.canvas.delete("stickman")
            self.draw_stickman(self.stickman_x, self.stickman_y, 1.0, color=BLACK) # آدمک نهایی
            self.root.after(1000, self.start_running)

    def draw_stickman(self, x, y, progress, color):
        self.canvas.delete("stickman")
        # اندازه آدمک با پیشرفت تبدیل بزرگ می‌شود
        scale = progress 
        
        # پارامترهای آدمک (مفصل‌بندی شده)
        head_r = 25 * scale
        body_len = 70 * scale
        arm_len = 50 * scale
        leg_len = 60 * scale
        
        # سر
        self.canvas.create_oval(x - head_r, y - body_len - head_r, x + head_r, y - body_len + head_r, 
                                outline=color, width=3, tags="stickman")
        # گردن و تنه
        self.canvas.create_line(x, y - body_len + head_r, x, y, fill=color, width=3, tags="stickman")
        
        # دست‌ها (مفصل‌دار)
        # بازوی راست: از شانه به سمت راست و پایین
        self.canvas.create_line(x, y - body_len/2, x + arm_len, y - body_len/2 + (arm_len/2), fill=color, width=3, tags="stickman")
        # بازوی چپ: از شانه به سمت چپ و پایین
        self.canvas.create_line(x, y - body_len/2, x - arm_len, y - body_len/2 + (arm_len/2), fill=color, width=3, tags="stickman")
        
        # پاها (مفصل‌دار)
        # پای راست
        self.canvas.create_line(x, y, x + leg_len/1.5, y + leg_len, fill=color, width=3, tags="stickman")
        # پای چپ
        self.canvas.create_line(x, y, x - leg_len/1.5, y + leg_len, fill=color, width=3, tags="stickman")

    def start_running(self):
        self.canvas.delete("stickman")
        self.run_step = 0
        self.run_x = self.stickman_x
        self.run()

    def run(self):
        if self.run_x < 900: # تا خارج شدن از کادر
            self.run_x += 10
            self.draw_running_stickman(self.run_x, 320, self.run_step)
            self.run_step += 1
            self.root.after(40, self.run)
        else:
            # وقتی خارج شد، برنامه متوقف می‌شود (یا می‌توانید دکمه خروج بگذارید)
            pass

    def draw_running_stickman(self, x, y, step):
        self.canvas.delete("stickman")
        color = BLACK
        head_r = 25
        body_len = 70
        arm_len = 50
        leg_len = 60
        
        # حرکت دادن پاها و دست‌ها با استفاده از سینوس (برای حالت دویدن)
        swing = math.sin(step * 0.5) * 20 
        
        # سر
        self.canvas.create_oval(x - head_r, y - body_len - head_r, x + head_r, y - body_len + head_r, outline=color, width=3, tags="stickman")
        # تنه
        self.canvas.create_line(x, y - body_len + head_r, x, y, fill=color, width=3, tags="stickman")
        # دست‌ها (حرکت متضاد)
        self.canvas.create_line(x, y - body_len/2, x + arm_len, y - body_len/2 - swing, fill=color, width=3, tags="stickman")
        self.canvas.create_line(x, y - body_len/2, x - arm_len, y - body_len/2 + swing, fill=color, width=3, tags="stickman")
        # پاها (حرکت متضاد)
        self.canvas.create_line(x, y, x + leg_len/1.5 + swing/2, y + leg_len - swing/2, fill=color, width=3, tags="stickman")
        self.canvas.create_line(x, y, x - leg_len/1.5 - swing/2, y + leg_len + swing/2, fill=color, width=3, tags="stickman")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
