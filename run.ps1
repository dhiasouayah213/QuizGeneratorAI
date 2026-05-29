# Script PowerShell pour lancer Quiz Generator AI

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Quiz Generator AI - Launcher" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python trouvé: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERREUR: Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Créer l'environnement virtuel s'il n'existe pas
if (-not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Environnement virtuel créé" -ForegroundColor Green
}

# Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Vérifier si les dépendances sont installées
$streamlitInstalled = pip show streamlit 2>$null
if (-not $streamlitInstalled) {
    Write-Host ""
    Write-Host "Installation des dépendances..." -ForegroundColor Yellow
    Write-Host "(Cela peut prendre 2-3 minutes)" -ForegroundColor Gray
    pip install -r requirements.txt
    Write-Host "✓ Dépendances installées" -ForegroundColor Green
} else {
    Write-Host "✓ Dépendances déjà installées" -ForegroundColor Green
}

# Lancer l'application
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Lancement de l'application..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "L'app s'ouvrira à: http://localhost:8501" -ForegroundColor Green
Write-Host "Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

Read-Host "Appuyez sur Entrée pour quitter"
