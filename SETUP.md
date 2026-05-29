# 🚀 Guide d'Installation Rapide - Quiz Generator AI

## ⚡ Installation en 5 minutes

### Étape 1: Ouvrir le terminal PowerShell
```powershell
# Naviguez vers le dossier du projet
cd c:\dhiaprojetAI\QuizGeneratorAI
```

### Étape 2: Créer un environnement virtuel (recommandé)
```powershell
# Créer l'environnement
python -m venv venv

# Activer l'environnement
.\venv\Scripts\Activate

# Vous devriez voir (venv) au début du terminal
```

### Étape 3: Installer les dépendances
```powershell
# Installer tous les paquets requis
pip install -r requirements.txt

# ⏳ Cela peut prendre 2-3 minutes la première fois
```

### Étape 4: Lancer l'application
```powershell
streamlit run app.py
```

✅ L'application s'ouvrira dans votre navigateur à `http://localhost:8501`

---

## 📁 Fichiers créés

| Fichier | Description |
|---------|-------------|
| `app.py` | ✅ Application principale (corrigée et améliorée) |
| `config.py` | Configuration et paramètres |
| `utils.py` | Fonctions utilitaires |
| `styles.css` | Styles CSS personnalisés |
| `requirements.txt` | Dépendances Python |
| `README.md` | Documentation complète |
| `.streamlit/config.toml` | Configuration Streamlit |
| `.gitignore` | Fichiers à ignorer pour Git |
| `app_old_backup.py` | Ancien fichier (sauvegarde) |

---

## ✅ Corrections apportées

### Code original
- ❌ Imports dupliqués et mal placés
- ❌ Modèle "text2text-generation" n'existe pas
- ❌ Variables non définies
- ❌ Bouton téléchargement incomplet
- ❌ Interface peu attrayante

### Code corrigé
- ✅ Structure propre et organisée
- ✅ Modèle GPT2 fonctionnel
- ✅ Gestion d'erreurs complète
- ✅ Interface moderne avec onglets
- ✅ Exports multiples (TXT, JSON)
- ✅ Design responsive
- ✅ Paramètres ajustables

---

## 🎨 Améliorations du design

### Interface moderne
- Gradient de couleurs (bleu → violet)
- Onglets pour mieux organiser
- Barre latérale intuitive
- Icônes emoji pour meilleure UX
- Animations fluides

### Fonctionnalités
- 📊 Statistiques du texte (caractères, mots, paragraphes)
- 🔧 Réglages avancés (créativité, longueur)
- 📥 Export TXT et JSON
- 💡 Guide d'utilisation intégré
- 🎓 Questions fréquentes

---

## 🔧 Dépannage

### Q: L'installation est lente
**R:** Le modèle GPT2 (~500MB) se télécharge la première fois. C'est normal.

### Q: Erreur "No module named 'streamlit'"
**R:** Vérifiez que l'environnement virtuel est activé et les dépendances installées
```powershell
pip install -r requirements.txt
```

### Q: L'application ne démarre pas
**R:** Essayez ceci:
```powershell
# Redémarrer Python
deactivate
.\venv\Scripts\Activate
streamlit run app.py
```

### Q: Le PDF n'extraie pas le texte
**R:** 
- Vérifiez que le PDF n'est pas protégé
- Les PDFs scannés ne fonctionnent pas
- Le PDF doit avoir du texte sélectionnable

---

## 📝 Prochaines étapes

1. ✅ Téléchargez un document PDF
2. ✅ Ajustez les paramètres dans la barre latérale
3. ✅ Cliquez sur "Générer le Quiz"
4. ✅ Téléchargez le résultat

---

## 💻 Systèmes supportés

- ✅ Windows (7, 10, 11)
- ✅ macOS (10.14+)
- ✅ Linux (Ubuntu, Debian, etc.)

---

## 📞 Support

Consultez le README.md pour plus d'informations ou la section "Aide" dans l'application.

---

**Version**: 1.0  
**Mise à jour**: Mai 2026  
**Statut**: ✅ Prêt à l'emploi
