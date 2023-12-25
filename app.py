
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import time
import io

key = st.secrets.HF_KEY

# Define a function to generate image captions
def generate_caption(image):

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    import requests

    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer {}".format(key)}

    def query(image):
        response = requests.post(API_URL, headers=headers, data=image)
        return response.json()

    output = query(img_byte_arr)
    return str(output[0]['generated_text'])

# Streamlit app
st.title("Image Captioning!")

# Allow the user to upload an image or input a URL
image_option = st.radio("Choose an image source:", ("Upload Image", "URL"))
image = None

if image_option == "Upload Image":
    uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
else:
    url = st.text_input("Enter the image URL:")
    if st.button("Load Image"):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
            else:
                st.error("Failed to fetch image from the URL. Please check the URL.")
        except Exception as e:
            st.error("An error occurred while fetching the image.")

# Display the image and caption
if image is not None:
    st.image(image, caption="Uploaded Image", use_column_width=True, width = 200)
    st.write("Generating caption...")
    progress_bar = st.progress(0)
    time.sleep(0.5)
    with st.empty():
        for i in range(86):
            progress_bar.progress(i)
            # st.text(f"Progress: {i}%")
            time.sleep(0.01)

    # Preprocess the image and generate the caption
    # image = transforms.ToTensor()(image).unsqueeze(0)
    caption = generate_caption(image)

    progress_bar.progress(100)

    # Display the generated caption
    st.write("Generated Caption:")
    st.success(caption)

