import re
import json
import streamlit as st
import ollama
from langdetect import detect

MODEL = "llama3.2"

# --- Preprocesamiento ---

def clean_text(text):
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "desconocido"

# --- LLM ---

def summarize(text):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Resume el texto en 3-5 puntos clave en espanol. Usa formato de lista con guiones. Solo los puntos, sin introduccion."},
            {"role": "user",   "content": text},
        ]
    )
    return response["message"]["content"].strip()

def get_sentiment(text):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": 'Responde SOLO con JSON: {"tono": "positivo/negativo/neutro/mixto", "razon": "frase corta"}'},
            {"role": "user",   "content": text},
        ]
    )
    raw = response["message"]["content"]
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return {"tono": "indeterminado", "razon": raw[:80]}

# --- Interfaz ---

st.title("Analizador de texto con LLM local")

text = st.text_area("Introduce tu texto (cualquier idioma)", height=200)

if st.button("Analizar", type="primary"):
    if not text.strip():
        st.warning("Introduce algun texto.")
    else:
        cleaned = clean_text(text)
        lang    = detect_language(cleaned)

        st.write(f"**Idioma detectado:** {lang} | **Palabras:** {len(cleaned.split())}")
        st.divider()

        with st.spinner("Generando resumen..."):
            summary = summarize(cleaned)
        st.markdown("**Resumen en espanol**")
        st.markdown(summary)

        st.divider()

        with st.spinner("Analizando tono..."):
            sentiment = get_sentiment(cleaned)
        st.markdown("**Tono del texto**")
        st.write(f"{sentiment.get('tono', '-').capitalize()} — {sentiment.get('razon', '-')}")