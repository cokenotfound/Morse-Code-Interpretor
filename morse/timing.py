import time
from utils.config import LETTER_GAP

class TemporalAnalyzer:
    def __init__(self):
        self.start_time = None
        self.buffer = ""  # This is where the dots and dashes live
        self.last_signal_end_time = time.time()
        self.is_active = False

    def get_buffer(self):
        """Returns the current sequence of dots and dashes."""
        return self.buffer

    def clear_buffer(self):
        """Resets the sequence after a letter is decoded."""
        self.buffer = ""

    def process(self, signal, mode):
        now = time.time()

        # MODE 2: HAND (Logic based on Shape - Fist/Palm)
        if mode == 2:
            if signal and not self.is_active:
                self.buffer += "." if signal == "DOT" else "-"
                self.is_active = True
                self.last_signal_end_time = now
            elif not signal:
                self.is_active = False
        
        # MODES 1 & 3: LIGHT/EYE (Logic based on Duration)
        else:
            if signal == "ACTIVE":
                if not self.is_active:
                    self.start_time = now
                    self.is_active = True
            else:
                if self.is_active:
                    duration = now - self.start_time
                    self.buffer += "." if duration < 0.4 else "-"
                    self.is_active = False
                    self.last_signal_end_time = now

        # Gap Detection for all modes
        if not self.is_active and (now - self.last_signal_end_time) > LETTER_GAP:
            if self.buffer != "":
                return "DECODE_LETTER"
        return None