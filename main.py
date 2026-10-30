import tkinter as tk
from tkinter import font as tkfont
import os, sys

PISTACHIO = "#A3C585"   # سبز پسته‌ای
WHITE     = "#FFFFFF"

def resource_path(rel):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel)

class App:
    def __init__(self, root):
        self.root = root
        root.title("حرکت بدن")
        root.geometry("700x500")
        root.configure(bg=PISTACHIO)
        root.resizable(False, False)

        # فونت
        fpath = resource_path("vazirmatn.ttf")
        if os.path.exists(fpath):
            try:
                tkfont.Font(file=fpath, size=1)  # ثبت فونت
            except Exception:
                pass

        # نوشته با فید تدریجی
        self.label = tk.Label(root, text="حرکت بدن", bg=PISTACHIO, fg=WHITE,
                              font=("Vazirmatn", 44, "bold"))
        self.label.place(relx=0.5, rely=0.45, anchor="center")
        self.alpha = 0.0
        self.fade_in()

        # دکمه تست (فعلاً فقط برای اطمینان)
        tk.Button(root, text="شروع", command=self.start_animation,
                  font=("Vazirmatn", 14), bg=WHITE, fg=PISTACHIO,
                  relief="flat", padx=20, pady=6).place(relx=0.5, rely=0.7, anchor="center")

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.05
            # ترکیب رنگ سفید با پس‌زمینه برای شبیه‌سازی شفافیت
            r = int(0xA3 + (0xFF - 0xA3) * self.alpha)
            g = int(0xC5 + (0xFF - 0xC5) * self.alpha)
            b = int(0x85 + (0xFF - 0x85) * self.alpha)
            self.label.config(fg=f"#{r:02x}{g:02x}{b:02x}")
            self.root.after(40, self.fade_in)

    def start_animation(self):
        # فعلاً فقط تست: آدمک ساده روی بوم
        self.canvas = tk.Canvas(self.root, width=700, height=500,
                                bg=PISTACHIO, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.draw_stickman(350, 300)
        self.root.after(500, self.run_stickman)

    def draw_stickman(self, x, y):
        self.canvas.delete("stick")
        # سر
        self.canvas.create_oval(x-20, y-80, x+20, y-40, outline=WHITE, width=4, tags="stick")
        # تن
        self.canvas.create_line(x, y-40, x, y+20, fill=WHITE, width=4, tags="stick")
        # دست‌ها
        self.canvas.create_line(x-30, y-20, x+30, y-20, fill=WHITE, width=4, tags="stick")
        # پاها
        self.canvas.create_line(x, y+20, x-25, y+60, fill=WHITE, width=4, tags="stick")
        self.canvas.create_line(x, y+20, x+25, y+60, fill=WHITE, width=4, tags="stick")

    def run_stickman(self):
        # آدمک به سمت راست حرکت می‌کند و از کادر خارج می‌شود
        self.sx = getattr(self, "sx", 350)
        if self.sx < 750:
            self.sx += 8
            self.draw_stickman(self.sx, 300)
            self.root.after(30, self.run_stickman)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
