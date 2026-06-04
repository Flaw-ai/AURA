from pathlib import Path

class CheckpointManager:
    def __init__(
        self,
        checkpoint_dir
    ):
        self.checkpoint_dir = Path(
            checkpoint_dir
        )
        self.checkpoint_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def latest_checkpoint(
        self
    ):
        checkpoints = list(
            self.checkpoint_dir.glob(
                "checkpoint-*"
            )
        )

        if not checkpoints:
            return None
        checkpoints.sort()
        
        return str(
            checkpoints[-1]
        )