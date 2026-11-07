# Concept Tutor 🎓

An AI-powered learning platform designed to simplify complex Artificial Intelligence (AI), Machine Learning (ML), and Deep Learning (DL) concepts through interactive explanations and practical learning tools.

**Live Application:** https://jaaishelekar-concept-tutor-app-vkifxz.streamlit.app/

## Project Overview

Concept Tutor is an interactive educational application that helps students understand AI, ML, and DL concepts in a simple and engaging way. It uses Google's Gemini API along with various AI-powered tools to provide explanations, compare prompts, analyze diagrams, visualize attention, and generate learning resources.

The platform aims to make technical learning more accessible through interactive and multimodal features.

## Features

- **AI Concept Tutor:** Explains complex AI, ML, and DL concepts using different prompting approaches.
- **Prompt Comparison:** Compares outputs generated using different prompting techniques.
- **AI Chatbot:** Provides an interactive conversational interface for asking questions and exploring concepts.
- **Syllabus Notes – RAG:** Retrieves relevant information from available learning materials and generates context-based answers.
- **Diagram Explainer:** Analyzes uploaded diagrams and explains their components using AI.
- **Attention Visualizer:** Visualizes attention patterns to help understand how transformer-based models process text.
- **AI Image Generator:** Generates images from text prompts.
- **Audio Summary:** Converts learning explanations into audio for listening.
- **Responsible AI & Evaluation:** Includes evaluation resources to assess responses and encourage responsible AI usage.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Generative AI | Google Gemini API |
| RAG | LangChain / FAISS (as implemented) |
| NLP & Embeddings | Sentence-BERT, BERT |
| Image Processing | BLIP, PIL |
| Image Generation | Hosted Diffusion Models |
| Audio | gTTS |
| Data Handling | NumPy, Pandas |
| Environment Management | 	python-dotenv |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/JaaiShelekar/concept-tutor.git
cd concept-tutor
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

### 3. Install Dependencies 

Install all project dependencies using the requirements file:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project's root directory and add the following:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace `your_gemini_api_key` with your own Gemini API key.

**Note:** Never upload your `.env` file or expose your API key publicly.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

## Evaluation

The project includes evaluation resources to test and assess the generated responses.

- `evaluation/test_cases.json` – Contains test cases for evaluating the application.
- `evaluation/evaluation_template.csv` – Provides a template for recording evaluation results.

## Limitations

- Response quality depends on the underlying Gemini model and API availability.
- AI-generated explanations may occasionally contain inaccurate information and should be verified.
- Some features depend on external APIs or model availability.
- Response time may vary depending on network connectivity and API demand.

## Privacy and Security

- API keys are managed through environment variables and Streamlit secrets.
- The `.env` file is excluded from version control.
- Users should avoid uploading confidential or sensitive documents.
- AI-generated responses should be reviewed before being used for academic or professional purposes.

## Future Enhancements

- Support for additional AI models.
- Improved response evaluation and accuracy.
- More interactive visualizations for AI and ML concepts.
- Expanded learning resources and personalized learning experiences.
- Enhanced user experience and interface improvements.

---

**Developed as an AI/ML learning project using Python, Streamlit, and Generative AI technologies.**