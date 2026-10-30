import tkinter as tk
from tkinter import font as tkfont
import os, sys

PISTACHIO = "#A3C585"
WHITE     = "#FFFFFF"

class App:
    def __init__(self, root):
        self.root = root
        root.title("حرکت بدن")
        root.geometry("700x500")
        root.configure(bg=PISTACHIO)
        root.resizable(False, False)

        # بوم (Canvas) برای کشیدن انیمیشن‌ها
        self.canvas = tk.Canvas(root, width=700, height=500, bg=PISTACHIO, highlightthickness=0)
        self.canvas.pack()

        # تنظیمات فید شدن متن
        self.alpha = 0.0
        self.text_item = self.canvas.create_text(350, 250, text="حرکت بدن", fill=PISTACHIO, font=("Arial", 48, "bold"))

        # شروع انیمیشن
        self.fade_in()

    def fade_in(self):
        # متن کم‌کم سفید می‌شود
        if self.alpha < 1.0:
            self.alpha += 0.05
            r = int(0xA3 + (0xFF - 0xA3) * self.alpha)
            g = int(0xC5 + (0xFF - 0xC5) * self.alpha)
            b = int(0x85 + (0xFF - 0x85) * self.alpha)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.itemconfig(self.text_item, fill=color)
            self.root.after(40, self.fade_in)
        else:
            # بعد از کامل شدن متن، کمی صبر می‌کنیم و بعد تبدیل به آدمک می‌کنیم
            self.root.after(1000, self.transform_to_stickman)

    def transform_to_stickman(self):
        # متن را پاک می‌کنیم
        self.canvas.delete(self.text_item)
        
        # مختصات شروع آدمک در وسط صفحه
        self.stickman_x = 350
        self.stickman_y = 250
        
        # کشیدن آدمک
        self.draw_stickman()
        
        # شروع دویدن بعد از نیم ثانیه
        self.root.after(500, self.run)

    def draw_stickman(self):
        self.canvas.delete("stickman")
        x, y = self.stickman_x, self.stickman_y
        
        # سر
        self.canvas.create_oval(x-20, y-80, x+20, y-40, outline=WHITE, width=4, tags="stickman")
        # تن
        self.canvas.create_line(x, y-40, x, y+20, fill=WHITE, width=4, tags="stickman")
        # دست‌ها
        self.canvas.create_line(x-30, y-20, x+30, y-20, fill=WHITE, width=4, tags="stickman")
        # پاها
        self.canvas.create_line(x, y+20, x-25, y+60, fill=WHITE, width=4, tags="stickman")
        self.canvas.create_line(x, y+20, x+25, y+60, fill=WHITE, width=4, tags="stickman")

    def run(self):
        # حرکت آدمک به سمت راست
        if self.stickman_x < 750:
            self.stickman_x += 8
            self.draw_stickman()
            self.root.after(30, self.run)
        else:
            # وقتی از کادر خارج شد، فعلاً متوقف می‌شود
            pass

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
