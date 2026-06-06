from datetime import (datetime)

class ProgressionTracker:
    def __init__(self):
        self.history = []

    def log_stage(self, stage_name, samples, loss):
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "stage": stage_name,
            "samples": samples,
            "loss": loss
        })

    def latest(self):
        if not self.history:
            return None
        return self.history[-1]

    def all_logs(self):
        return self.history