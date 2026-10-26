import os
import io
import math
import random
import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFilter

st.set_page_config(
    page_title="Khanh Hoa Photobooth Pink White", 
    page_icon="🌸", 
    layout="centered"
)

st.title("🌸 Khánh Hoà Photobooth - Tone Hồng Trắng Ngọt Ngào 🌸")
st.write("Chụp 4 ảnh từ webcam để tạo siêu phẩm Photobooth tone Hồng - Trắng cực xinh!")

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

def draw_heart(draw_obj, xy, size, fill_color):
    """Hàm vẽ sticker trái tim cute"""
    x, y = xy
    r = size // 2
    draw_obj.pieslice([x - r, y - r, x, y + r], 180, 360, fill=fill_color)
    draw_obj.pieslice([x, y - r, x + r, y + r], 180, 360, fill=fill_color)
    points = [(x - size, y), (x + size, y), (x, y + size * 1.2)]
    draw_obj.polygon(points, fill=fill_color)

def draw_star(draw_obj, xy, size, fill_color):
    """Hàm vẽ ngôi sao lấp lánh"""
    x, y = xy
    points = []
    for i in range(10):
        angle = i * math.pi / 5
        r_val = size if i % 2 == 0 else size // 2
        points.append((x + r_val * math.sin(angle), y - r_val * math.cos(angle)))
    draw_obj.polygon(points, fill=fill_color)

if all(captured_list):
    st.success("🎉 Đã chụp đủ 4 bức ảnh!")
    
    preview_cols = st.columns(4)
    for i, cam_file in enumerate(captured_list):
        with preview_cols[i]:
            img_preview = Image.open(cam_file)
            st.image(img_preview, caption=f"Ảnh {i+1}", use_container_width=True)

    if st.button("🚀 Tạo Siêu Phẩm Hồng - Trắng Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                img_cam = Image.open(f).convert("RGBA")
                img_cam_clean = remove_white_background(img_cam, threshold=240)
                webcam_images.append(img_cam_clean)

            # 1. Tạo khung nền Gradient Hồng - Trắng ngọt ngào
            bg_width, bg_height = 1000, 1300
            base_image = Image.new("RGBA", (bg_width, bg_height))
            draw = ImageDraw.Draw(base_image)
            
            for y in range(bg_height):
                r = int(255 - (y / bg_height) * 30)
                g = int(192 + (y / bg_height) * 30)
                b = int(203 + (y / bg_height) * 30)
                draw.line([(0, y), (bg_width, y)], fill=(r, g, b, 255))

            # 2. Thêm sticker trái tim và ngôi sao lấp lánh khắp nền
            random.seed(101)
            for _ in range(22):
                rx = random.randint(30, bg_width - 30)
                ry = random.randint(30, bg_height - 30)
                draw_heart(draw, (rx, ry), size=random.randint(10, 18), fill_color=(255, 255, 255, 200))

            star_positions = [(70, 70), (930, 70), (70, 1230), (930, 1230), (500, 45), (500, 1255), (200, 45), (800, 45)]
            for sp in star_positions:
                draw_star(draw, sp, size=14, fill_color=(255, 255, 255, 240))

            # 3. Tạo hiệu ứng phát sáng Neon cho khung viền
            neon_layer = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
            neon_draw = ImageDraw.Draw(neon_layer)
            neon_draw.rectangle([(25, 25), (bg_width - 25, bg_height - 25)], outline=(255, 255, 255, 180), width=14)
            neon_layer = neon_layer.filter(ImageFilter.GaussianBlur(10))
            base_image = Image.alpha_composite(base_image, neon_layer)
            draw = ImageDraw.Draw(base_image)

            # Viền khung kép sắc nét
            draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 255, 255, 255), width=8)
            draw.rectangle([(42, 42), (bg_width - 42, bg_height - 42)], outline=(255, 105, 180, 255), width=4)

            current_dir = os.path.dirname(os.path.abspath(__file__))

            # --- CHÈN BANNER ẢNH CHỮ VÀO GIỮA KHUNG PHÍA TRÊN ---
            banner_path = os.path.join(current_dir, "banner.png")
            if os.path.exists(banner_path):
                banner_img = Image.open(banner_path).convert("RGBA")
                # Điều chỉnh chiều rộng banner vừa khít với khung (ví dụ rộng 880 pixel)
                banner_w = 880
                banner_h = int(banner_w * banner_img.height // banner_img.width)
                banner_img = banner_img.resize((banner_w, banner_h), Image.Resampling.LANCZOS)
                
                # Căn giữa tuyệt đối theo chiều ngang, đặt ở vị trí phía trên
                banner_x = (bg_width - banner_w) // 2
                banner_y = 50
                
                # Dán banner lên nền
                base_image.paste(banner_img, (banner_x, banner_y), banner_img)
            else:
                # Fallback nếu chưa tải ảnh banner lên
                draw.rectangle([(60, 40, 940, 150)], fill=(255, 255, 255, 250), outline=(255, 105, 180, 255), width=5)
            # ----------------------------------------------------

            # Banner dưới trang trí
            draw.rectangle([(250, 1180), (750, 1230)], fill=(255, 255, 255, 230), outline=(255, 105, 180, 255), width=3)

            # 4. Tọa độ 4 ô chứa ảnh webcam
            box_coords = [
                (100, 175, 470, 680),   # Ô 1: Trên - Trái
                (530, 175, 900, 680),   # Ô 2: Trên - Phải
                (100, 710, 470, 1240),  # Ô 3: Dưới - Trái
                (530, 710, 900, 1240)   # Ô 4: Dưới - Phải
            ]

            # 5. Fit ảnh webcam vào 4 ô với khung viền trắng hồng
            for i, img in enumerate(webcam_images):
                box = box_coords[i]
                bw = box[2] - box[0]
                bh = box[3] - box[1]

                img_fitted = ImageOps.fit(img, (bw - 24, bh - 24), method=Image.Resampling.LANCZOS)
                
                draw.rectangle([box[0], box[1], box[2], box[3]], fill=(255, 240, 245, 220), outline=(255, 105, 180, 255), width=6)
                base_image.paste(img_fitted, (box[0] + 12, box[1] + 12), img_fitted)

            # 6. Xóa nền và chèn Bạch Tuộc vào giữa
            octopus_path = os.path.join(current_dir, "bach_tuoc.png")
            if os.path.exists(octopus_path):
                octo_img = Image.open(octopus_path).convert("RGBA")
                octo_img = remove_white_background(octo_img)
                octo_w = 210
                octo_h = int(octo_w * octo_img.height // octo_img.width)
                octo_img = octo_img.resize((octo_w, octo_h), Image.Resampling.LANCZOS)
                
                octo_x = (bg_width - octo_w) // 2
                octo_y = (175 + 680 + 710 - octo_h) // 2
                base_image.paste(octo_img, (octo_x, octo_y), octo_img)

            # 7. Xóa nền và chèn Sticker 1 (Góc trên trái)
            sticker1_path = os.path.join(current_dir, "sticker1.png")
            if os.path.exists(sticker1_path):
                stk1 = Image.open(sticker1_path).convert("RGBA")
                stk1 = remove_white_background(stk1)
                stk1_w = 170
                stk1_h = int(stk1_w * stk1.height // stk1.width)
                stk1 = stk1.resize((stk1_w, stk1_h), Image.Resampling.LANCZOS)
                base_image.paste(stk1, (55, 80), stk1)

            # 8. Xóa nền và chèn Sticker 2 (Góc dưới phải)
            sticker2_path = os.path.join(current_dir, "sticker2.png")
            if os.path.exists(sticker2_path):
                stk2 = Image.open(sticker2_path).convert("RGBA")
                stk2 = remove_white_background(stk2)
                stk2_w = 170
                stk2_h = int(stk2_w * stk2.height // stk2.width)
                stk2 = stk2.resize((stk2_w, stk2_h), Image.Resampling.LANCZOS)
                base_image.paste(stk2, (bg_width - stk2_w - 55, bg_height - stk2_h - 65), stk2)

            st.success("🌟 Tạo siêu phẩm Photobooth thành công!")
            st.image(base_image, caption="Thành phẩm Photobooth Happy Birthday Khánh Hoà", use_container_width=True)
            
            buf = io.BytesIO()
            base_image.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải ảnh Photobooth về máy",
                data=byte_im,
                file_name="khanhhoa_birthday_photobooth.png",
                mime="image/png",
                type="primary"
            )

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
            
