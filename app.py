import os
import io
import math
import random
import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFilter

st.set_page_config(
    page_title="Khanh Hoa Photobooth Pro Max", 
    page_icon="💖", 
    layout="centered"
)

st.title("💖 Khánh Hoà Photobooth - Siêu Phẩm Neon & Chi Tiết Sống Động 💖")
st.write("Chụp 4 ảnh từ webcam để tạo siêu phẩm Photobooth cực kỳ rực rỡ và sinh động!")

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

def draw_star(draw_obj, xy, size, fill_color):
    """Hàm vẽ ngôi sao trang trí sinh động"""
    x, y = xy
    points = []
    for i in range(10):
        angle = i * math.pi / 5
        r = size if i % 2 == 0 else size / 2
        points.append((x + r * math.sin(angle), y - r * math.cos(angle)))
    draw_obj.polygon(points, fill=fill_color)

if all(captured_list):
    st.success("🎉 Đã chụp đủ 4 bức ảnh!")
    
    preview_cols = st.columns(4)
    for i, cam_file in enumerate(captured_list):
        with preview_cols[i]:
            img_preview = Image.open(cam_file)
            st.image(img_preview, caption=f"Ảnh {i+1}", use_container_width=True)

    if st.button("🚀 Tạo Siêu Phẩm Cực Sống Động Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0.0)
                img_cam = Image.open(f).convert("RGBA")
                img_cam_clean = remove_white_background(img_cam, threshold=240)
                webcam_images.append(img_cam_clean)

            # 1. Tạo khung nền Gradient Xanh - Hồng neon sâu thẳm
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height))
            draw = ImageDraw.Draw(base_image)
            
            for y in range(bg_height):
                r = int(15 + (y / bg_height) * 210)
                g = int(90 - (y / bg_height) * 50)
                b = int(240 - (y / bg_height) * 30)
                draw.line([(0, y), (bg_width, y)], fill=(r, g, b, 255))

            # 2. Thêm vô số chi tiết bong bóng, ngôi sao và đốm sáng trang trí nền lung linh
            random.seed(42)  # Cố định vị trí các chi tiết cho đẹp mắt
            for _ in range(35):
                rx = random.randint(20, bg_width - 20)
                ry = random.randint(20, bg_height - 20)
                rad = random.randint(3, 8)
                color = random.choice([
                    (255, 105, 180, 200), 
                    (0, 255, 255, 200), 
                    (255, 255, 0, 200), 
                    (255, 255, 255, 180)
                ])
                draw.ellipse([rx - rad, ry - rad, rx + rad, ry + rad], fill=color)

            # Vẽ thêm các ngôi sao lấp lánh ở 4 góc viền
            star_positions = [(65, 65), (935, 65), (65, 1235), (935, 1235), (500, 50), (500, 1250)]
            for sp in star_positions:
                draw_star(draw, sp, size=12, fill_color=(255, 255, 0, 240))

            # 3. Tạo hiệu ứng phát sáng Neon (Glow Effect) cho khung viền
            neon_layer = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
            neon_draw = ImageDraw.Draw(neon_layer)
            neon_draw.rectangle([(25, 25), (bg_width - 25, bg_height - 25)], outline=(255, 20, 147, 160), width=14)
            neon_layer = neon_layer.filter(ImageFilter.GaussianBlur(10))
            base_image = Image.alpha_composite(base_image, neon_layer)
            draw = ImageDraw.Draw(base_image)

            # Viền khung kép sắc nét phong cách Neon Cyberpunk
            draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 255, 255, 255), width=8)
            draw.rectangle([(42, 42), (bg_width - 42, bg_height - 42)], outline=(0, 255, 255, 255), width=4)

            # Thêm banner tiêu đề cách điệu ở trên và dưới khung
            draw.rectangle([(150, 45), (850, 110)], fill=(20, 20, 40, 220), outline=(255, 105, 180, 255), width=3)
            draw.rectangle([(250, 1180), (750, 1230)], fill=(20, 20, 40, 220), outline=(0, 255, 255, 255), width=3)

            # 4. Tọa độ 4 ô chứa ảnh webcam
            box_coords = [
                (100, 150, 470, 680),   # Ô 1: Trên - Trái
                (530, 150, 900, 680),   # Ô 2: Trên - Phải
                (100, 710, 470, 1240),  # Ô 3: Dưới - Trái
                (530, 710, 900, 1240)   # Ô 4: Dưới - Phải
            ]

            # 5. Fit ảnh webcam vào 4 ô với khung viền Neon bao quanh
            for i, img in enumerate(webcam_images):
                box = box_coords[i]
                bw = box[2] - box[0]
                bh = box[3] - box[1]

                img_fitted = ImageOps.fit(img, (bw - 24, bh - 24), method=Image.Resampling.LANCZOS)
                
                # Vẽ viền neon cyan cho từng ô chứa ảnh
                draw.rectangle([box[0], box[1], box[2], box[3]], fill=(15, 15, 35, 220), outline=(0, 255, 255, 255), width=6)
                base_image.paste(img_fitted, (box[0] + 12, box[1] + 12), img_fitted)

            current_dir = os.path.dirname(os.path.abspath(__file__))

            # 6. Xóa nền và chèn Bạch Tuộc vào giữa giao điểm
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

            # 7. Xóa nền và chèn Sticker 1 (Góc trên trái)
            sticker1_path = os.path.join(current_dir, "sticker1.png")
            if os.path.exists(sticker1_path):
                stk1 = Image.open(sticker1_path).convert("RGBA")
                stk1 = remove_white_background(stk1)
                stk1_w = 170
                stk1_h = int(stk1_w * stk1.height / stk1.width)
                stk1 = stk1.resize((stk1_w, stk1_h), Image.Resampling.LANCZOS)
                base_image.paste(stk1, (55, 65), stk1)

            # 8. Xóa nền và chèn Sticker 2 (Góc dưới phải)
            sticker2_path = os.path.join(current_dir, "sticker2.png")
            if os.path.exists(sticker2_path):
                stk2 = Image.open(sticker2_path).convert("RGBA")
                stk2 = remove_white_background(stk2)
                stk2_w = 170
                stk2_h = int(stk2_w * stk2.height / stk2.width)
                stk2 = stk2.resize((stk2_w, stk2_h), Image.Resampling.LANCZOS)
                base_image.paste(stk2, (bg_width - stk2_w - 55, bg_height - stk2_h - 65), stk2)

            st.success("🌟 Tạo siêu phẩm Photobooth cực kỳ sống động thành công!")
            st.image(base_image, caption="Thành phẩm Photobooth Sống Động Xịn Xò", use_container_width=True)
            
            buf = io.BytesIO()
            base_image.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải ảnh Photobooth về máy",
                data=byte_im,
                file_name="khanhhoa_vivid_photobooth.png",
                mime="image/png",
                type="primary"
            )

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
