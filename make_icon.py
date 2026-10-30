from PIL import Image, ImageDraw, ImageFont
import os

# رنگ‌ها
PISTACHIO = (163, 197, 133) # معادل #A3C585
WHITE = (255, 255, 255)

# سایزهای استاندارد برای فایل ICO ویندوز
sizes = [16, 32, 48, 64, 128, 256]
images = []

for size in sizes:
    # ساخت تصویر با پس‌زمینه سبز پسته‌ای
    img = Image.new('RGB', (size, size), PISTACHIO)
    draw = ImageDraw.Draw(img)
    
    # پیدا کردن یک فونت پیش‌فرض (چون روی سرور گیت‌هاب فونت خاصی نصب نیست، از فونت پیش‌فرض استفاده می‌کنیم)
    try:
        # تلاش برای استفاده از فونت Arial در ویندوز (سرور گیت‌هاب)
        font = ImageFont.truetype("arial.ttf", int(size * 0.7))
    except IOError:
        try:
            # فونت پیش‌فرض لینوکس
            font = ImageFont.truetype("DejaVuSans.ttf", int(size * 0.7))
        except IOError:
            # اگر هیچ فونتی پیدا نشد، از فونت پیش‌فرض خود PIL استفاده کن
            font = ImageFont.load_default()

    # متن (عدد ۵)
    text = "5"
    
    # محاسبه ابعاد متن برای قرار دادن دقیق در مرکز
    try:
        # برای نسخه‌های جدید Pillow
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top
    except AttributeError:
        # برای نسخه‌های قدیمی‌تر Pillow
        text_width, text_height = draw.textsize(text, font=font)
        
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - (size * 0.05) # کمی به بالا شیفت می‌دهیم تا در مرکز بصری قرار بگیرد
    
    # نوشتن متن سفید روی تصویر
    draw.text((x, y), text, font=font, fill=WHITE)
    
    images.append(img)

# ذخیره به عنوان فایل ico با تمام سایزها
images[0].save('icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
print("Icon created successfully: icon.ico")
