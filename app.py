import os
import streamlit as st
from dotenv import load_dotenv

from modules.llm_engine import GeminiTutor
from modules.rag_engine import SyllabusRAG
from modules.audio_generation import make_audio

load_dotenv()
st.set_page_config(page_title="Concept Tutor", page_icon="🎓", layout="wide")

PAGES = [
    "Home", "Concept Tutor", "Prompt Comparison", "AI Chatbot",
    "Syllabus Notes – RAG", "Diagram Explainer", "Attention Visualizer",
    "AI Image Generator", "Audio Summary", "Responsible AI & Evaluation"
]
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_explanation" not in st.session_state:
    st.session_state.last_explanation = ""

with st.sidebar:
    st.title("🎓 Concept Tutor")
    st.caption("AI • Machine Learning • Deep Learning")
    page = st.radio("Navigate", PAGES, index=PAGES.index(st.session_state.page))
    st.session_state.page = page
    st.divider()
    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()

@st.cache_resource
def get_tutor():
    return GeminiTutor()

def tutor_or_error():
    try:
        return get_tutor()
    except Exception as e:
        st.error(f"Gemini is not ready: {e}")
        return None

def explain_prompt(topic, level, style="zero-shot", temperature=0.4, context=None):
    style_instructions = {
        "zero-shot": "Explain directly without examples being supplied in the prompt.",
        "few-shot": "Use this pattern: define the concept, give a simple analogy, then give a practical example.",
        "step-by-step": "Give a concise, numbered explanation of the key steps. Do not reveal private internal reasoning."
    }
    levels = {
        "School": "Use simple words, short sentences and familiar examples. Avoid unnecessary jargon.",
        "Undergraduate": "Include technical details, algorithms, working principles and practical applications.",
        "Expert": "Include advanced terminology, mathematical foundations, architecture details and limitations."
    }
    context_text = (
    "Use only this supplied syllabus context where possible:\n" + context
    if context else ""
)
    return f"""You are an accurate educational tutor.
Explain: {topic}
Audience level: {level}. {levels[level]}
Prompting approach: {style}. {style_instructions[style]}
Include: definition, explanation, example, key characteristics, applications, advantages, limitations,
and a comparison table with related concepts. If uncertain, state the uncertainty.
{context_text}
"""

st.title("Concept Tutor")
st.caption("Learn AI, Machine Learning and Deep Learning at your own level.")

if page == "Home":
    st.header("Welcome to your AI learning companion")
    st.write("An educational tutor that explains AI concepts at school, undergraduate and expert levels.")
    st.subheader("What you can do")
    st.markdown("""
    - Learn concepts with level-specific explanations.
    - Compare zero-shot, few-shot and step-by-step prompts.
    - Ask follow-up questions in an AI chatbot.
    - Upload syllabus PDFs and ask questions using retrieval-augmented generation.
    - Explain diagrams, visualize attention and explore optional generative tools.
    - Review responsible-AI limitations and evaluation evidence.
    """)
    st.info("Start with **Concept Tutor** or upload your notes in **Syllabus Notes – RAG**.")
    st.divider()
    st.caption(
        "Built with: Python • Streamlit • Google Gemini API • "
        "Sentence Transformers • NumPy • PyMuPDF • gTTS • "
        "Hugging Face • BLIP • PyTorch • Matplotlib"
    )

elif page == "Concept Tutor":
    st.header("Concept Tutor")
    topic = st.text_input("Enter an AI / ML / DL concept", placeholder="e.g. Convolutional Neural Network")
    level = st.selectbox("Choose explanation level", ["School", "Undergraduate", "Expert"])
    style = st.selectbox("Prompting technique", ["zero-shot", "few-shot", "step-by-step"])
    if st.button("Explain concept", type="primary") and topic.strip():
        tutor = tutor_or_error()
        if tutor:
            with st.spinner("Generating explanation..."):
                try:
                    result, elapsed = tutor.generate(explain_prompt(topic, level, style), 0.4)
                    st.session_state.last_explanation = result
                    st.write(result)
                    st.caption(f"Response time: {elapsed:.2f} seconds")
                except Exception as e:
                    st.error(f"Generation failed: {e}")
    elif not topic.strip():
        st.caption("Enter a concept to begin.")

elif page == "Prompt Comparison":
    st.header("Compare prompting techniques")
    question = st.text_area("Enter one concept question", "Explain how a CNN recognizes an image.")
    level = st.selectbox("Audience level", ["School", "Undergraduate", "Expert"], key="compare_level")
    if st.button("Compare all three prompts", type="primary") and question.strip():
        tutor = tutor_or_error()
        if tutor:
            for style in ["zero-shot", "few-shot", "step-by-step"]:
                with st.expander(style.replace("-", " ").title(), expanded=True):
                    with st.spinner(f"Running {style}..."):
                        try:
                            answer, elapsed = tutor.generate(explain_prompt(question, level, style), 0.4)
                            st.write(answer)
                            st.caption(f"Latency: {elapsed:.2f}s")
                        except Exception as e:
                            st.error(str(e))
            st.warning("This page compares generated outputs and latency. Human quality ratings should be completed separately; no quality scores are fabricated.")

elif page == "AI Chatbot":
    st.header("AI Chatbot with conversation memory")
    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])
    user_text = st.chat_input("Ask a follow-up question...")
    if user_text:
        st.session_state.chat_history.append({"role":"user","content":user_text})
        tutor = tutor_or_error()
        if tutor:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Bound history to the latest 10 turns to control prompt size.
                        history = st.session_state.chat_history[-20:]
                        answer, elapsed = tutor.chat(history)
                        st.markdown(answer)
                        st.caption(f"Response time: {elapsed:.2f}s")
                        st.session_state.chat_history.append({"role":"assistant","content":answer})
                    except Exception as e:
                        st.error(str(e))
        st.rerun()

elif page == "Syllabus Notes – RAG":
    st.header("Syllabus Notes – Retrieval-Augmented Generation")
    st.write("Upload a text-based PDF, index its content, then ask questions grounded in the retrieved excerpts.")
    uploaded = st.file_uploader("Upload syllabus PDF", type=["pdf"])
    if uploaded:
        if st.button("Index PDF", type="primary"):
            try:
                rag = SyllabusRAG()
                with st.spinner("Extracting text and creating the index..."):
                    chunks = rag.index_pdf(uploaded)
                st.session_state.rag_chunks = chunks
                st.success(f"Indexed {len(chunks)} text chunks.")
            except Exception as e:
                st.error(f"Could not index PDF: {e}")
    question = st.text_input("Ask a question about your uploaded notes")
    if st.button("Ask from notes") and question.strip():
        chunks = st.session_state.get("rag_chunks", [])
        if not chunks:
            st.warning("Upload and index a PDF first.")
        else:
            try:
                rag = SyllabusRAG()
                matches = rag.retrieve(question, chunks)
                context = "\n\n".join([f"[Page {m['page']}] {m['text']}" for m in matches])
                tutor = tutor_or_error()
                if tutor:
                    prompt = f"""Answer using only the context below. If it does not support an answer, say exactly:
"I'm not sure based on the provided syllabus notes."
Cite page numbers and do not invent references.
QUESTION: {question}
CONTEXT:
{context}"""
                    answer, elapsed = tutor.generate(prompt, 0.2)
                    st.markdown(answer)
                    st.caption(f"Response time: {elapsed:.2f}s")
                    with st.expander("Retrieved evidence"):
                        for m in matches:
                            st.markdown(f"**Page {m['page']}**")
                            st.write(m["text"])
            except Exception as e:
                st.error(f"RAG query failed: {e}")



elif page == "Diagram Explainer":
    st.header("Diagram Explainer")

    image = st.file_uploader(
        "Upload a diagram or educational image",
        type=["png", "jpg", "jpeg"]
    )

    question = st.text_input(
        "What would you like to understand about it?",
        "Explain the main components and their relationship."
    )

    if image:
        st.image(
            image,
            caption="Uploaded image",
            use_container_width=True
        )

        if st.button("Explain diagram"):
            try:
                from modules.image_captioning import caption_image

                tutor = tutor_or_error()

                if tutor:
                    with st.spinner("Analyzing your diagram..."):

                        # Generate BLIP caption
                        caption = caption_image(image)

                        st.write("**Image caption:**", caption)

                        # Read uploaded image
                        image.seek(0)
                        image_bytes = image.getvalue()

                        # Send image and caption to Gemini
                        answer, latency = tutor.generate(
                            prompt=f"""
You are an educational AI tutor.

Analyze the uploaded educational diagram.

BLIP image caption:
{caption}

Student's question:
{question}

Explain:
1. What the diagram represents.
2. Its main components.
3. The function of each component.
4. How the components are connected.
5. The overall working process.

Use simple educational language.
Do not invent labels or details that are
not visible in the image.
Mention anything that is unclear.
""",
                            temperature=0.3,
                            image_bytes=image_bytes,
                            image_mime_type=image.type
                        )

                    st.subheader("Diagram Explanation")
                    st.write(answer)

                    st.caption(
                        f"Gemini response time: {latency:.2f} seconds"
                    )

            except Exception as e:
                st.error(f"Diagram explanation failed: {e}")


elif page == "Attention Visualizer":
    st.header("Attention Visualizer")
    text = st.text_input("Enter a sentence", "Transformers use attention to process relationships between tokens.")
    if st.button("Visualize attention"):
        try:
            from modules.attention_visualizer import attention_figure
            fig = attention_figure(text)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Optional attention model unavailable: {e}")
            st.info("Install the optional dependencies and retry. The core tutor does not depend on this page.")


elif page == "AI Image Generator":
    st.header("AI Image Generator")

    st.write(
        "Generate educational illustrations using AI. "
        "If the hosted service is unavailable, a local "
        "Python diagram generator will be used."
    )

    prompt = st.text_area(
        "Describe an educational illustration",
        "A simple labelled illustration of a convolutional neural network."
    )

    if st.button("Generate illustration"):
        if not prompt.strip():
            st.warning("Please enter a description first.")

        else:
            try:
                from modules.image_generation import generate_image

                with st.spinner("Generating your illustration..."):
                    img, source = generate_image(prompt)

                st.success(f"Illustration generated using: {source}")

                st.image(
                    img,
                    caption="Educational illustration",
                    use_container_width=True
                )

                st.download_button(
                    "Download image",
                    data=img,
                    file_name="educational_illustration.png",
                    mime="image/png"
                )

                if source == "Python educational diagram fallback":
                    st.info(
                        "Hugging Face image generation was unavailable. "
                        "A relevant educational diagram was generated "
                        "locally instead. This is a simplified "
                        "programmatic illustration, not an AI-generated image."
                    )

            except Exception as e:
                st.error(f"Image generation failed: {e}")


elif page == "Audio Summary":
    st.header("Audio Summary")
    source = st.text_area("Enter or paste a concept explanation", st.session_state.get("last_explanation",""))
    if st.button("Generate audio") and source.strip():
        try:
            audio = make_audio(source)
            st.audio(audio, format="audio/mp3")
            st.download_button("Download audio", data=audio, file_name="concept_summary.mp3", mime="audio/mpeg")
        except Exception as e:
            st.error(f"Audio generation failed: {e}")

elif page == "Responsible AI & Evaluation":
    st.header("Responsible AI & Evaluation")
    st.markdown("""
    **Grounding rule:** In syllabus mode, answers should be supported by retrieved excerpts. If the notes do not support an answer, the tutor should say:  
    *“I'm not sure based on the provided syllabus notes.”*

    **Important limitations**
    - Gemini can produce incorrect or incomplete information.
    - Retrieval can miss relevant passages, especially in scanned PDFs.
    - BLIP captions may omit labels, arrows or technical relationships.
    - Attention weights are not a definitive explanation of model reasoning.
    - Hosted image-generation availability and quotas may change.
    - Text-to-speech quality depends on language and pronunciation support.

    **Responsible use**
    - Use the tutor as a learning aid, not as the sole source for high-stakes decisions.
    - Do not upload confidential or personally identifying documents.
    - Keep API keys private and outside source code.
    """)
    st.subheader("Required evaluation plan")
    st.write("Run and record the nine required concept/level combinations: ANN, CNN and GAN at School, Undergraduate and Expert levels.")
    st.warning("No evaluation scores are displayed here until the tests have actually been run and reviewed.")
    st.download_button("Download blank evaluation template", data="concept,level,correctness,clarity,technical_depth,relevance,completeness,latency_seconds,notes\n", file_name="evaluation_template.csv", mime="text/csv")
