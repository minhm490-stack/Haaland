import os
import io
import streamlit as st
from PIL import Image, ImageOps, ImageDraw

st.set_page_config(
    page_title="Khanh Hoa Photobooth Pro", 
    page_icon="💖", 
    layout="centered"
)

st.title("💖 Khánh Hoà Photobooth - Xanh Hồng Xịn Xò 💖")
st.write("Chụp 4 ảnh từ webcam để tạo siêu phẩm Photobooth tone Xanh-Hồng cực chất!")

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
    """Hàm tự động biến nền trắng hoặc xám nhạt thành trong suốt (xóa phong nền)"""
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        # Nếu điểm ảnh có màu sáng (gần trắng), chuyển nó thành trong suốt hoàn toàn
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img

if all(captured_list):
    st.success("🎉 Đã chụp đủ 4 bức ảnh!")
    
    preview_cols = st.columns(4)
    for i, cam_file in enumerate(captured_list):
        with preview_cols[i]:
            img_preview = Image.open(cam_file)
            st.image(img_preview, caption=f"Ảnh {i+1}", use_container_width=True)

    if st.button("🚀 Tạo Siêu Phẩm Xanh - Hồng Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                # Đọc ảnh webcam và tự động xóa phông nền trắng/sáng xung quanh người
                img_cam = Image.open(f).convert("RGBA")
                img_cam_clean = remove_white_background(img_cam, threshold=240)
                webcam_images.append(img_cam_clean)

            # 1. Tạo hiệu ứng nền Gradient Xanh dương - Hồng neon cực kỳ xịn xò
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height))
            draw = ImageDraw.Draw(base_image)
            
            for y in range(bg_height):
                # Chuyển sắc mượt mà từ Xanh đậm ở trên sang Hồng tím ở dưới
                r = int(30 + (y / bg_height) * 190)
                g = int(144 - (y / bg_height) * 80)
                b = int(255 - (y / bg_height) * 50)
                draw.line([(0, y), (bg_width, y)], fill=(r, g, b, 255))

            # Vẽ viền phong cách neon nghệ thuật
            draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 255, 255, 255), width=10)
            draw.rectangle([(45, 45), (bg_width - 45, bg_height - 45)], outline=(255, 105, 180, 255), width=4)

            # 2. Tọa độ 4 ô chứa ảnh
            box_coords = [
                (100, 150, 470, 680),   # Ô 1: Trên - Trái
                (530, 150, 900
