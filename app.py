import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Kelly - The AI Skeptic Poet",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Kelly: The AI Skeptic Poet")
st.markdown(
    "*An AI scientist who speaks only in verse — questioning hype with evidence-based insight.*"
)

with st.sidebar:
    st.markdown("### About Kelly")
    st.markdown("""
    Kelly is an AI scientist who:
    - 🎭 Speaks only in poetry  
    - 🔍 Questions AI hype and broad claims  
    - 💡 Offers practical, evidence-based advice  
    - 📊 Values data over marketing promises  
    """)
    st.markdown("---")

    if st.button("🧹 Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

KELLY_PROMPT = """You are Kelly, an AI scientist and poet who responds to all questions EXCLUSIVELY in poetic form.

Core Traits:
- SKEPTICAL: Question broad AI claims, highlight limitations
- ANALYTICAL: Use evidence-based reasoning
- PROFESSIONAL: Maintain academic credibility
- POETIC: Every response must be a complete poem (8–16 lines)
- CONSTRUCTIVE: Offer practical alternatives

Poetic Style:
- Use rhyming couplets or blank verse
- Integrate technical language naturally
- Prioritize clarity over ornamentation
- End with an actionable insight or probing question

Rules:
1. Respond only in poetry
2. Never break character
3. Question hype, emphasize grounded reasoning
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Kelly anything about AI, ML, or Data Science..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Kelly is composing thoughtful verse..."):
                try:
                    conversation = f"{KELLY_PROMPT}\n\nUser: {prompt}\n\nKelly (respond in poetry):"
                    response = model.generate_content(
                        conversation,
                        generation_config={"max_output_tokens": 400}
                    )

                    if hasattr(response, "text") and response.text:
                        kelly_response = response.text.strip()
                    else:
                        kelly_response = "Kelly pauses — even poets need data to proceed."

                    st.markdown(f"```\n{kelly_response}\n```")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": kelly_response}
                    )

                except Exception as e:
                    error_text = f"Kelly encountered an issue: {e}"
                    st.error(error_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_text}
                    )