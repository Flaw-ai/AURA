import subprocess

def train_flaw():
    result = subprocess.run(
        [
            "python",
            "training/train.py"
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Training failed."
        )

    print("Training complete.")

if __name__ == "__main__":
    train_flaw()