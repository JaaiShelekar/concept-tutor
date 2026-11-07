
import streamlit as st
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


@st.cache_resource(show_spinner="Loading BLIP model... Please wait.")
def load_blip_model():
    model_id = "Salesforce/blip-image-captioning-base"

    processor = BlipProcessor.from_pretrained(model_id)
    model = BlipForConditionalGeneration.from_pretrained(model_id)

    model.eval()

    return processor, model


def caption_image(uploaded_file):
    processor, model = load_blip_model()

    image = Image.open(uploaded_file).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=60,
            num_beams=5,
            repetition_penalty=1.5
        )

    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption
