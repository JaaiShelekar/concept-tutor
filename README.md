# AI–ML–DL Concept Tutor

An educational Streamlit application that explains Artificial Intelligence, Machine Learning and Deep Learning concepts at School, Undergraduate and Expert levels.

## Features

- Gemini-powered concept explanations with zero-shot, few-shot and concise step-by-step prompting.
- Temperature control and prompt comparison.
- Conversational chatbot with bounded session history.
- PDF syllabus question answering using Sentence-BERT retrieval and Gemini-generated grounded responses.
- Optional BLIP diagram captioning.
- Optional BERT attention heatmap.
- Optional hosted diffusion image generation.
- Text-to-speech audio summaries using gTTS.
- Responsible-AI guidance and an evaluation template.

## Syllabus mapping

| Unit | Implementation |
|---|---|
| I – Foundations of Generative AI | Prompt techniques, temperature and prompt comparison |
| II – GANs and LLMs | Gemini chatbot, conversation memory and separate BERT attention visualization |
| III – GPT, BERT and Multimodal AI | PDF RAG and BLIP image captioning |
| IV – Generative AI Tools and Techniques | Hosted image generation and gTTS audio |
| V – Responsible AI | Evidence display, unsupported-question response, limitations and evaluation plan |

## Requirements

- Python 3.10 or newer
- Gemini API key
- Internet connection for Gemini and first-time model downloads
- Optional: additional memory for Sentence-BERT, BLIP and BERT features

## Setup (Windows / VS Code)

Open a terminal in the project folder:

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a file named `.env` by copying `.env.example`. Put your Gemini API key in `.env`:

```text
GEMINI_API_KEY=your_actual_key
GEMINI_MODEL=gemini-2.5-flash
```

Never share the `.env` file or commit it to a public repository.

Run:

```bash
streamlit run app.py
```

## Optional model features

For PDF semantic retrieval, BLIP and attention visualization, install:

```bash
pip install -r requirements-optional.txt
```

The first use may download large model files. These optional features may be slow or unavailable on low-memory computers.

For hosted image generation, configure `HUGGINGFACEHUB_API_TOKEN` and `HF_IMAGE_ENDPOINT` in `.env`. The endpoint must be supported by the inference provider and model you choose. Image generation is not required for the core tutor to start.

## Evaluation

The required test matrix is in `evaluation/test_cases.json`. Use `evaluation/evaluation_template.csv` to record actual observations for ANN, CNN and GAN at all three levels. Evaluate correctness, clarity, technical depth, relevance, completeness and latency. Do not enter invented scores.

A suggested manual procedure:
1. Run each of the nine concept/level combinations.
2. Save the generated response.
3. Review it against trusted course material.
4. Rate each criterion using a documented scale (for example, 1–5).
5. Record response time and note any incorrect or unsupported output.
6. Test a question not covered by the uploaded notes and check whether the app expresses uncertainty.

## Limitations

- Gemini output may contain errors and should be checked against course material.
- RAG retrieval quality depends on PDF text quality and chunking. Scanned PDFs are not OCR-processed.
- Similarity scores help retrieve passages; they do not prove factual correctness.
- BLIP may miss labels, arrows and detailed diagram relationships.
- BERT attention weights are model-specific and are not a complete explanation of reasoning or Gemini internals.
- Hosted image inference depends on provider access, endpoint configuration, model availability and quotas.
- gTTS requires internet access.

## Privacy and security

- Keep API keys in `.env`; never hardcode them.
- Do not upload confidential or personally identifying documents.
- Uploaded PDF text is processed in the running app for retrieval; review the behavior of any external API before sending excerpts to it.

## Future enhancements

- OCR for scanned PDFs.
- Automated evaluation with a reviewed rubric.
- Persistent user profiles and saved learning history.
- Better diagram-layout understanding.
- A configurable image-generation provider.
- Deployment after local testing.
