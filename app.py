import os
import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(
    page_title="Khánh Hoà Photobooth", 
    page_icon="🌸", 
    layout="centered"
)

st.title("🌸 Khánh Hoà Photobooth - Tone Hồng Pastel 🌸")
st.write("Hãy dùng webcam chụp lần lượt **4 bức ảnh** để tạo khung hình kỷ niệm siêu xinh nhé!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Khung chụp 1")
    cam1 = st.camera_input("Ảnh 1")
    cam2 = st.camera_input("Ảnh 2")

with col2:
    st.subheader("📸 Khung chụp 2")
    cam3 = st.camera_input("Ảnh 3")
    cam4 = st.camera_input("Ảnh 4")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list):
    if st.button("✨ Tạo Khung Ảnh Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGB"))

            # --- CẤU HÌNH KHUNG VUÔNG & TÔNG MÀU HỒNG PASTEL ---
            canvas_w = 600
            canvas_h = 750  
            
            bg_color = (255, 245, 247, 255)       
            border_color = (248, 187, 208, 255)   
            frame_bg = (255, 255, 255, 255)       
            text_color = (216, 112, 147, 255)     

            canvas = Image.new("RGBA", (canvas_w, canvas_h), bg_color)
            draw = ImageDraw.Draw(canvas)

            draw.rectangle([(15, 15), (canvas_w - 15, canvas_h - 15)], outline=border_color, width=4)

            try:
                font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
                font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
            except IOError:
                font_title = ImageFont.load_default()
                font_sub = ImageFont.load_default()

            # --- TIÊU ĐỀ ---
            draw.text((canvas_w // 2, 45), "💖 KHÁNH HOÀ PHOTOCARD 💖", fill=text_color, font=font_title, anchor="mm")
            draw.text((canvas_w // 2, 75), "🌸 Memories of You & Me 🌸", fill=(220, 150, 170, 255), font=font_sub, anchor="mm")

            # --- SẮP XẾP 4 ẢNH THÀNH LƯỚI 2x2 (VUÔNG) ---
            grid_w, grid_h = 250, 220
            start_x = 45
            start_y = 110
            gap_x = 10
            gap_y = 10

            positions = [
                (start_x, start_y),
                (start_x + grid_w + gap_x, start_y),
                (start_x, start_y + grid_h + gap_y),
                (start_x + grid_w + gap_x, start_y + grid_h + gap_y)
            ]

            for idx, img in enumerate(webcam_images):
                gx, gy = positions[idx]
                
                draw.rectangle([(gx, gy), (gx + grid_w, gy + grid_h)], fill=frame_bg, outline=border_color, width=3)
                
                img_resized = ImageOps.fit(img, (grid_w - 16, grid_h - 16), method=Image.Resampling.LANCZOS)
                canvas.paste(img_resized, (gx + 8, gy + 8))

            # --- PHẦN FOOTER ---
            footer_y = canvas_h - 60
            draw.text((canvas_w // 2, footer_y), "✨ Made with love for Khánh Hoà ✨", fill=text_color, font=font_sub, anchor="mm")

            st.success("✨ Đã tạo khung ảnh thành công với tông hồng pastel tuyệt đẹp!")
            st.image(canvas, caption="Khung ảnh của bạn", use_container_width=True)
            
            buf = io.BytesIO()
            canvas.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải ảnh về máy",
                data=byte_im,
                file_name="khanhhoa_photocard.png",
                mime="image/png",
                type="primary"
            )
        except Exception as e:
            st.error(f"Đã xảy ra lỗi trong quá trình xử lý ảnh: {e}")
