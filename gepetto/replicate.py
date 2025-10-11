import json
import requests
import replicate
import random
import os

async def generate_image(prompt, aspect_ratio="1:1", output_format="webp", output_quality=90, enhance_prompt=True):
    model = get_random_image_model()
    input_params, cost = get_input_for_model(model, prompt, aspect_ratio)
    print(f"Using image model: {model} with cost: {cost}")
    output = await replicate.async_run(
        model,
        input=input_params,
    )
    if isinstance(output, list):
        image_url = output[0]
    else:
        image_url = output
    # strip any training :hash from the model name, eg nvidia/sana:c6b5d2b7459910fec94432e9e1203c3cdce92d6db20f714f1355747990b52fa6
    model_name = model.split(":")[0]
    return image_url, model_name, cost

async def generate_video(prompt, model="wan-video/wan-2.2-t2v-fast"):
    input = {
        "prompt": prompt,
        "go_fast": True,
        "num_frames": 81,
        "resolution": "480p",
        "aspect_ratio": "16:9",
        "sample_shift": 12,
        "optimize_prompt": False,
        "frames_per_second": 16,
        "lora_scale_transformer": 1,
        "lora_scale_transformer_2": 1
    }
    output = await replicate.async_run(
        model,
        input=input
    )
    cost = 0.05
    if isinstance(output, list):
        video_url = output[0]
    else:
        video_url = output

    # strip any training :hash from the model name, eg nvidia/sana:c6b5d2b7459910fec94432e9e1203c3cdce92d6db20f714f1355747990b52fa6
    model_name = model.split(":")[0]
    return video_url, model_name, cost

def get_input_for_model(model, prompt, aspect_ratio):
    if model.startswith("black-forest-labs/"):
        input = {
            "prompt": prompt,
            "num_outputs": 1,
            "aspect_ratio": aspect_ratio,
            "disable_safety_checker": True,
            "output_format": "jpg",
        }
        cost = 0.04
    elif model.startswith("tencent/"):
        input = {
            "prompt": prompt,
            "disable_safety_checker": True,
        }
        cost = 0.08
    elif model.startswith("qwen/"):
        input = {
            "prompt": prompt,
        }
        cost = 0.025
    elif model.startswith("bria/"):
        input = {
            "prompt": prompt,
        }
        cost = 0.04
    elif model.startswith("prunaai/"):
        input = {
            "prompt": prompt,
            "seed": -1,
        }
        cost = 0.02
    elif model.startswith("openai/"):
        input = {
            "prompt": prompt,
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "moderation": "low",
        }
        if "mini" in model:
            cost = 0.01
        else:
            cost = 0.04
    elif model.startswith("recraft-ai/"):
        input={
            "size": "1365x1024",
            "style": "any",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio
        }
        cost = 0.04
    elif model.startswith("ideogram-ai/"):
        input={
            "prompt": prompt,
            "resolution": "None",
            "style_type": "None",
            "aspect_ratio": aspect_ratio,
            "magic_prompt_option": "Auto"
        }
        cost = 0.06
    elif model.startswith("bytedance/seedream-3"):
        input={
            "size": "regular",
            "width": 2048,
            "height": 2048,
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "guidance_scale": 2.5
        }
        cost = 0.003
    elif model.startswith("bytedance/seedream-4"):
        input={
            "size": "2K",
            "width": 2048,
            "height": 2048,
            "prompt": prompt,
            "max_images": 1,
            "image_input": [],
            "aspect_ratio": "4:3",
            "sequential_image_generation": "disabled"
        }
        cost = 0.003
    elif model.startswith("luma/"):
        input = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "image_reference_weight": 0.85,
            "style_reference_weight": 0.85
        }
        cost = 0.02
    elif model.startswith("google/gemini"):
        input={
            "prompt": prompt,
        }
        cost = 0.039
    elif model.startswith("google/"):
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "safety_filter_level": "block_only_high"
        }
        cost = 0.04
    elif model.startswith("minimax/"):
        input = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio
        }
        cost = 0.03
    else:
        # default to sana model format input parameters
        input = {
            "width": 1024,
            "height": 1024,
            "prompt": prompt,
            "guidance_scale": 5,
            "negative_prompt": "",
            "pag_guidance_scale": 2,
            "num_inference_steps": 18
        }
        cost = 0.003
    return input, cost

def get_random_image_model():
    model_options = [
         "black-forest-labs/flux-1.1-pro",
         "black-forest-labs/flux-krea-dev",
         "bria/image-3.2",
         "google/imagen-4",
         "google/gemini-2.5-flash-image",
         "qwen/qwen-image",
         "bytedance/seedream-4",
         "tencent/hunyuan-image-3",
    ]
    if os.getenv("ENABLE_GPT_IMAGE", None) is not None:
        model_options.append("openai/gpt-image-1")
        model_options.append("openai/gpt-image-1-mini")
    model = random.choice(model_options)
    return model
