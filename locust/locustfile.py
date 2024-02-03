from locust import HttpUser, task, between
import json
import requests
import numpy as np
from PIL import Image

class TritonInferenceTest(HttpUser):
    wait_time = between(0.5, 3) # Wait time before each request in seconds
    
    @task
    def inference(self):
        img = Image.open("../imgs/test.jpg")
        raw_image = np.array(img)
        print(raw_image.shape)
        # Make a request to Triton Inference Server
        triton_server_url = "/v2/models/img_to_text/infer" # http://localhost:8000
        headers = {"Content-Type": "application/json"}
        data = {"inputs": [{"name": "image_input", "shape": raw_image.shape, "datatype": "UINT8", "data": raw_image.tolist()}]}
        
        response = self.client.post(triton_server_url, data=json.dumps(data), headers=headers)
        print(response)
        
        if response.status_code != 200:
            raise Exception("Request failed")