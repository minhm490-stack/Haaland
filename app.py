import os
import io
import streamlit as st
from PIL import Image, ImageOps, ImageDraw

st.set_page_config(
    page_title="Khanh Hoa Photobooth Pro", 
    page_icon="🔥", 
    layout="centered"
)

st.title("🔥 Khánh Hoà Photobooth - Sticker Haaland & Bạch Tuộc 🔥")
st.write("Hãy dùng webcam chụp lần lượt 4 bức ảnh để tạo khung và tự động ghép sticker trang trí nhé!")

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

# Kiểm tra nếu đã chụp đủ 4 ảnh từ webcam
if all(captured_list):
    st.success("🎉 Đã chụp đủ 4 bức ảnh! Dưới đây là các ảnh bạn vừa chụp:")
    
    # Hiển thị xem trước 4 ảnh vừa chụp
    preview_cols = st.columns(4)
    for i, cam_file in enumerate(captured_list):
        with preview_cols[i]:
            img_preview = Image.open(cam_file)
            st.image(img_preview, caption=f"Ảnh {i+1}", use_container_width=True)

    if st.button("🚀 Tạo Khung & Chèn Sticker Ngay", type="primary"):
        try:
            # 1. Đọc 4 ảnh từ webcam
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGBA"))

            # 2. Tạo khung nền (background) màu cam phong cách graffiti kích thước 1000x1300 pixel
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height), (235, 110, 30, 255))
            draw = ImageDraw.Draw(base_image)

            # Vẽ viền trang trí khung
            draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 220, 100, 255), width=8)
            draw.rectangle([(50, 50), (bg_width - 50, bg_height - 50)], outline=(255, 255, 255, 255), width=4)

            # 3. Tọa độ 4 ô chứa ảnh trên khung tự tạo
            box_coords = [
                (100, 150, 470, 680),   # Ô 1: Trên - Trái
                (530, 150, 900, 680),   # Ô 2: Trên - Phải
                (100, 710, 470, 1240),  # Ô 3: Dưới - Trái
                (530, 710, 900, 1240)   # Ô 4: Dưới - Phải
            ]

            # 4. Lần lượt fit và dán 4 ảnh webcam vào các ô
            for i, img in enumerate(webcam_images):
                box = box_coords[i]
                bw = box[2] - box[0]
                bh = box[3] - box[1]

                img_fitted = ImageOps.fit(img, (bw - 20, bh - 20), method=Image.Resampling.LANCZOS)
                
                # Vẽ khung nền trắng cho mỗi ô ảnh
                draw.rectangle([box[0], box[1], box[2], box[3]], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=5)
                
                # Dán ảnh lên nền
                base_image.paste(img_fitted, (box[0] + 10, box[1] + 10))

            current_dir = os.path.dirname(os.path.abspath(__file__))

            # 5. Chèn con bạch tuộc vào chính giữa giao điểm của 4 ô ảnh
            octopus_path = os.path.join(current_dir, "bach_tuoc.png")
            if os.path.exists(octopus_path):
                octopus_img = Image.open(octopus_path).convert("RGBA")
                octo_w = 200
                octo_h = int(octo_w * octopus_img.height / octopus_img.width)
                octopus_img = octopus_img.resize((octo_w, octo_h), Image.Resampling.LANCZOS)
                
                octo_x = (bg_width - octo_w) // 2
                octo_y = (150 + 680 + 710 - octo_h) // 2
                base_image.paste(octopus_img, (octo_x, octo_y), octopus_img)

            # 6. Chèn Sticker 1 (Ví dụ: Haaland chibi góc trên bên trái)
            sticker1_path = os.path.join(current_dir, "sticker1.png")
            if os.path.exists(sticker1_path):
                stk1 = Image.open(sticker1_path).convert("RGBA")
                stk1_w = 160
                stk1_h = int(stk1_w * stk1_h / stk1_w if False else stk1_w * stk1.height / stk1.width)
                stk1 = stk1.resize((stk1_w, stk1_h), Image.Resampling.LANCZOS)
                base_image.paste(stk1, (20, 60), stk1)

            # 7. Chèn Sticker 2 (Ví dụ: Haaland chibi góc dưới bên phải)
            sticker2_path = os.path.join(current_dir, "sticker2.png")
            if os.path.exists(sticker2_path):
                stk2 = Image.open(sticker2_path).convert("RGBA")
                stk2_w = 160
                stk2_h = int(stk2_w * stk2.height / stk2.width)
                stk2 = stk2.resize((stk2_w, stk2_h), Image.Resampling.LANCZOS)
                base_image.paste(stk2, (bg_width - stk2_w - 20, bg_height - stk2_h - 60), stk2)

            st.success("✨ Tạo ảnh Photobooth với sticker cực đẹp hoàn tất!")
            st.image(base_image, caption="Thành phẩm Photobooth của bạn", use_container_width=True)
            
            # Nút tải ảnh kết quả về máy
            buf = io.BytesIO()
            base_image.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải ảnh Photobooth về máy",
                data=byte_im,
                file_name="khanhhoa_sticker_photobooth.png",
                mime="image/png",
                type="primary"
            )

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
            
