import os
import io
import math
import random
import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFilter

st.set_page_config(
    page_title="Khanh Hoa Photobooth Pro Max", 
    page_icon="💖", 
    layout="centered"
)

st.title("💖 Khánh Hoà Photobooth - Siêu Phẩm Neon & Chi Tiết Sống Động 💖")
st.write("Chụp 4 ảnh từ webcam để tạo siêu phẩm Photobooth cực kỳ rực rỡ và sinh động!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Khung chụp 1")
    cam1 = st.camera_input("Ảnh 1 (Trên - Trái)")
    cam2 = st.camera_input("Ảnh 2 (Dưới - Trái)")

with col2:
    st.subheader("Khung chụp 2")
    cam3 = st.camera_input("Ảnh 3 (Trên - Phải)")
    cam4 = st.camera_input("Ảnh 4 (Dưới - Phải)")

captured_list = [cam1, cam2, cam3, cam4]

def remove_white_background(img, threshold=230):
    """Hàm tự động xóa phông nền trắng hoặc xám nhạt của sticker"""
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img

def draw_star(draw_obj, xy, size, fill_color):
    """Hàm vẽ ngôi sao trang trí sinh động"""
    x, y = xy
    points = []
    for i in range(10):
        angle = i * math.pi / 5
        r = size if i % 2 == 0 else size / 2
        points.append((x + r * math.sin(angle), y - r * math.cos(angle)))
    draw_obj.polygon(points, fill=fill_color)

if all(captured_list):
    st.success("🎉 Đã chụp đủ 4 bức ảnh!")
    
    preview_cols = st.columns(4)
    for i, cam_file in enumerate(captured_list):
        with preview_cols[i]:
            img_preview = Image.open(cam_file)
            st.image(img_preview, caption=f"Ảnh {i+1}", use_container_width=True)

    if st.button("🚀 Tạo Siêu Phẩm Cực Sống Động Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0.0)
                img_cam = Image.open(f).convert("RGBA")
                img_cam_clean = remove_white_background(img_cam, threshold=240)
                webcam_images.append(img_cam_clean)

            # 1. Tạo khung nền Gradient Xanh - Hồng neon sâu thẳm
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height))
            draw = ImageDraw.Draw(base_image)
            
            for y in range(bg_height):
                r = int(15 + (y / bg_height) * 210)
                g = int(90 - (y / bg_height) * 50)
                b = int(240 - (y / bg_height) * 30)
                draw.line([(0, y), (bg_width, y)], fill=(r, g, b, 255))

            # 2. Thêm vô số chi tiết bong bóng, ngôi sao và đốm sáng trang trí nền lung linh
            random.seed(42)  # Cố định vị trí các chi tiết cho đẹp mắt
            for _ in range(35):
                rx = random.randint(20, bg_width - 20)
                ry = random.randint(20, bg_height - 20)
                rad = random.randint(3, 8)
                color = random.choice([
                    (255, 105, 180, 200), 
                    (0, 255, 255, 200), 
                    (255, 255, 0, 200), 
                    (255, 255, 255, 180)
                ])
                draw.ellipse([rx - rad, ry - rad, rx + rad, ry + rad], fill=color)

            # Vẽ thêm các ngôi sao lấp lánh ở 4 góc viền
            star_positions = [(65, 65), (935, 65), (65, 1235), (935
