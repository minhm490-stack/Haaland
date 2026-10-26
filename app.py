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

            # 2. Mở file khung nền (khung.png phải nằm cùng thư mục trên GitHub)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, "khung.png")
            
            if not os.path.exists(template_path):
                st.error("⚠️ Không tìm thấy file `khung.png` trên GitHub! Hãy kiểm tra lại tên file.")
            else:
                base_image = Image.open(template_path).convert("RGBA")
                
                # 3. Tọa độ chính xác cho 4 ô trống trong khung của bạn (Thứ tự: Trên-Trái, Dưới-Trái, Trên-Phải, Dưới-Phải)
                # (x_start, y_start, x_end, y_end)
                box_coords = [
                    (304, 235, 477, 529),  # Ô 1: Trên Trái
                    (304, 584, 477, 873),  # Ô 2: Dưới Trái
                    (534, 235, 706, 529),  # Ô 3: Trên Phải
                    (534, 584, 706, 873)   # Ô 4: Dưới Phải
                ]

                # 4. Fit và dán từng ảnh vào từng ô
                for i, img in enumerate(webcam_images):
                    box = box_coords[i]
                    bw = box[2] - box[0]
                    bh = box[3] - box[1]

                    # Cắt và điều chỉnh ảnh vừa khít ô
                    img_fitted = ImageOps.fit(img, (bw, bh), method=Image.Resampling.LANCZOS)
                    
                    # Dán ảnh lên khung
                    base_image.paste(img_fitted, (box[0], box[1]))

                # 5. Hiển thị kết quả thành công
                st.success("✨ Ghép ảnh vào khung thành công xuất sắc!")
                st.image(base_image, caption="Khung Photobooth của bạn", use_container_width=True)
                
                # Nút tải ảnh
                buf = io.BytesIO()
                base_image.convert("RGB").save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download_button(
                    label="📥 Tải ảnh Photobooth về máy",
                    data=byte_im,
                    file_name="khanhhoa_graffiti_photobooth.png",
                    mime="image/png",
                    type="primary"
                )

        except Exception as e:
            st.error(f"Đã xảy ra lỗi trong quá trình xử lý ảnh: {e}")
