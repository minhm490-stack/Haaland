import os
import io
import streamlit as st
from PIL import Image, ImageOps, ImageDraw

st.set_page_config(
    page_title="Khanh Hoa Photobooth", 
    page_icon="🔥", 
    layout="centered"
)

st.title("🔥 Khánh Hoà Photobooth - Tự Động Ghép Ảnh Cực Ngầu 🔥")
st.write("Ứng dụng tự động tạo khung nền graffiti và ghép các bức ảnh trang trí sinh động!")

if st.button("✨ Tạo Ảnh Photobooth Ngay", type="primary"):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 1. Tạo khung nền (background) màu cam phong cách graffiti kích thước 1000x1300 pixel
        bg_width, bg_height = 1000, 1300
        base_image = Image.new("RGBA", (bg_width, bg_height), (235, 110, 30, 255))
        draw = ImageDraw.Draw(base_image)

        # Vẽ đường viền trang trí khung phong cách comic
        draw.rectangle([(30, 30), (bg_width - 30, bg_height - 30)], outline=(255, 220, 100, 255), width=8)
        draw.rectangle([(50, 50), (bg_width - 50, bg_height - 50)], outline=(255, 255, 255, 255), width=4)

        # 2. Danh sách 4 file ảnh bạn đã tải lên GitHub
        image_filenames = ["anh1.jpg", "anh2.jpg", "anh3.jpg", "anh4.jpg"]
        
        # Tọa độ 4 ô chứa ảnh trên khung
        box_coords = [
            (100, 150, 470, 680),   # Ô 1: Trên - Trái
            (530, 150, 900, 680),   # Ô 2: Trên - Phải
            (100, 710, 470, 1240),  # Ô 3: Dưới - Trái
            (530, 710, 900, 1240)   # Ô 4: Dưới - Phải
        ]

        # 3. Lần lượt đọc từng ảnh, fit vừa khung, vẽ viền trắng và dán lên
        for i, filename in enumerate(image_filenames):
            img_path = os.path.join(current_dir, filename)
            if os.path.exists(img_path):
                img = Image.open(img_path).convert("RGBA")
                box = box_coords[i]
                bw = box[2] - box[0]
                bh = box[3] - box[1]

                img_fitted = ImageOps.fit(img, (bw - 20, bh - 20), method=Image.Resampling.LANCZOS)
                
                # Vẽ khung nền trắng bo viền đen cho mỗi ô ảnh
                draw.rectangle([box[0], box[1], box[2], box[3]], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=5)
                
                # Dán ảnh lên nền
                base_image.paste(img_fitted, (box[0] + 10, box[1] + 10))
            else:
                st.warning(f"Không tìm thấy file: {filename}")

        # 4. Chèn con bạch tuộc vào chính giữa giao điểm 4 khung
        octopus_path = os.path.join(current_dir, "bach_tuoc.png")
        if os.path.exists(octopus_path):
            octopus_img = Image.open(octopus_path).convert("RGBA")
            octo_w = 220
            octo_h = int(octo_w * octopus_img.height / octopus_img.width)
            octopus_img = octopus_img.resize((octo_w, octo_h), Image.Resampling.LANCZOS)
            
            octo_x = (bg_width - octo_w) // 2
            octo_y = (150 + 680 + 710 - octo_h) // 2
            
            base_image.paste(octopus_img, (octo_x, octo_y), octopus_img)

        st.success("✨ Tạo ảnh Photobooth thành công xuất sắc!")
        st.image(base_image, caption="Thành phẩm của bạn", use_container_width=True)
        
        # Nút tải ảnh kết quả về máy
        buf = io.BytesIO()
        base_image.convert("RGB").save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Tải ảnh Photobooth về máy",
            data=byte_im,
            file_name="khanhhoa_photobooth_pro.png",
            mime="image/png",
            type="primary"
        )

    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")
