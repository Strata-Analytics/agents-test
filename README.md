# Pipecat AI Agent Project

Este proyecto es un agente de IA conversacional construido con Pipecat AI, que incluye capacidades de voz utilizando Piper TTS y servicios de LLM como Groq.

## Requisitos Previos

- Python 3.8 o superior
- uv (instalador de paquetes para Python)
- Una cuenta en Groq para obtener la API key

## Instalación

1. Clona o navega al directorio del proyecto.

2. Instala las dependencias usando uv:

   ```
   uv pip install -r requirements.txt
   ```

3. Descarga los modelos de voz necesarios (.onnx y .onnx.json) en la carpeta `./voice`. Por ejemplo, para el modelo `es_MX-claude-high`, descarga `es_MX-claude-high.onnx` y `es_MX-claude-high.onnx.json` desde [HF](https://huggingface.co/rhasspy/piper-voices/tree/main) o fuentes compatibles

4. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

   ```
   GROQ_API_KEY=tu_clave_de_api_de_groq

   CURRENT_VOICE=es_MX-claude-high.onnx
   CURRENT_VOICE_CONFIG=es_MX-claude-high
   PIPER_PORT=5002
   ```

   - Reemplaza `tu_clave_de_api_de_groq` con tu clave real de Groq.
   - Las variables de voz se configuran con lo realizado en el paso 3. El puerto puede permanecer como está a menos que se desee cambiarlo.

## Ejecución

1. **Inicia el servidor de Piper TTS** (necesario para la síntesis de voz):

   ```
   uv run python run_piper.py
   ```

   Esto levantará el servidor en el puerto especificado en `PIPER_PORT`.

2. **Ejecuta el agente de IA** en una terminal separada:
   ```
   uv run python agent.py
   ```

El agente estará listo para recibir conexiones y procesar audio/texto en tiempo real.

## Notas

- Asegúrate de que el servidor de Piper esté corriendo antes de iniciar el agente.
- Los modelos de voz deben descargarse en la carpeta `voice/`.
- Para más opciones de transporte, consulta la documentación de Pipecat AI.
