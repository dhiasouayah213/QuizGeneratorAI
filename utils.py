"""
Fonctions utilitaires pour Quiz Generator AI
"""

import streamlit as st
from datetime import datetime
import json
from typing import List, Dict, Tuple

def format_file_size(bytes_size: int) -> str:
    """
    Formate la taille du fichier en format lisible
    
    Args:
        bytes_size: Taille en bytes
        
    Returns:
        Taille formatée (KB, MB, GB)
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def count_words(text: str) -> int:
    """Compte le nombre de mots dans un texte"""
    return len(text.split())


def count_paragraphs(text: str) -> int:
    """Compte le nombre de paragraphes"""
    return len([p for p in text.split("\n\n") if p.strip()])


def extract_text_preview(text: str, max_length: int = 800) -> str:
    """
    Extrait un aperçu du texte
    
    Args:
        text: Texte complet
        max_length: Longueur maximale de l'aperçu
        
    Returns:
        Aperçu du texte
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def create_quiz_json(quiz_text: str, num_questions: int, filename: str = None) -> Dict:
    """
    Crée une structure JSON pour le quiz
    
    Args:
        quiz_text: Texte du quiz généré
        num_questions: Nombre de questions
        filename: Nom du fichier source
        
    Returns:
        Dictionnaire JSON du quiz
    """
    return {
        "metadata": {
            "title": "Quiz généré automatiquement",
            "date_created": datetime.now().isoformat(),
            "version": "1.0",
            "source_file": filename
        },
        "quiz": {
            "num_questions": num_questions,
            "content": quiz_text,
            "language": "fr"
        }
    }


def validate_pdf(file) -> Tuple[bool, str]:
    """
    Valide un fichier PDF
    
    Args:
        file: Objet fichier
        
    Returns:
        Tuple (est_valide, message)
    """
    if file is None:
        return False, "Aucun fichier sélectionné"
    
    if file.type != "application/pdf":
        return False, "Le fichier n'est pas un PDF"
    
    # Vérifier la taille (max 50 MB)
    if file.size > 50 * 1024 * 1024:
        return False, "Le fichier est trop volumineux (max 50 MB)"
    
    return True, "PDF valide"


def create_html_quiz(quiz_text: str, title: str = "Quiz") -> str:
    """
    Crée un fichier HTML pour le quiz
    
    Args:
        quiz_text: Texte du quiz
        title: Titre du quiz
        
    Returns:
        Contenu HTML
    """
    html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            }}
            h1 {{
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
            }}
            .meta {{
                text-align: center;
                color: #999;
                font-size: 0.9em;
                margin-bottom: 30px;
                border-bottom: 1px solid #e0e0e0;
                padding-bottom: 20px;
            }}
            .question {{
                margin: 20px 0;
                padding: 15px;
                background: #f9f9f9;
                border-left: 4px solid #667eea;
                border-radius: 5px;
            }}
            .question h3 {{
                color: #667eea;
                margin-top: 0;
            }}
            .option {{
                margin: 10px 0;
                padding: 10px;
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 3px;
            }}
            .answer {{
                color: #28a745;
                font-weight: bold;
                margin-top: 10px;
            }}
            footer {{
                text-align: center;
                color: #999;
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 {title}</h1>
            <div class="meta">
                <p>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
            </div>
            <div class="content">
                {quiz_text.replace(chr(10), '<br>')}
            </div>
            <footer>
                <p>Créé avec Quiz Generator AI</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return html


def get_model_info() -> Dict:
    """Retourne les informations sur le modèle utilisé"""
    return {
        "name": "GPT-2",
        "task": "text-generation",
        "language": ["en", "fr"],
        "parameters": "124M",
        "size": "~500 MB",
        "license": "MIT"
    }


def create_progress_text(current: int, total: int) -> str:
    """Crée un texte de progression"""
    percentage = (current / total) * 100
    bar_length = 20
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    return f"[{bar}] {percentage:.1f}% ({current}/{total})"


def log_generation(quiz_text: str, num_questions: int, processing_time: float = None):
    """
    Enregistre les informations de génération
    
    Args:
        quiz_text: Texte du quiz
        num_questions: Nombre de questions
        processing_time: Temps de traitement en secondes
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "num_questions": num_questions,
        "text_length": len(quiz_text),
        "processing_time": processing_time
    }
    
    # Pourrait être sauvegardé dans un fichier ou une base de données
    return log_entry
