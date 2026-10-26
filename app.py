import os
import io
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(
    page_title="Khanh Hoa Photobooth", 
    page_icon="🔥", 
    layout="centered"
)

st.title("Khanh Hoa Photobooth - Haaland & MCK")
st.write("Hãy dùng webcam chụp lần lượt 4 bức ảnh để ghép vào khung!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Khung chụp 1")
    cam1 = st.camera_input("Ảnh 1 (Trên trái)")
    cam2 = st.camera_input("Ảnh 2 (Dưới trái)")

with col2:
    st.subheader("Khung chụp 2")
    cam3 = st.camera_input("Ảnh 3 (Trên phải)")
    cam4 = st.camera_input("Ảnh 4 (Dưới phải)")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list):
    if st.button("Ghép Ảnh Vào Khung Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGBA"))

            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, "khung.png")
            
            if not os.path.exists(template_path):
                st.error("Không tìm thấy file khung.png trong thư mục!")
            else:
                base_image = Image.open(template_path).convert("RGBA")
                
                # Lấy kích thước gốc của khung để đồng bộ tỉ lệ tuyệt đối
                base_w, base_h = base_image.size

                # Tọa độ 4 ô chữ nhật đứng chuẩn xác (y_min, x_min, y_max, x_max)
                box_coords = [
                    (275, 305, 475, 500),  # Ô trên - trái
                    (275, 560, 475, 755),  # Ô trên - phải
                    (495, 305, 695, 500),  # Ô dưới - trái
                    (495, 560, 695, 755)   # Ô dưới - phải
                ]

                for i, img in enumerate(webcam_images):
                    y_min, x_min, y_max, x_max = box_coords[i]
                    
                    # Tính toán chính xác chiều rộng và chiều cao của khung hình chữ nhật
                    bw = x_max - x_min
                    bh = y_max - y_min

                    # Fit ảnh webcam theo đúng tỉ lệ (width, height) của ô khung với độ nét cao (LANCZOS)
                    img_fitted = ImageOps.fit(img, (bw, bh), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                    
                    # Dán ảnh vào đúng vị trí (x_min, y_min) trên khung nền
                    base_image.paste(img_fitted, (x_min, y_min))

                st.success("Ghép ảnh thành công!")
                st.image(base_image, caption="Photobooth của bạn", use_container_width=True
