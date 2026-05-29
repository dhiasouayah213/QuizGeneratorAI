import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline

# Configuration de la page
st.set_page_config(page_title="Quiz Generator AI", layout="wide", page_icon="📚")

st.title("🎯 Quiz Generator AI")
st.write("Bienvenue dans le générateur automatique de quiz à partir de documents PDF")

# Barre latérale pour les paramètres
st.sidebar.header("⚙️ Paramètres")
num_questions = st.sidebar.slider(
    "Nombre de questions",
    min_value=3,
    max_value=10,
    value=5
)
max_length = st.sidebar.slider(
    "Longueur maximale de réponse",
    min_value=256,
    max_value=1024,
    value=512,
    step=128
)

# Téléchargement du fichier PDF
uploaded_file = st.file_uploader(
    "📄 Choisir un fichier PDF",
    type="pdf"
)

if uploaded_file is None:
    st.info("👈 Veuillez télécharger un fichier PDF pour commencer")
    st.stop()

# Extraction du texte du PDF
try:
    pdf_reader = PdfReader(uploaded_file)
    st.success(f"✅ PDF chargé avec {len(pdf_reader.pages)} page(s)")
    
    text = ""
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text
    
    if not text.strip():
        st.error("❌ Aucun texte n'a pu être extrait du PDF")
        st.stop()
    
    # Afficher un aperçu du texte
    with st.expander("👁️ Aperçu du texte extrait"):
        preview = text[:500] + "..." if len(text) > 500 else text
        st.text(preview)
    
except Exception as e:
    st.error(f"❌ Erreur lors de la lecture du PDF: {str(e)}")
    st.stop()

# Initialiser le modèle
st.info("⏳ Chargement du modèle d'IA...")
try:
    generator = pipeline(
        "text-generation",
        model="gpt2"
    )
    st.success("✅ Modèle chargé!")
except Exception as e:
    st.error(f"❌ Erreur lors du chargement du modèle: {str(e)}")
    st.stop()

# Générer le quiz
if st.button("🚀 Générer le Quiz", use_container_width=True):
    with st.spinner("Génération du quiz en cours..."):
        try:
            # Créer le prompt
            prompt = f"""Generate {num_questions} multiple choice questions from this text:

{text[:1000]}

Questions:"""
            
            # Générer avec le modèle
            result = generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7
            )
            
            quiz_text = result[0]["generated_text"]
            
            st.subheader("📋 Quiz généré")
            st.write(quiz_text)
            
            # Bouton de téléchargement
            st.download_button(
                label="📥 Télécharger le Quiz",
                data=quiz_text,
                file_name="quiz_generated.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.success("✅ Quiz généré avec succès!")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération: {str(e)}")