
import os
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def create_fallback_diagram(prompt):
    """Create a labelled educational diagram based on the user's prompt."""

    text = prompt.lower()

    # Select a suitable diagram template
    if any(word in text for word in ["cnn", "convolution", "pooling"]):
        title = "Convolutional Neural Network (CNN)"
        stages = [
            "Input Image",
            "Convolution",
            "ReLU",
            "Pooling",
            "Flatten",
            "Fully Connected",
            "Output"
        ]

    elif any(word in text for word in ["gan", "generative adversarial"]):
        title = "Generative Adversarial Network (GAN)"
        stages = [
            "Random Noise",
            "Generator",
            "Fake Data",
            "Discriminator",
            "Real / Fake"
        ]

    elif any(word in text for word in ["transformer", "attention", "self-attention"]):
        title = "Transformer Architecture"
        stages = [
            "Input Tokens",
            "Embedding",
            "Positional Encoding",
            "Self Attention",
            "Feed Forward",
            "Output"
        ]

    elif any(word in text for word in ["ann", "neural network"]):
        title = "Artificial Neural Network (ANN)"
        stages = [
            "Input Layer",
            "Hidden Layer 1",
            "Hidden Layer 2",
            "Output Layer"
        ]

    elif any(word in text for word in ["deep learning", "deep neural"]):
        title = "Deep Learning Workflow"
        stages = [
            "Input Data",
            "Preprocessing",
            "Neural Network",
            "Training",
            "Prediction"
        ]

    elif any(word in text for word in ["machine learning", "ml model"]):
        title = "Machine Learning Workflow"
        stages = [
            "Collect Data",
            "Preprocess",
            "Train Model",
            "Evaluate",
            "Prediction"
        ]

    else:
        title = "AI Concept Workflow"
        stages = [
            "Input",
            "Processing",
            "Learning",
            "Analysis",
            "Output"
        ]

    # Create the diagram
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, len(stages))
    ax.set_ylim(0, 2)
    ax.axis("off")

    ax.set_title(title, fontsize=19, fontweight="bold", pad=20)

    box_width = 0.78
    box_height = 0.55
    y_position = 0.9

    for i, stage in enumerate(stages):
        x_position = i + 0.11

        box = FancyBboxPatch(
            (x_position, y_position),
            box_width,
            box_height,
            boxstyle="round,pad=0.04",
            linewidth=1.5,
            edgecolor="#245B8F",
            facecolor="#E6F1FA"
        )

        ax.add_patch(box)

        ax.text(
            x_position + box_width / 2,
            y_position + box_height / 2,
            stage,
            ha="center",
            va="center",
            fontsize=8,
            wrap=True
        )

        # Connect each stage to the next
        if i < len(stages) - 1:
            arrow = FancyArrowPatch(
                (x_position + box_width, y_position + box_height / 2),
                (x_position + 1.11, y_position + box_height / 2),
                arrowstyle="->",
                mutation_scale=13,
                linewidth=1.5,
                color="#245B8F"
            )
            ax.add_patch(arrow)

    ax.text(
        len(stages) / 2,
        0.35,
        "Educational illustration - simplified conceptual representation",
        ha="center",
        fontsize=9,
        color="dimgray"
    )

    plt.tight_layout()

    image_buffer = BytesIO()
    fig.savefig(
        image_buffer,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)

    image_buffer.seek(0)
    return image_buffer.getvalue()


def generate_image(prompt):
    """
    Try Hugging Face image generation first.
    If it fails, generate a relevant educational diagram locally.

    Returns:
        image_bytes, generation_source
    """

    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    if token:
        try:
            from huggingface_hub import InferenceClient

            model = os.getenv(
                "HF_IMAGE_MODEL",
                "black-forest-labs/FLUX.1-dev"
            )

            client = InferenceClient(api_key=token)

            image = client.text_to_image(
                prompt=prompt,
                model=model
            )

            image_buffer = BytesIO()
            image.save(image_buffer, format="PNG")

            return image_buffer.getvalue(), "Hugging Face FLUX"

        except Exception as e:
            print(f"Hugging Face generation failed: {e}")

    # Automatic local fallback
    fallback_image = create_fallback_diagram(prompt)

    return fallback_image, "Python educational diagram fallback"
