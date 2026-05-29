@echo off
REM Script de lancement rapide pour Quiz Generator AI

echo.
echo ================================
echo   Quiz Generator AI - Launcher
echo ================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Créer l'environnement virtuel s'il n'existe pas
if not exist venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Vérifier si les dépendances sont installées
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation des dépendances...
    pip install -r requirements.txt
)

REM Lancer l'application
echo.
echo ================================
echo Lancement de l'application...
echo ================================
echo.
echo L'app s'ouvrira à: http://localhost:8501
echo Appuyez sur Ctrl+C pour arrêter
echo.

streamlit run app.py

pause
