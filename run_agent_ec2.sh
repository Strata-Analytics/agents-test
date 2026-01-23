#!/bin/bash
# Script para ejecutar el agente y guardar todos los logs en un archivo

# Crear directorio de logs si no existe
mkdir -p logs

uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt

# Ejecutar el agente y redirigir stderr a un archivo mientras se muestra en consola
python src/agent.py --host 0.0.0.0 --port 7860
