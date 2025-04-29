#!/bin/bash

echo "### Initialisation de l'environnement virtuel..."
python3 -m venv PythonVirtualEnv

echo "### Activation de l'environnement..."
source PythonVirtualEnv/bin/activate

echo "### Installation des dépendances..."
pip install -r requirements.txt

echo "### Installation terminée, lancer Flask..."
