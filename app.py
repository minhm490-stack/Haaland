import os
import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(
    page_title="Khánh Hoà Photobooth", 
    page_icon="💖", 
    layout="centered"
)

st.title("💖 Khánh Hoà Photobooth - Chụp Trực Tiếp")
st.write("Hãy dùng webcam chụp lần lượt **4 bức ảnh** để tạo dải Photostrip sinh nhật siêu dễ thương nhé!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Khung chụp ảnh")
    cam1 = st.camera_input("Chụp ảnh 1")
    cam2 = st.camera_input("Chụp ảnh 2")

with col2:
    st.subheader("📸 Khung chụp tiếp")
    cam3 = st.camera_input("Chụp ảnh 3")
    cam4 = st.camera_input("Chụp ảnh 4")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list):
    if st.button("✨ Tạo Dải Photostrip Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGB"))

            strip_w = 640
            card_w, card_h = 580, 150 
            margin_x = (strip_w - card_w) // 2
            margin_y = 15
            header_h = 130
            footer_h = 160

            strip_h = header_h + (card_h * 4) + (margin_y * 5) + footer_h

            bg_pink_white = (255, 240, 245, 255)
            strip = Image.new("RGBA", (strip_w, strip_h), bg_pink_white)
            draw = ImageDraw.Draw(strip)

            stripe_w = 20
            border_pink = (255, 150, 180, 255)
            card_bg_color = (255, 255, 255, 255)
            frame_outline = (255, 105, 180, 255)
            text_pink_color = (219, 62, 115, 255)

            draw.rectangle([(0, 0), (stripe_w, strip_h)], fill=border_pink)
            draw.rectangle([(strip_w - stripe_w, 0), (strip_w, strip_h)], fill=border_pink)

            try:
                font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
                font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
                font_wish = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
            except IOError:
                font_title = font_sub = font_wish = ImageFont.load_default()

            def draw_flower(draw_obj, cx, cy, petal_color, center_color, size=8):
                for dx, dy in [(-size, 0), (size, 0), (0, -size), (0, size), (-size*0.7, -size*0.7), (size*0.7, size*0.7), (-size*0.7, size*0.7), (size*0.7, -size*0.7)]:
                    draw_obj.ellipse([(cx + dx - size/2, cy + dy - size/2), (cx + dx + size/2, cy + dy + size/2)], fill=petal_color)
                draw_obj.ellipse([(cx - size/2, cy - size/2), (cx + size/2, cy + size/2)], fill=center_color)

            # --- HEADER ---
            draw.text((strip_w // 2, 45), "🎉 HAPPY BIRTHDAY 🎉", fill=text_pink_color, font=font_title, anchor="mm")
            draw.text((strip_w // 2, 85), "🌸 KHÁNH HOÀ C CUTIE 🌸", fill=(255, 105, 180), font=font_sub, anchor="mm")

            draw_flower(draw, 80, 45, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=10)
            draw_flower(draw, strip_w - 80, 45, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=10)

            # --- DÁN ẢNH ---
            current_y = header_h + margin_y
            for img in webcam_images:
                draw.rectangle([
                    (margin_x, current_y), 
                    (margin_x + card_w, current_y + card_h)
                ], fill=card_bg_color, outline=frame_outline, width=3)

                img_resized = ImageOps.fit(img, (card_w - 16, card_h - 16), method=Image.Resampling.LANCZOS)
                strip.paste(img_resized, (margin_x + 8, current_y + 8))
                current_y += card_h + margin_y

            # --- FOOTER ---
            footer_y = strip_h - footer_h + 30
            draw.text((strip_w // 2, footer_y), "Make with 💖 for Khánh Hoà", fill=text_pink_color, font=font_wish, anchor="mm")
            draw_flower(draw, strip_w // 2 - 100, footer_y, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=8)
            draw_flower(draw, strip_w // 2 + 100, footer_y, petal_color=(255, 182, 193), center_color=(255, 215, 0), size=8)

            st.success("✨ Đã tạo dải Photostrip thành công!")
            st.image(strip, caption="Dải Photostrip của bạn", use_container_width=True)
            
            buf = io.BytesIO()
            strip.convert("RGB").save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải ảnh Photostrip về máy",
                data=byte_im,
                file_name="khanhhoa_photostrip.png",
                mime="image/png",
                type="primary"
            )
        except Exception as e:
            st.error(f"Đã xảy ra lỗi trong quá trình xử lý ảnh: {e}")
