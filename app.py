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
