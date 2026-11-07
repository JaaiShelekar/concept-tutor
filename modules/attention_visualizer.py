def attention_figure(text):
    import torch
    import matplotlib.pyplot as plt
    from transformers import AutoTokenizer, AutoModel
    model_id = "google-bert/bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModel.from_pretrained(model_id, output_attentions=True)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=64)
    with torch.no_grad():
        outputs = model(**inputs)
    # Average heads from the final layer for a compact token-to-token view.
    attention = outputs.attentions[-1][0].mean(dim=0).cpu().numpy()
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    fig, ax = plt.subplots(figsize=(max(7, len(tokens)*0.45), max(5, len(tokens)*0.4)))
    ax.imshow(attention, aspect="auto")
    ax.set_xticks(range(len(tokens))); ax.set_xticklabels(tokens, rotation=70, ha="right")
    ax.set_yticks(range(len(tokens))); ax.set_yticklabels(tokens)
    ax.set_title("BERT final-layer attention (averaged across heads)")
    fig.tight_layout()
    return fig
