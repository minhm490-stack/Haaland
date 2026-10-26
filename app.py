import os
import io
import streamlit as st
from PIL import Image, ImageOps, ImageDraw

st.set_page_config(
    page_title="Khanh Hoa Photobooth", 
    page_icon="🔥", 
    layout="centered"
)

st.title("Khanh Hoa Photobooth - Sinh Động Cùng Bạch Tuộc")
st.write("Hãy dùng webcam chụp lần lượt 4 bức ảnh để tự động tạo khung và ghép ảnh nhé!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Khung chụp 1")
    cam1 = st.camera_input("Anh 1 (Tren trai)")
    cam2 = st.camera_input("Anh 2 (Duoi trai)")

with col2:
    st.subheader("Khung chụp 2")
    cam3 = st.camera_input("Anh 3 (Tren phai)")
    cam4 = st.camera_input("Anh 4 (Duoi phai)")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list):
    if st.button("Tạo Khung Và Ghép Ảnh Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGBA"))

            # 1. Tạo khung nền (background) màu cam phong cách graffiti kích thước 1000x1300 pixel
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height), (235, 110, 30, 255))
            draw = ImageDraw.Draw(base_image)

            # Vẽ viền trang trí khung
            draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 220, 100, 255), width=8)
            draw.rectangle([(50, 50), (bg_width - 50, bg_height - 50)], outline=(255, 255, 255, 255), width=4)

            # 2. Tọa độ 4 ô chứa ảnh
            box_coords = [
                (100, 150, 470, 680),   # Ô 1: Trên - Trái
                (530, 150, 900, 680),   # Ô 2: Trên - Phải
                (100, 710, 470, 1240),  # Ô 3: Dưới - Trái
                (530, 710, 900, 1240)   # Ô 4: Dưới - Phải
            ]

            # 3. Fit và dán từng ảnh webcam vào 4 ô kèm vẽ viền trắng nổi bật
            for i, img in enumerate(webcam_images):
                box = box_coords[i]
                bw = box[2] - box[0]
                bh = box[3] - box[1]

                img_fitted = ImageOps.fit(img, (bw - 20, bh - 20), method=Image.Resampling.LANCZOS)
                
                # Vẽ khung nền trắng cho mỗi ô ảnh
                draw.rectangle([box[0], box[1], box[2], box[3]], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=5)
                
                # Dán ảnh lên nền
                base_image.paste(img_fitted, (box[0] + 10, box[1] + 10))

            # 4. Chèn con bạch tuộc vào chính giữa giao điểm của 4 ô ảnh để tạo điểm nhấn sinh động
            current_dir = os.path.dirname(os.path.abspath(__file__))
            octopus_path = os.path.join(current_dir, "bach_tuoc.png")
            
            if os.path.exists(octopus_path):
                octopus_img = Image.open(octopus_path).convert("RGBA")
                # Thay đổi kích thước bạch tuộc cho cân đối (ví dụ: rộng 220px)
                octo_w = 220
                octo_h = int(octo_w * octopus_img.height / octopus_img.width)
                octopus_img = octopus_img.resize((octo_w, octo_h), Image.Resampling.LANCZOS)
                
                # Tính tọa độ chính giữa giao điểm 4 khung
                octo_x = (bg_width - octo_w) // 2
                octo_y = (150 + 680 + 710 - octo_h) // 2  # Vùng giao nhau giữa các khung trên và dưới
                
                # Dán bạch tuộc đè lên trung tâm bằng kênh Alpha (trong suốt)
                base_image.paste(octopus_img, (octo_x, octo_y), octopus_img)

            st.success("Ghép ảnh và trang trí thành công!")
            st.image(base_image, caption="Photobooth siêu sinh động của bạn", use_container_width=True)
            
            # Nút tải ảnh kết quả về máy
            buf = io.BytesIO()
            base_image.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="Tải ảnh về máy",
                data=byte_im,
                file_name="khanhhoa_octopus_photobooth.png",
                mime="image/png",
                type="primary"
            )

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
