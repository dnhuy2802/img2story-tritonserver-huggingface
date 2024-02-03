import google.generativeai as genai
import requests
import os
import streamlit as st
import json
from transformers import pipeline
from PIL import Image
from tritonclient.utils import *

# load env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
HF_API = os.getenv("HF_API")

def img2text_triton(img):
    raw_image = np.array(img)
    print(raw_image.shape)
    # Make a request to Triton Inference Server
    triton_server_url = "http://localhost:8000/v2/models/img_to_text/infer"
    headers = {"Content-Type": "application/json"}
    data = {"inputs": [{"name": "image_input", "shape": raw_image.shape, "datatype": "UINT8", "data": raw_image.tolist()}]}
    
    response = requests.post(triton_server_url, data=json.dumps(data), headers=headers)
    
    # Parse the response and return the prediction
    result = json.loads(response.content.decode("utf-8"))
    text_response = result["outputs"][0]["data"][0]
    print(result)
    return text_response

# img to text
def img2text(img):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    text = image_to_text(img)[0]["generated_text"]
    print(text)
    return text

# llm
def generate_story(scenario):
    template = f"""You are a story teller. You can generate a short story based on a simplenarrative, thestorwshoutdbe nomore than 20 wrords. CONTEXT: {scenario}"""
    # print(template)
    # Genai Config
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(template)

    return response.text

# text to speech
def text_to_speech(msg):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HF_API}"}

    payload = {"inputs": msg}

    response = requests.post(API_URL, headers=headers, json=payload)

    open("output/output.wav", "wb").write(response.content)

def main():
    st.set_page_config(page_title="Story Generator", page_icon="📖", layout="wide")
    st.header("Story Generator")

    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"], key="image")
    image = ""

    if uploaded_file is not None:
        print (uploaded_file)
        image = Image.open(uploaded_file)
        # bytes_data = uploaded_file.getvalue()

        st.image(image, caption="Uploaded Image", use_column_width=True)
        # scenario = img2text(image)
        scenario = img2text_triton(image)
        story = generate_story(scenario)
        text_to_speech(story)

        with st.expander("Scenario"):
            st.write(scenario)
        
        with st.expander("Story"):
            st.write(story)
        
        st.audio("output/output.wav")

if __name__ == "__main__":
    main()
