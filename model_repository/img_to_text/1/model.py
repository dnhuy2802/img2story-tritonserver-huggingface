import json
import numpy as np
import triton_python_backend_utils as pb_utils
from transformers import pipeline
from PIL import Image

class TritonPythonModel:
    def initialize(self, args):
        self.model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    
    def execute(self, requests: list):
        responses = []
        for request in requests:
            # recieve numpy array image from request
            raw_image = pb_utils.get_input_tensor_by_name(request, "image_input").as_numpy()
            # convert to PIL image
            raw_image = Image.fromarray(raw_image)

            # run inference
            generated_txt = self.model(raw_image)[0]["generated_text"]
            print(generated_txt)
            # Encode the text to byte tensor to send back
            inference_response = pb_utils.InferenceResponse(
                output_tensors=[
                    pb_utils.Tensor(
                        "generated_text",
                        np.array([generated_txt.encode()]),
                    )
                ])
            responses.append(inference_response)
        return responses
