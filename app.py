import streamlit as st
from PyPDF2 import PdfReader
import json
import re
import requests
from datetime import datetime

# ─── Fonction pour nettoyer le texte ─────────────────────────────────────────
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(\b\w+\b)(\s+\1)+', r'\1', text)
    return text.strip()

# ─── Fonction pour appeler l'API Groq ────────────────────────────────────────
def generate_quiz_groq(text, num_questions, quiz_type, difficulty, language, api_key):
    type_map = {
        "Choix multiple (QCM)": "QCM avec 4 options A) B) C) D) — indiquer la bonne réponse",
        "Vrai / Faux":          "Vrai/Faux — indiquer la bonne réponse",
        "Réponse courte":       "Réponse courte — fournir une réponse modèle concise",
        "Mixte":                "Mixte : combiner QCM, Vrai/Faux et réponse courte"
    }
    question_format = type_map.get(quiz_type, type_map["Choix multiple (QCM)"])

    prompt = f"""Tu es un expert pédagogue. En te basant UNIQUEMENT sur le document ci-dessous, génère exactement {num_questions} questions de quiz en {language}.

Règles :
- Type : {question_format}
- Difficulté : {difficulty}
- Numéroter chaque question (Q1, Q2, ...)
- Pour QCM : lister A) B) C) D) puis "✅ Bonne réponse : X)"
- Pour Vrai/Faux : énoncer puis "✅ Bonne réponse : Vrai/Faux"
- Pour réponse courte : question puis "✅ Réponse : ..."
- Ajouter une explication courte (1-2 phrases) pour chaque réponse
- Séparer chaque question par une ligne vide

Document :
\"\"\"{text[:6000]}\"\"\"

Génère le quiz maintenant :"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 3000,
            "temperature": 0.7
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Erreur API Groq: {response.status_code} — {response.text}")

# ─── Configuration de la page ────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz Generator AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Styles CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .title-section {
        text-align: center;
        padding: 30px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 30px;
    }
    .title-section h1 { font-size: 2.5em; margin: 0; }
    .title-section p  { font-size: 1.1em; margin: 10px 0 0 0; opacity: 0.9; }
    .quiz-box {
        background: #f8f9ff;
        border-radius: 12px;
        padding: 24px;
        border-left: 5px solid #667eea;
        margin-top: 20px;
        white-space: pre-wrap;
        font-size: 1em;
        line-height: 1.8;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover { opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# ─── En-tête ──────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class='title-section'>
        <h1>🎯 Quiz Generator AI</h1>
        <p>Générateur de quiz intelligent — Propulsé par Groq (Gratuit)</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Barre latérale ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Paramètres")

    api_key = st.text_input(
        "🔑 Clé API Groq",
        type="password",
        placeholder="gsk_...",
        help="Obtenez votre clé GRATUITE sur https://console.groq.com"
    )
    st.markdown("🆓 [Obtenir une clé gratuite](https://console.groq.com)")

    st.divider()

    with st.expander("🔧 Réglages du quiz", expanded=True):
        num_questions = st.slider("Nombre de questions", min_value=3, max_value=15, value=5)
        quiz_type = st.selectbox(
            "Type de questions",
            ["Choix multiple (QCM)", "Vrai / Faux", "Réponse courte", "Mixte"]
        )
        difficulty = st.select_slider(
            "Difficulté",
            options=["Facile", "Moyen", "Difficile"],
            value="Moyen"
        )
        language = st.selectbox("Langue du quiz", ["Français", "Anglais", "Arabe"])

    st.divider()
    st.success("✅ 100% Gratuit avec Groq !")
    st.info("⚡ Modèle : Llama 3.3 70B")

# ─── Onglets ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📤 Générer", "📋 Historique", "❓ Aide"])

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — Génération
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📄 Télécharger un document PDF")
        uploaded_file = st.file_uploader("Sélectionnez un fichier PDF", type="pdf", label_visibility="collapsed")
    with col2:
        st.write("")
        st.write("")
        file_size = f"{uploaded_file.size / 1024 / 1024:.2f} MB" if uploaded_file else "N/A"
        st.metric("Taille du fichier", file_size)

    if uploaded_file is None:
        st.warning("👈 Veuillez télécharger un fichier PDF pour commencer")
    else:
        try:
            pdf_reader = PdfReader(uploaded_file)
            st.success(f"✅ PDF chargé : {len(pdf_reader.pages)} page(s)")

            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            text = clean_text(text)

            if not text.strip():
                st.error("❌ Aucun texte extrait. Vérifiez que le PDF n'est pas une image scannée.")
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("Caractères", f"{len(text):,}")
                c2.metric("Mots", f"{len(text.split()):,}")
                c3.metric("Pages", len(pdf_reader.pages))

                with st.expander("👁️ Aperçu du texte extrait"):
                    st.write(text[:800] + ("..." if len(text) > 800 else ""))

                st.divider()

                col_btn = st.columns([1, 2, 1])[1]
                with col_btn:
                    generate = st.button("🚀 Générer le Quiz", use_container_width=True)

                if generate:
                    if not api_key:
                        st.error("❌ Entrez votre clé API Groq dans la barre latérale.")
                        st.stop()

                    with st.spinner("⚡ Groq génère votre quiz..."):
                        try:
                            quiz_text = generate_quiz_groq(
                                text, num_questions, quiz_type, difficulty, language, api_key
                            )

                            st.markdown(
                                f"<div class='quiz-box'>{quiz_text}</div>",
                                unsafe_allow_html=True
                            )
                            st.success("✅ Quiz généré avec succès !")
                            st.balloons()

                            if "history" not in st.session_state:
                                st.session_state.history = []
                            st.session_state.history.append({
                                "date":       datetime.now().strftime("%d/%m/%Y %H:%M"),
                                "filename":   uploaded_file.name,
                                "questions":  num_questions,
                                "type":       quiz_type,
                                "difficulty": difficulty,
                                "language":   language,
                                "content":    quiz_text
                            })

                            st.divider()
                            st.subheader("📥 Télécharger le quiz")
                            dl1, dl2 = st.columns(2)
                            with dl1:
                                st.download_button(
                                    label="📄 Télécharger (TXT)",
                                    data=quiz_text,
                                    file_name=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain",
                                    use_container_width=True
                                )
                            with dl2:
                                json_data = {
                                    "title": "Quiz généré par Groq AI",
                                    "date": datetime.now().isoformat(),
                                    "source": uploaded_file.name,
                                    "questions": num_questions,
                                    "type": quiz_type,
                                    "difficulty": difficulty,
                                    "language": language,
                                    "content": quiz_text
                                }
                                st.download_button(
                                    label="📋 Télécharger (JSON)",
                                    data=json.dumps(json_data, ensure_ascii=False, indent=2),
                                    file_name=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json",
                                    use_container_width=True
                                )

                        except Exception as e:
                            st.error(f"❌ Erreur : {str(e)}")

        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du PDF : {str(e)}")

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — Historique
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("📊 Historique des quiz générés")
    if "history" not in st.session_state or not st.session_state.history:
        st.info("💾 Aucun quiz généré pour l'instant.")
    else:
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"📄 {entry['filename']} — {entry['date']} ({entry['questions']} questions)"):
                st.markdown(f"**Type :** {entry['type']} | **Difficulté :** {entry['difficulty']} | **Langue :** {entry['language']}")
                st.text(entry["content"])
                st.download_button(
                    label="📥 Télécharger",
                    data=entry["content"],
                    file_name=f"quiz_{i+1}.txt",
                    mime="text/plain",
                    key=f"dl_history_{i}"
                )
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.history = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 — Aide
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("❓ Guide d'utilisation")
    st.markdown("""
    ### Comment utiliser cette application ?
    1. Obtenez une clé gratuite sur **console.groq.com**
    2. Entrez la clé dans la barre latérale
    3. Téléchargez un PDF
    4. Cliquez sur **Générer le Quiz**
    5. Téléchargez en TXT ou JSON

    ### Dépendances
    ```bash
    pip install streamlit PyPDF2 requests
    ```

    ### Lancer
    ```bash
    streamlit run app.py
    ```

    ### Pourquoi Groq ?
    | Critère | GPT-2 | Groq (Llama 3) |
    |---|---|---|
    | Qualité | ❌ Mauvaise | ✅ Excellente |
    | Gratuit | ✅ | ✅ |
    | Quota | ✅ Illimité | ✅ 14400/jour |
    | Vitesse | 🐢 Lent | ⚡ Ultra rapide |
    """)

# ─── Pied de page ─────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; margin-top: 20px;'>
    <p>🤖 Quiz Generator AI — Propulsé par Groq (Llama 3) | Créé avec Streamlit</p>
    <p style='font-size: 0.8em;'>© 2026 — 100% Gratuit</p>
</div>
""", unsafe_allow_html=True)