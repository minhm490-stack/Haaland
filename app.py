import os
import io
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(
    page_title="Khánh Hoà Photobooth - Haaland & MCK", 
    page_icon="🔥", 
    layout="centered"
)

st.title("🔥 Khánh Hoà Photobooth - Haaland & MCK Edition 🔥")
st.write("Hãy dùng webcam chụp lần lượt **4 bức ảnh** để ghép vào khung siêu ngầu nhé!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Khung chụp 1")
    cam1 = st.camera_input("Ảnh 1 (Ô trên trái)")
    cam2 = st.camera_input("Ảnh 2 (Ô dưới trái)")

with col2:
    st.subheader("📸 Khung chụp 2")
    cam3 = st.camera_input("Ảnh 3 (Ô trên phải)")
    cam4 = st.camera_input("Ảnh 4 (Ô dưới phải)")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list):
    if st.button("✨ Ghép Ảnh Vào Khung Ngay", type="primary"):
        try:
            # 1. Đọc 4 ảnh từ webcam
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGBA"))

            # 2. Mở file khung nền
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, "khung.png")
            
            if not os.path.exists(template_path):
                st.error("⚠️ Không tìm thấy file `khung.png` trên GitHub! Hãy kiểm tra lại tên file.")
            else:
                base_image = Image.open(template_path).convert("RGBA")
                
                # 3. Tọa độ chuẩn chỉnh đã căn lại theo đúng 4 ô hồng trên khung của bạn
                # Thứ tự: [Trên-Trái, Trên-Phải, Dưới-Trái, Dưới-Phải] tương ứng với [cam1, cam3, cam2, cam4]
                # Hoặc theo thứ tự [cam1, cam2, cam3, cam4] (Trái trên, Trái dưới, Phải trên, Phải dưới):
                box_coords = [
                    (312, 238, 497, 525),  # Ảnh 1: Ô Trên-Trái
                    (312, 574, 497, 860),  # Ảnh 2: Ô Dưới-Trái
                    (536, 238, 722, 525),  # Ảnh 3: Ô Trên-Phải
                    (536, 574, 722, 860)   #
