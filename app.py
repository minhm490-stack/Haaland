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
                
                # 3. Tọa độ 4 ô trống
                box_coords = [
                    (312, 238, 497, 525),
                    (312, 574, 497, 860),
                    (536, 238, 722, 525),
                    (536, 574, 722, 860)
                ]

                # 4. Fit và dán từng ảnh vào đúng ô
                for i, img in enumerate(webcam_images):
                    box = box_coords[i]
                    bw = box[2] - box[0]
                    bh = box[3] - box[1]

                    img_fitted = ImageOps.fit(img, (bw, bh), method=Image.Resampling.LANCZOS)
                    base_image.paste(img_fitted, (box[0], box[1]))

                # 5. Hiển thị kết quả
                st.success("✨ Ghép ảnh vào khung thành công xuất sắc!")
                st.image(base_image, caption="Khung Photobooth của bạn", use_container_width=True)
                
                # Nút tải ảnh
                buf = io.BytesIO()
                base_image.convert("RGB").save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download
