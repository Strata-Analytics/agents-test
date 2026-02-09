from typing import AsyncGenerator, Optional
from pipecat.services.stt_service import STTService
from pipecat.frames.frames import (
    Frame, TranscriptionFrame, InterimTranscriptionFrame,
    StartFrame, EndFrame, CancelFrame
)
from pipecat.utils.time import time_now_iso8601
import websockets
import numpy as np

class WhisperLiveKitSTT(STTService):
    def __init__(self, url: str, sample_rate: int = 16000, **kwargs):
        super().__init__(sample_rate=sample_rate, **kwargs)
        self._url = url
        self._websocket = None

    async def start(self, frame: StartFrame):
        await super().start(frame)
        self._websocket = await websockets.connect(self._url, max_size=None)

    async def stop(self, frame: EndFrame):
        await super().stop(frame)
        if self._websocket:
            await self._websocket.close()

    async def cancel(self, frame: CancelFrame):
        await super().cancel(frame)
        if self._websocket:
            await self._websocket.close()

    async def run_stt(self, audio: bytes) -> AsyncGenerator[Frame, None]:
        if self._websocket:
            # Send audio (convert to int16 PCM if needed)
            await self._websocket.send(audio)

            # Receive transcription
            msg = await self._websocket.recv()
            if msg:
                yield TranscriptionFrame(
                    text=msg,
                    user_id="",
                    timestamp=time_now_iso8601()
                )