import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(
    page_title="Khánh Hoà Photobooth", 
    page_icon="💖", 
    layout="centered"
)

st.title("💖 Khánh Hoà Photobooth - Chụp Trực Tiếp")
st.write("Hãy dùng webcam chụp lần lượt **4 bức ảnh** để tạo dải Photostrip sinh nhật siêu dễ thương nhé!")

current_dir = os.path.dirname(os.path.abspath(__file__))

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Khung chụp ảnh")
    cam1 = st.camera_input("Chụp ảnh 1")
    cam2 = st.camera_input("Chụp ảnh 2")

with col2:
    st.subheader("📸 Khung chụp tiếp")
    cam3 = st.camera_input("Chụp ảnh 3")
    cam4 = st.camera_input("Chụp ảnh 4")

captured_list = [cam1, cam2, cam3, cam4]

# Kiểm tra chỉ cần đủ 4 ảnh từ webcam là hiện nút tạo ảnh (không cần file ảnh phụ nữa)
if all(captured_list):
    if st.button("✨ Tạo Dải Photostrip Ngay", type="primary"):
        webcam_images = [Image.open(f).convert("RGB") for f in captured_list]

        strip_w = 640
        card_w, card_h = 580, 150  # Thu gọn chiều cao khung card vì mỗi khung chỉ chứa 1 ảnh to
        margin_x = (strip_w - card_w) // 2
        margin_y = 15
        header_h = 130
        footer_h = 160

        strip_h = header_h + (card_h * 4) + (margin_y * 5) + footer_h

        # Nền màu TRẮNG HỒNG
        bg_pink_white = (255, 240, 245, 255)
        strip = Image.new("RGBA", (strip_w, strip_h), bg_pink_white)
        draw = ImageDraw.Draw(strip)

        stripe_w = 20
        border_pink = (255, 150, 180, 255)
        card_bg_color = (255, 255, 255, 255)
        frame_outline = (255, 105, 180, 255)
        text_pink_color = (219, 62, 115, 255)

        draw.rectangle([(0, 0), (stripe_w, strip_h)], fill=border_pink)
        draw.rectangle([(strip_w - stripe_w, 0), (strip_w, strip_h)], fill=border_pink)

        try:
            font_title = ImageFont.truetype("arialbd.ttf", 28)
            font_sub = ImageFont.truetype("arialbd.ttf", 16)
            font_wish = ImageFont.truetype("arialbd.ttf", 16)
        except IOError:
            font_title = font_sub = font_wish = ImageFont.load_default()

        def draw_flower(draw_obj, cx, cy, petal_color, center_color, size=8):
            for dx, dy in [(-size, 0), (size, 0), (0, -size), (0, size), (-size*0.7, -size*0.7), (size*0.7, size*0.7), (-size*0.7, size*0.7), (size*0.7, -size*0.7)]:
                draw_obj.ellipse([(cx + dx - size/2, cy + dy - size/2), (cx + dx + size/2, cy + dy + size/2)], fill=petal_color)
            draw_obj.ellipse([(cx - size/2, cy - size/2), (cx + size/2, cy + size/2)], fill=center_color)

        # --- PHẦN HEADER ---
        draw.text((strip_w // 2, 45), "🎉 HAPPY BIRTHDAY 🎉", fill=text_pink_color, font=font_title, anchor="mm")
        draw.text((strip_w // 2, 85), "🌸 KHÁNH HOÀ C CUTIE 🌸", fill=(255, 105, 180), font=font_sub, anchor="mm")

        draw_flower(draw, 80, 45, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=10)
        draw_flower(draw, strip_w - 80, 45, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=10)
