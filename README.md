# Pipecat AI Voice Agent

Agente conversacional de voz construido con [Pipecat AI](https://github.com/pipecat-ai/pipecat). Pipeline configurable de STT, LLM y TTS con soporte para multiples proveedores.

## Arquitectura

```
Browser/Phone
     |
  Transport (WebRTC / Daily / Twilio)
     |
  STT  -->  LLM  -->  TTS
     |                   |
  WhisperLiveKit    Chatterbox Server
  Deepgram          Polly / Piper
```

## Estructura del Proyecto

```
.
├── src/
│   ├── agent.py                  # Pipeline principal: Transport -> STT -> LLM -> TTS
│   └── helpers/
│       ├── config.py             # Transports, VAD, system prompt
│       ├── services.py           # Factories de STT/TTS/LLM por env vars
│       ├── tools.py              # Tool definitions para el LLM
│       ├── whisper_livekit_custom_integration.py   # Plugin STT: WhisperLiveKit streaming
│       └── chatterbox_custom_integration.py        # Plugin TTS: Chatterbox Server
├── scripts/
│   ├── piper/
│   │   ├── Dockerfile            # Imagen Docker para Piper TTS
│   │   └── run_piper.py          # Launcher del servidor Piper
│   └── whisperlivekit_websocket.py  # Script de test para WebSocket STT
├── Dockerfile                    # Imagen Docker del agente
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Credenciales AWS con acceso a Bedrock

## Instalacion

```bash
uv pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus valores
```

## Variables de Entorno

| Variable | Default | Descripcion |
|---|---|---|
| `STT_SERVICE_PROVIDER` | `WHISPER-STREAM` | `WHISPER-STREAM` \| `DEEPGRAM` |
| `TTS_SERVICE_PROVIDER` | `CHATTERBOX_SERVER` | `CHATTERBOX_SERVER` \| `CHATTERBOX_SERVER_OPENAI` \| `PIPER` \| `POLLY` |
| `EC2_HOST` | — | Host por defecto para todos los servidores remotos |
| `EC2_HOST_WHISPER_STREAM` | `EC2_HOST` | Override para el servidor WhisperLiveKit |
| `EC2_HOST_CHATTERBOX` | `EC2_HOST` | Override para el servidor Chatterbox |
| `EC2_HOST_PIPER` | `EC2_HOST` | Override para el servidor Piper |
| `EC2_WHISPER_PORT` | `8000` | Puerto del servidor WhisperLiveKit |
| `EC2_CHATTERBOX_PORT` | `8004` | Puerto del servidor Chatterbox |
| `EC2_PIPER_PORT` | `5002` | Puerto del servidor Piper |
| `AWS_ACCESS_KEY_ID` | — | Credenciales AWS (Bedrock / Polly) |
| `AWS_SECRET_ACCESS_KEY` | — | |
| `AWS_SESSION_TOKEN` | — | |
| `AWS_DEFAULT_REGION` | `us-east-1` | |
| `DEEPGRAM_API_KEY` | — | Solo si `STT_SERVICE_PROVIDER=DEEPGRAM` |

## Ejecucion

```bash
uv run src/agent.py
```

El agente expone un servidor WebRTC en el puerto 7860.

### Docker

```bash
docker compose up --build
```

## Proveedores de STT

### WhisperLiveKit (Streaming) — Default

STT en streaming via WebSocket. Transcribe audio mientras el usuario habla, sin esperar a que termine.

- Plugin custom: `src/helpers/whisper_livekit_custom_integration.py`
- Protocolo: WebSocket en `ws://{host}:{port}/asr`
- Env: `STT_SERVICE_PROVIDER=WHISPER-STREAM`

#### Despliegue del servidor WhisperLiveKit

<!-- TODO: documentar despliegue del servidor WhisperLiveKit -->

### Deepgram

STT cloud via API de Deepgram (modelo nova-3, spanish).

- Env: `STT_SERVICE_PROVIDER=DEEPGRAM`, `DEEPGRAM_API_KEY=...`

## Proveedores de TTS

### Chatterbox Server — Default

TTS via servidor Chatterbox con soporte para voces predefinidas y clonadas. Detecta automaticamente el modo de voz consultando `/get_predefined_voices`.

- Plugin custom: `src/helpers/chatterbox_custom_integration.py`
- Endpoints soportados: `/tts` (default) y `/v1/audio/speech` (OpenAI-compatible)
- Env: `TTS_SERVICE_PROVIDER=CHATTERBOX_SERVER` o `CHATTERBOX_SERVER_OPENAI`

#### Despliegue del servidor Chatterbox

<!-- TODO: documentar despliegue del servidor Chatterbox -->

### AWS Polly

TTS cloud via AWS Polly (voz Lupe, motor generative, spanish).

- Env: `TTS_SERVICE_PROVIDER=POLLY`

### Piper

TTS local/remoto open-source. Requiere un servidor Piper separado.

- Env: `TTS_SERVICE_PROVIDER=PIPER`
- Dockerfile separado en `scripts/piper/`

## LLM

### AWS Bedrock

Claude Haiku 4.5 via AWS Bedrock. Configurado con tools para busqueda de productos, carrito y ordenes.

## Metricas

El agente usa `MetricsLogObserver` de Pipecat para loggear automaticamente:
- **TTFB**: Time to first byte de cada servicio
- **Processing time**: Tiempo de procesamiento de STT, LLM y TTS
- **LLM token usage**: Prompt tokens, completion tokens, total
- **TTS usage**: Caracteres procesados

Las metricas se imprimen en stdout con el pipeline activo.
