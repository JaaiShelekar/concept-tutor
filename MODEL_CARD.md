# Model Card – AI–ML–DL Concept Tutor

## 1. Project overview
An educational application for explaining AI, Machine Learning and Deep Learning concepts at three levels.

## 2. Intended use
Learning support, concept revision, syllabus question answering and exploration of model behavior. It is not a substitute for textbooks, instructors or expert review.

## 3. Models and services

| Model/service | Identifier | Role | Access mode |
|---|---|---|---|
| Google Gemini | Configured by `GEMINI_MODEL` (default in code: `gemini-2.5-flash`) | Concept explanations and chatbot | External API |
| Sentence-BERT | `sentence-transformers/all-MiniLM-L6-v2` | PDF chunk embeddings and retrieval | Locally downloaded model |
| BLIP | `Salesforce/blip-image-captioning-base` | Image captioning | Locally downloaded model |
| BERT | `google-bert/bert-base-uncased` | Token attention visualization | Locally downloaded model |
| Hosted diffusion model | Configured through `HF_IMAGE_ENDPOINT` | Optional image generation | External hosted inference |
| gTTS | Google Text-to-Speech service/library | Audio summaries | External service |

## 4. Architecture
Gemini is used for natural-language generation. Sentence-BERT creates embeddings for PDF passages. The app ranks passages using vector similarity and sends selected context to Gemini. BLIP and BERT are separate optional models.

## 5. Training and fine-tuning
No project-specific model training or fine-tuning is performed by this application. Pretrained models are used as published.

## 6. Inputs and outputs
- Text concept question and selected learning level → generated explanation.
- Conversation turns → chatbot response.
- PDF syllabus → extracted passages, retrieved evidence and grounded answer.
- Image → optional BLIP caption and explanation.
- Sentence → BERT token attention heatmap.
- Text → MP3 audio summary.
- Prompt and configured endpoint → optional generated image.

## 7. Evaluation
The project includes a nine-case evaluation matrix for ANN, CNN and GAN at School, Undergraduate and Expert levels. Performance results must be measured after execution and recorded in the evaluation CSV. No benchmark result is claimed in this model card.

## 8. Limitations and failure cases
Potential failures include hallucinated explanations, poor retrieval from scanned or poorly formatted PDFs, incomplete image captions, misleading interpretation of attention weights, API rate limits and unavailable hosted inference endpoints. Document observed failures during testing.

## 9. Bias, fairness and hallucination
Generated content may reflect limitations or biases in model training data. Verify important educational claims against reliable sources. RAG context can reduce unsupported answers but cannot guarantee correctness.

## 10. Safety and transparency
The app is intended for education. It communicates uncertainty for unsupported syllabus questions and identifies separate-model attention visualization.

## 11. Privacy and security
API credentials belong in environment variables. Avoid uploading sensitive documents. Text excerpts sent to Gemini are subject to the API provider's terms and data practices.

## 12. Licences and intellectual property
Check the current licence and usage terms for each model, API and hosted service before redistribution or commercial use. This project does not claim ownership of third-party models. Licence details should be verified from the official model cards and provider terms at the time of submission.

## 13. External dependencies
Google Gemini API, Hugging Face model hosting/inference where configured, and gTTS. Availability, pricing and quotas may change.

## 14. Ethical considerations
Use as a study aid, disclose AI-generated content where required by institutional policy, and independently verify answers.
