import cohere
import gradio as gr
import requests
from PIL import Image
import io

def generate_text(prompt,maxi,cohere_api_key):
    co = cohere.Client(cohere_api_key)

    response = co.generate(prompt=prompt,
                            temperature=0,
                            max_tokens=maxi)
    return response[0]

def generate_image(prompt,gradio_api_key):
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
        files={
            'prompt': (None, prompt, 'text/plain')
        },
        headers={'x-api-key': gradio_api_key}
    )

    if r.ok:
        images = Image.open(io.BytesIO(r.content))
        return images
    else:
        raise ValueError("Failed to generate image")

def text_and_image_generator(prompt,maxi,cohere_api_key,gradio_api_key):
    text = generate_text(prompt,maxi,cohere_api_key)
    image = generate_image(text,gradio_api_key)

    return text,image

app = gr.Interface(
    title="Story and Image Generator",
    fn=text_and_image_generator,
    inputs = [gr.inputs.Textbox(label="Enter your prompt to generate a story"),
    gr.inputs.Slider(1,1000,label="Story length :"),gr.inputs.Textbox(type="password",label="Cohere API key :"),gr.inputs.Textbox(type="password",label="Gradio API key :")],
    outputs= [gr.outputs.Textbox(label="Generated Story"),gr.outputs.Image(type="pil",label="Image based on the Generated story")]
)

app.launch(share=True)