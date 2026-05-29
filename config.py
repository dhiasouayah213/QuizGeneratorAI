# Configuration pour Quiz Generator AI

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Quiz Generator AI",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuration du modèle
MODEL_CONFIG = {
    "task": "text-generation",
    "model_name": "gpt2",
    "default_max_length": 512,
    "default_num_questions": 5,
    "default_temperature": 0.7
}

# Paramètres d'extraction PDF
PDF_CONFIG = {
    "max_chars": 1500,  # Caractères maximum à utiliser
    "min_chars": 100,   # Caractères minimum requis
    "max_pages": 50     # Nombre maximum de pages
}

# Couleurs et thème
THEME = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "success_color": "#28a745",
    "error_color": "#dc3545",
    "warning_color": "#ffc107",
    "info_color": "#17a2b8"
}

# Messages
MESSAGES = {
    "fr": {
        "welcome": "Bienvenue dans le générateur automatique de quiz",
        "upload_pdf": "Téléchargez un fichier PDF",
        "no_file": "Aucun fichier PDF sélectionné",
        "loading": "Chargement du modèle d'IA...",
        "generating": "Génération du quiz en cours...",
        "success": "Quiz généré avec succès!",
        "error": "Une erreur s'est produite"
    }
}
