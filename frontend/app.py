import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(
    page_title="Image Caption Generator",
    page_icon="🖼️",
    layout="centered"
)

st.title("🖼️ Image Caption Generator")
st.markdown("Powered by **LLaVA via Ollama** · FastAPI backend · Streamlit frontend")
st.divider()

uploaded_file = st.file_uploader(
    "Upload an image to caption:",
    type=["png", "jpg", "jpeg", "webp"],
    help="Supported formats: PNG, JPG, JPEG, WEBP"
)

if uploaded_file is not None:
    # Display image preview
    image = Image.open(uploaded_file)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    # Show image metadata
    with st.expander("📋 Image Details"):
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Format:** {image.format or uploaded_file.type}")
        st.write(f"**Size:** {image.width} × {image.height} px")
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        st.write(f"**File size:** {file_size_kb:.1f} KB")

    st.divider()

    if st.button("✨ Generate Caption", type="primary", use_container_width=True):
        with st.spinner("Analyzing image with LLaVA..."):
            try:
                # Reset file pointer before sending
                uploaded_file.seek(0)
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    "http://localhost:8000/caption/",
                    files=files,
                    timeout=150
                )

                if response.status_code == 200:
                    result = response.json()
                    caption = result.get("caption", "No caption generated.")

                    st.subheader("📝 Generated Caption")
                    st.success(caption)

                    # Copy-friendly text box
                    st.text_area("Copy caption:", value=caption, height=80)

                elif response.status_code == 400:
                    detail = response.json().get("detail", "Bad request.")
                    st.error(f"❌ {detail}")
                elif response.status_code == 503:
                    st.error("❌ Could not connect to Ollama. Make sure it is running (`ollama serve`).")
                else:
                    st.error(f"❌ Server error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not reach the backend. Make sure FastAPI is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. LLaVA may need more time — try again.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

else:
    st.info("👆 Upload an image above to get started.")

st.divider()
st.caption(
    "Ensure Ollama is running (`ollama serve`) and the backend is active "
    "(`uvicorn backend.main:app --reload`) before uploading an image."
)
