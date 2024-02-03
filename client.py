import numpy as np
import tritonclient.http as httpclient
from PIL import Image
import google.generativeai as genai
import os
import requests

# load env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

HF_API = os.getenv("HF_API")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# text to speech
def text_to_speech(msg):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HF_API}"}

    payload = {"inputs": msg}

    response = requests.post(API_URL, headers=headers, json=payload)

    open("output/output.wav", "wb").write(response.content)

# llm
def generate_story(scenario):
    template = f"""You are a story teller. You can generate a short story based on a simplenarrative, thestorwshoutdbe nomore than 20 wrords. CONTEXT: {scenario}"""
    # print(template)
    # Genai Config
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(template)

    return response.text

def img2text(image):
    # Setting up client
    client = httpclient.InferenceServerClient(url="localhost:8000")

    # # Read image and create input object
    # raw_image = Image.open("imgs/young-people-3575167_640.jpg")
    # convert to numpy array
    raw_image = np.array(image)
    print(raw_image.shape)
    
    # Send image to server
    img_input = httpclient.InferInput("image_input", raw_image.shape, "UINT8")
    img_input.set_data_from_numpy(raw_image)

    # Get output
    results = client.infer(model_name="img_to_text", inputs=[img_input])

    # Print text from response
    text_response = results.as_numpy("generated_text")[0].decode()

    return text_response

def main():
    # Read image and create input object
    raw_image = Image.open("imgs/test.jpg")
    scenario = img2text(raw_image)
    story = generate_story(scenario)
    print(story)
    text_to_speech(story)

if __name__ == "__main__":
    main()
