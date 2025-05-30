import streamlit as st
from PIL import Image
import io
import os

st.title("🖼️ Image Compressor")

uploaded_file = st.file_uploader("Upload an image (JPEG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)

    st.write("### Compression Settings")
    quality = st.slider("Quality (for JPEG)", 10, 95, 70)

    # Detect format from filename or fallback
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext in ['.jpg', '.jpeg']:
        output_format = "JPEG"
    elif file_ext == '.png':
        output_format = "PNG"
    else:
        st.error("Only JPEG and PNG formats are supported.")
        st.stop()

    output_buffer = io.BytesIO()

    try:
        if output_format == "JPEG":
            if image.mode in ("RGBA", "P"):  # Convert to RGB if needed
                image = image.convert("RGB")
            image.save(output_buffer, format="JPEG", quality=quality, optimize=True)

        elif output_format == "PNG":
            # Ensure no incompatible mode
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA")
            image.save(output_buffer, format="PNG", optimize=True)

        st.success("Image compressed!")

        compressed_size_kb = len(output_buffer.getvalue()) / 1024
        st.write(f"📦 Compressed Size: {compressed_size_kb:.2f} KB")

        st.download_button(
            label="📥 Download Compressed Image",
            data=output_buffer.getvalue(),
            file_name=f"compressed_image.{output_format.lower()}",
            mime=f"image/{output_format.lower()}"
        )
    except Exception as e:
        st.error(f"An error occurred during compression: {e}")
