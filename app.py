import gradio as gr
import asyncio
import fal_client
import requests
from PIL import Image
from io import BytesIO
import time
import base64
import json

with open("examples/examples.json") as f:
    examples = json.load(f)

# IC Light, Replace Background
async def submit_ic_light_bria(image_data, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color):
    if not lightsource_start_color.startswith("#"):
        lightsource_start_color = f"#{lightsource_start_color}"
    if not lightsource_end_color.startswith("#"):
        lightsource_end_color = f"#{lightsource_end_color}"

    retries = 3
    for attempt in range(retries):
        try:
            handler = await fal_client.submit_async(
                "comfy/martintmv-git/ic-light-bria",
                arguments={
                    "loadimage_1": image_data,
                    "Positive Prompt": positive_prompt,
                    "Negative Prompt": negative_prompt,
                    "lightsource_start_color": lightsource_start_color,
                    "lightsource_end_color": lightsource_end_color
                },
            )

            log_index = 0
            output_logs = []
            async for event in handler.iter_events(with_logs=True):
                if isinstance(event, fal_client.InProgress):
                    if event.logs:
                        new_logs = event.logs[log_index:]
                        for log in new_logs:
                            output_logs.append(log["message"])
                        log_index = len(event.logs)

            result = await handler.get()
            output_logs.append("Processing completed")

            # Debug log
            print("API Result:", result)

            # Extract the image URL
            image_url = result["outputs"]["9"]["images"][0]["url"]
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            return output_logs, image
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # HTTP req retry mechanism
            else:
                return [f"Error: {str(e)}"], None

# SDXL, Depth Anything, Replace Background
async def submit_sdxl_rembg(image_data, positive_prompt, negative_prompt):
    retries = 3
    for attempt in range(retries):
        try:
            handler = await fal_client.submit_async(
                "comfy/martintmv-git/sdxl-rembg",
                arguments={
                    "loadimage_1": image_data,
                    "Positive prompt": positive_prompt,
                    "Negative prompt": negative_prompt
                },
            )

            log_index = 0
            output_logs = []
            async for event in handler.iter_events(with_logs=True):
                if isinstance(event, fal_client.InProgress):
                    if event.logs:
                        new_logs = event.logs[log_index:]
                        for log in new_logs:
                            output_logs.append(log["message"])
                        log_index = len(event.logs)

            result = await handler.get()
            output_logs.append("Processing completed")

            # Debug log
            print("API Result:", result)

            # Extract the image URL
            image_url = result["outputs"]["9"]["images"][0]["url"]
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            return output_logs, image
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # HTTP req retry mechanism
            else:
                return [f"Error: {str(e)}"], None

def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

def submit_sync_ic_light_bria(image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color):
    image_data = convert_image_to_base64(Image.open(image_upload))
    return asyncio.run(submit_ic_light_bria(image_data, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color))

def submit_sync_sdxl_rembg(image_upload, positive_prompt, negative_prompt):
    image_data = convert_image_to_base64(Image.open(image_upload))
    return asyncio.run(submit_sdxl_rembg(image_data, positive_prompt, negative_prompt))

def run_gradio_app():
    with gr.Blocks() as demo:
        gr.Markdown("# Comfy Anything 🐈")
        gr.Markdown("### Custom ComfyUI workflows running on [fal.ai](https://fal.ai)")

        with gr.Row():
            with gr.Column(scale=1):
                workflow = gr.Dropdown(label="Select Workflow", choices=["IC Light, Replace Background", "SDXL, Depth Anything, Replace Background"], value="IC Light, Replace Background")
                image_upload = gr.Image(label="Upload Image", type="filepath")
                positive_prompt = gr.Textbox(label="Positive Prompt")
                negative_prompt = gr.Textbox(label="Negative Prompt", value="Watermark")
                lightsource_start_color = gr.ColorPicker(label="Start Color", value="#FFFFFF", visible=True)
                lightsource_end_color = gr.ColorPicker(label="End Color", value="#000000", visible=True)
                submit_btn = gr.Button("Submit")

            with gr.Column(scale=2):
                output_logs = gr.Textbox(label="Logs")
                output_result = gr.Image(label="Result")

        def update_ui(workflow):
            if workflow == "IC Light, Replace Background":
                return gr.update(visible=True), gr.update(visible=True)
            else:
                return gr.update(visible=False), gr.update(visible=False)

        workflow.change(fn=update_ui, inputs=workflow, outputs=[lightsource_start_color, lightsource_end_color])

        def on_submit(image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color, workflow):
            if workflow == "IC Light, Replace Background":
                return submit_sync_ic_light_bria(image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color)
            else:
                return submit_sync_sdxl_rembg(image_upload, positive_prompt, negative_prompt)

        submit_btn.click(
            fn=on_submit,
            inputs=[image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color, workflow],
            outputs=[output_logs, output_result]
        )

        gr.Examples(
            examples=[
                [example['input_image'], example['positive_prompt'], example['negative_prompt'], example.get('lightsource_start_color', ""), example.get('lightsource_end_color', ""), example['workflow']]
                for example in examples
            ],
            inputs=[image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color, workflow],
            outputs=[output_logs, output_result],
            fn=on_submit,
            cache_examples=True
        )

    demo.launch()

if __name__ == "__main__":
    run_gradio_app()