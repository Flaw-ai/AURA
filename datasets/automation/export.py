import subprocess

def export_model():
    subprocess.run(
        [
            "python",
            "quantization/quantize.py"
        ]
    )
    subprocess.run(
        [
            "python",
            "quantization/gguf_export.py"
        ]
    )

    print("Export complete.")

if __name__ == "__main__":
    export_model()