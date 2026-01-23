"""Procesadores customizados del pipeline"""
import time
from pipecat.frames.frames import TextFrame, Frame
from pipecat.processors.frame_processor import FrameProcessor


class STTLogger(FrameProcessor):
    """Logger que guarda las transcripciones de STT en un archivo"""
    
    def __init__(self, filename="logs/stt_log.txt"):
        super().__init__()
        self.filename = filename

    async def process_frame(self, frame, direction):
        await super().process_frame(frame, direction)
        if isinstance(frame, TextFrame):
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(frame.text + "\n")


class TimingStats:
    """Clase compartida para almacenar estadísticas de timing"""
    def __init__(self):
        self.stt_times = []
        self.llm_times = []
        self.tts_times = []
        self.start_time = None
        
    def print_stats(self):
        """Imprime estadísticas de timing"""
        if self.stt_times:
            avg_stt = sum(self.stt_times) / len(self.stt_times)
            print(f"\n📊 Estadísticas de Timing:")
            print(f"  STT: {avg_stt:.3f}s (promedio de {len(self.stt_times)} mediciones)")
            
        if self.llm_times:
            avg_llm = sum(self.llm_times) / len(self.llm_times)
            print(f"  LLM: {avg_llm:.3f}s (promedio de {len(self.llm_times)} mediciones)")
            
        if self.tts_times:
            avg_tts = sum(self.tts_times) / len(self.tts_times)
            print(f"  TTS: {avg_tts:.3f}s (promedio de {len(self.tts_times)} mediciones)")


class TimingProcessor(FrameProcessor):
    """Procesador que mide el tiempo de cada etapa del pipeline"""
    
    def __init__(self, stage: str, stats: TimingStats):
        super().__init__()
        self.stage = stage
        self.stats = stats
        self.stage_start = None
        
    async def process_frame(self, frame: Frame, direction):
        await super().process_frame(frame, direction)
        
        # Medir tiempo solo para TextFrames
        if isinstance(frame, TextFrame):
            if not self.stage_start:
                self.stage_start = time.time()
            else:
                elapsed = time.time() - self.stage_start
                
                if self.stage == "stt":
                    self.stats.stt_times.append(elapsed)
                    print(f"⏱️  STT completado: {elapsed:.3f}s")
                elif self.stage == "llm":
                    self.stats.llm_times.append(elapsed)
                    print(f"⏱️  LLM completado: {elapsed:.3f}s")
                elif self.stage == "tts":
                    self.stats.tts_times.append(elapsed)
                    print(f"⏱️  TTS completado: {elapsed:.3f}s")
                    
                self.stage_start = None
        
        # CRÍTICO: Pasar el frame al siguiente procesador
        await self.push_frame(frame, direction)
