import os
import io
import math
import random
import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFilter

st.set_page_config(
    page_title="Khanh Hoa Photobooth Pink White", 
    page_icon="🌸", 
    layout="centered"
)

st.title("🌸 Khánh Hoà Photobooth - Tone Hồng Trắng Ngọt Ngào 🌸")
st.write("Chụp 4 ảnh từ webcam để tạo siêu phẩm Photobooth tone Hồng - Trắng cực xinh!")

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

def draw_heart(draw_obj, xy, size, fill_color):
    """Hàm vẽ sticker trái tim cute"""
    x, y = xy
    r = size // 2
    draw_obj.pieslice([x - r, y - r, x, y + r], 180, 360, fill=fill_color)
    draw_obj.pieslice([x, y - r, x + r, y + r], 180, 360, fill=fill_color)
    points = [(x - size, y), (x + size, y), (x, y + size * 1.2)]
    draw_obj.polygon(points, fill=fill_color)

def draw_star(draw_obj, xy, size, fill_color):
    """Hàm vẽ ngôi sao lấp lánh"""
    x, y = xy
    points = []
    for i in range(10):
        angle = i * math.pi / 5
        r_val = size if i % 2 == 0 else size // 2
        points.append((x + r_val * math.sin(angle), y - r_val * math.cos(angle)))
    draw_obj.polygon(points, fill=fill_color)

if all(captured_list):
    st.success("🎉 Đã chụp đủ 4 bức ảnh!")
    
    preview_cols = st.columns(4)
    for i, cam_file in enumerate(captured_list):
        with preview_cols[i]:
            img_preview = Image.open(cam_file)
            st.image(img_preview, caption=f"Ảnh {i+1}", use_container_width=True)

    if st.button("🚀 Tạo Siêu Phẩm Hồng - Trắng Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                img_cam = Image.open(f).convert("RGBA")
                img_cam_clean = remove_white_background(img_cam, threshold=240)
                webcam_images.append(img_cam_clean)

            # 1. Tạo khung nền Gradient Hồng - Trắng ngọt ngào
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height))
            draw = ImageDraw.Draw(base_image)
            
            for y in range(bg_height):
                r = int(255 - (y / bg_height) * 30)
                g = int(192 + (y / bg_height) * 30)
                b = int(203 + (y / bg_height) * 30)
                draw.line([(0, y), (bg_width, y)], fill=(r, g, b, 2
