# HF Spaces
import gradio as gr
import asyncio
import fal_client
import requests
from PIL import Image
from io import BytesIO
import time
import base64
import json
# --------------------------------------------
# Local Dev
import os
from dotenv import load_dotenv

load_dotenv()
FAL_KEY = os.getenv("FAL_KEY")
# --------------------------------------------

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
                "comfy/martintmv-git/sdxl-depthanything-rembg",
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
                time.sleep(2) # HTTP req retry mechanism
            else:
                return [f"Error: {str(e)}"], None

# SV3D, AnimateDiff
async def submit_sv3d(image_data, fps, loop_frames_count, gif_loop):
    retries = 3
    for attempt in range(retries):
        try:
            handler = await fal_client.submit_async(
                "comfy/martintmv-git/sv3d",
                arguments={
                    "loadimage_1": image_data,
                    "FPS (bigger number = more speed)": fps,
                    "Loop Frames Count": loop_frames_count,
                    "GIF Loop": gif_loop
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

            print("API Result:", result)

            gif_url = result["outputs"]["15"]["gifs"][0]["url"]
            return output_logs, gif_url
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
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

def submit_sync_sv3d(image_upload, fps, loop_frames_count, gif_loop):
    image_data = convert_image_to_base64(Image.open(image_upload))
    return asyncio.run(submit_sv3d(image_data, fps, loop_frames_count, gif_loop))

def run_gradio_app():
    with gr.Blocks() as demo:
        gr.Markdown("# Comfy Anything 🐈")
        gr.Markdown("### Community ComfyUI workflows running on [fal.ai](https://fal.ai)")
        gr.Markdown("#### Comfy Anything on [GitHub](https://github.com/martintmv-git/comfy-anything)")
        gr.Markdown("#### Support the project:")
        gr.Markdown("- [ko-fi.com/martintmv](https://ko-fi.com/martintmv) 🧡 Bitcoin address - bc1qs3q0rjpr9fvn9knjy5aktfr8w5duvvjpezkgt9")
        gr.Markdown("🚀 Want to run your own workflow? Follow the `README` guide and submit your workflow [here](https://huggingface.co/spaces/martintmv/ComfyAnything/tree/main/workflows) or open a [PR](https://huggingface.co/spaces/martintmv/ComfyAnything/discussions?new_pr=true).")

        with gr.Row(): 
            with gr.Column(scale=1):
                workflow = gr.Dropdown(label="Select Workflow", choices=["IC Light, Replace Background", "SDXL, Depth Anything, Replace Background", "SV3D"], value="IC Light, Replace Background")
                image_upload = gr.Image(label="Upload Image", type="filepath")
                positive_prompt = gr.Textbox(label="Positive Prompt", visible=True)
                negative_prompt = gr.Textbox(label="Negative Prompt", value="Watermark", visible=True)
                lightsource_start_color = gr.ColorPicker(label="Start Color", value="#FFFFFF", visible=True)
                lightsource_end_color = gr.ColorPicker(label="End Color", value="#000000", visible=True)
                fps = gr.Slider(label="FPS (bigger number = more speed)", minimum=1, maximum=60, step=1, value=8, visible=False)
                loop_frames_count = gr.Slider(label="Loop Frames Count", minimum=1, maximum=100, step=1, value=30, visible=False)
                gif_loop = gr.Checkbox(label="GIF Loop", value=True, visible=False)
                submit_btn = gr.Button("Submit")

            with gr.Column(scale=2):
                output_logs = gr.Textbox(label="Logs")
                output_result = gr.Image(label="Result")

        def update_ui(workflow):
            if workflow == "IC Light, Replace Background":
                return [gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)]
            elif workflow == "SDXL, Depth Anything, Replace Background":
                return [gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)]
            elif workflow == "SV3D":
                return [gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)]

        workflow.change(fn=update_ui, inputs=workflow, outputs=[positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color, fps, loop_frames_count, gif_loop])

        def on_submit(image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color, fps, loop_frames_count, gif_loop, workflow):
            if workflow == "IC Light, Replace Background":
                logs, image = submit_sync_ic_light_bria(image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color)
                return logs, image
            elif workflow == "SDXL, Depth Anything, Replace Background":
                logs, image = submit_sync_sdxl_rembg(image_upload, positive_prompt, negative_prompt)
                return logs, image
            elif workflow == "SV3D":
                logs, gif_url = submit_sync_sv3d(image_upload, fps, loop_frames_count, gif_loop)
                return logs, gif_url

        submit_btn.click(
            fn=on_submit,
            inputs=[image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color, fps, loop_frames_count, gif_loop, workflow],
            outputs=[output_logs, output_result]
        )

        gr.Examples(
            examples=[
                [example['input_image'], example['positive_prompt'], example['negative_prompt'], example.get('lightsource_start_color', "#FFFFFF"), example.get('lightsource_end_color', "#000000"), example.get('fps', 8), example.get('loop_frames_count', 30), example.get('gif_loop', True), example['workflow']]
                for example in examples
            ],
            inputs=[image_upload, positive_prompt, negative_prompt, lightsource_start_color, lightsource_end_color, fps, loop_frames_count, gif_loop, workflow],
            outputs=[output_logs, output_result],
            fn=on_submit,
            cache_examples=True
        )

    demo.launch()

if __name__ == "__main__":
    run_gradio_app()