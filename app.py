import io
import streamlit as st
from PIL import Image, ImageOps, ImageDraw

st.set_page_config(
    page_title="Khanh Hoa Photobooth", 
    page_icon="🔥", 
    layout="centered"
)

st.title("Khanh Hoa Photobooth - Tự Tạo Khung")
st.write("Hãy dùng webcam chụp lần lượt 4 bức ảnh để tự động ghép vào khung!")

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
    if st.button("Tu Tao Khung Va Ghep Anh", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGBA"))

            # 1. Tự tạo khung nền (background) màu cam chủ đạo kích thước 1000x1300 pixel
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height), (235, 110, 30, 255))
            draw = ImageDraw.Draw(base_image)

            # Vẽ các đường viền trang trí khung phong cách graffiti/comic
            draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 220, 100, 255), width=8)
            draw.rectangle([(50, 50), (bg_width - 50, bg_height - 50)], outline=(255, 255, 255, 255), width=4)

            # 2. Tọa độ 4 ô chứa ảnh trên nền canvas mới
            box_coords = [
                (100, 150, 470, 680),   # Ô 1: Trên - Trái
                (530, 150, 900, 680),   # Ô 2: Trên - Phải
                (100, 710, 470, 1240),  # Ô 3: Dưới - Trái
                (530, 710, 900, 1240)   # Ô 4: Dưới - Phải
            ]

            # 3. Fit và dán từng ảnh webcam vào 4 ô kèm vẽ viền trắng nổi bật cho từng ô ảnh
            for i, img in enumerate(webcam_images):
                box = box_coords[i]
                bw = box[2] - box[0]
                bh = box[3] - box[1]

                # Cắt và tinh chỉnh ảnh vừa khít ô
                img_fitted = ImageOps.fit(img, (bw - 20, bh - 20), method=Image.Resampling.LANCZOS)
                
                # Vẽ khung nền trắng cho mỗi ô ảnh
                draw.rectangle([box[0], box[1], box[2], box[3]], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=5)
                
                # Dán ảnh lên nền
                base_image.paste(img_fitted, (box[0] + 10, box[1] + 10))

            st.success("Tự tạo khung và ghép ảnh thành công!")
            st.image(base_image, caption="Photobooth của bạn", use_container_width=True)
            
            # Nút tải ảnh kết quả về máy
            buf = io.BytesIO()
            base_image.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="Tai anh ve may",
                data=byte_im,
                file_name="khanhhoa_autofit_photobooth.png",
                mime="image/png",
                type="primary"
            )

        except Exception as e:
            st.error(f"Loi: {e}")
