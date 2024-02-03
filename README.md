<a name="readme-top"></a>

<!-- ABOUT THE PROJECT -->
# Image to Story Using Triton Server

### Built With

* [![Python][Python]][Python]
* [![Triton Server][TritonServer]][TritonServer]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

1. Install requirements
   ```sh
    pip install -r requirements.txt
   ```
2. Setup Hugging Face API Key and Google API Key
   ```sh
   # Create a .env file in the root directory of the project
   # Add the following line to the .env file
   HF_API_KEY=your_hugging_face_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```
3. Prepare 2 windows Command Prompts. The  first one will be used to run the Triton Server and the second one will be used to run the Streamlit App.

4. In the first Command Prompt, run the following command to start the Triton Server:
   ```sh
   # xx.yy is the version of the Triton Server
   docker run --gpus=all -it --shm-size=256m -p8000:8000 -p8001:8001 -p8002:8002 -v ${PWD}:/workspace/ -v  "%cd%"/model_repository:/models nvcr.io/nvidia/tritonserver:xx.yy-py3 bash

   # In the Triton Server, run the following command to install some libraries:
   pip install transformers torch pillow python-dotenv
   
   # In the Triton Server, run the following command to start the Triton Server:
   tritonserver --model-repository=/models
   ```
5. In the second Command Prompt, run the following command to start the Streamlit App:
   ```sh
   streamlit run app.py
   ```
6. If you want to run Triton Server SDK, run the following command in the third Command Prompt:
   ```sh
   # xx.yy is the version of the Triton Server
   docker run -it --net=host -v ${PWD}:/workspace/ nvcr.io/nvidia/tritonserver:xx.yy-py3-sdk bash

   # Run the following command to install some libraries:
    pip install google-generativeai pillow python-dotenv tritonclient
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Dao Ngoc Huy - dnhuy2802@gmail.com

Github Link: [https://github.com/dnhuy2802](https://github.com/dnhuy2802)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[TritonServer]: https://img.shields.io/badge/Triton%20Server-grey?style=for-the-badge&logo=nvidia
