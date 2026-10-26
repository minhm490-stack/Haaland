import os
import io
import streamlit as st
from PIL import Image, ImageOps, ImageDraw

st.set_page_config(
    page_title="Khanh Hoa Photobooth Pro", 
    page_icon="🔥", 
    layout="centered"
)

st.title("🔥 Khánh Hoà Photobooth - Pro Edition 🔥")
st.write("Chụp 4 ảnh từ webcam để tạo siêu phẩm Photobooth cực chất!")

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

def remove_white_background(img, threshold=240):
    """Hàm tự động biến nền trắng hoặc xám nhạt của sticker thành trong suốt"""
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        # Nếu điểm ảnh gần màu trắng, chuyển nó thành trong suốt hoàn toàn
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

    if st.button("🚀 Tạo Siêu Phẩm Photobooth Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGBA"))

            # 1. Tạo hiệu ứng nền Gradient cam-vàng cực kỳ xịn xò và bắt mắt
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height))
            draw = ImageDraw.Draw(base_image)
            
            for y in range(bg_height):
                # Tạo dải màu chuyển từ cam đậm sang cam sáng ấm áp
                r = int(240 - (y / bg_height) * 40)
                g = int(90 + (y / bg_height) * 30)
                b = int(20 + (y / bg_height) * 40)
                draw.line([(0, y), (bg_width, y)], fill=(r, g, b, 255))

            # Vẽ viền phong cách graffiti nghệ thuật
            draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 240, 150, 255), width=10)
            draw.rectangle([(45, 45), (bg_width - 45, bg_height - 45)], outline=(255, 255, 255, 255), width=4)

            # 2. Tọa độ 4 ô chứa ảnh
            box_coords = [
                (100, 150, 470, 680),   # Ô 1: Trên - Trái
                (530, 150, 900, 680),   # Ô 2: Trên - Phải
                (100, 710, 470, 1240),  # Ô 3: Dưới - Trái
                (530, 710, 900, 1240)   # Ô 4: Dưới - Phải
            ]

            # 3. Fit ảnh webcam vào 4 ô với viền bo tròn/trắng nổi bật
            for i, img in enumerate(webcam_images):
                box = box_coords[i]
                bw = box[2] - box[0]
                bh = box[3] - box[1]

                img_fitted = ImageOps.fit(img, (bw - 24, bh - 24), method=Image.Resampling.LANCZOS)
                
                # Khung nền trắng cho từng ảnh chụp
                draw.rectangle([box[0], box[1], box[2], box[3]], fill=(255, 255, 255, 255), outline=(30, 30, 30, 255), width=6)
                base_image.paste(img_fitted, (box[0] + 12, box[1] + 12))

            current_dir = os.path.dirname(os.path.abspath(__file__))

            # 4. Tự động xóa nền trắng và chèn Bạch Tuộc vào giữa
            octopus_path = os.path.join(current_dir, "bach_tuoc.png")
            if os.path.exists(octopus_path):
                octo_img = Image.open(octopus_path).convert("RGBA")
                octo_img = remove_white_background(octo_img)
                octo_w = 210
                octo_h = int(octo_w * octo_img.height / octo_img.width)
                octo_img = octo_img.resize((octo_w, octo_h), Image.Resampling.LANCZOS)
                
                octo_x = (bg_width - octo_w) // 2
                octo_y = (150 + 680 + 710 - octo_h) // 2
                base_image.paste(octo_img, (octo_x, octo_y), octo_img)

            # 5. Tự động xóa nền trắng và chèn Sticker 1 (Góc trên trái)
            sticker1_path = os.path.join(current_dir, "sticker1.png")
            if os.path.exists(sticker1_path):
                stk1 = Image.open(sticker1_path).convert("RGBA")
                stk1 = remove_white_background(stk1)
                stk1_w = 170
                stk1_h = int(stk1_w * stk1.height / stk1.width)
                stk1 = stk1.resize((stk1_w, stk1_h), Image.Resampling.LANCZOS)
                base_image.paste(stk1, (55, 65), stk1)

            # 6. Tự động xóa nền trắng và chèn Sticker 2 (Góc dưới phải)
            sticker2_path = os.path.join(current_dir, "sticker2.png")
            if os.path.exists(sticker2_path):
                stk2 = Image.open(sticker2_path).convert("RGBA")
                stk2 = remove_white_background(stk2)
                stk2_w = 170
                stk2_h = int(stk2_w * stk2.height / stk2.width)
                stk2 = stk2.resize((stk2_w, stk2_h), Image.Resampling.LANCZOS)
                base_image.paste(stk2, (bg_width - stk2_w - 55, bg_height - stk2_h - 65), stk2)

            st.success("🌟 Tạo ảnh thành công cực kỳ sắc nét!")
            st.image(base_image, caption="Thành phẩm Photobooth Xịn Xò", use_container_width=True)
            
            buf = io.BytesIO()
            base_image.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải ảnh Photobooth về máy",
                data=byte_im,
                file_name="khanhhoa_pro_photobooth.png",
                mime="image/png",
                type="primary"
            )

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
