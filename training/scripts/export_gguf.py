import subprocess

class GGUFExporter:
    def __init__(self, model_path, output_path):
        self.model_path = model_path
        self.output_path = output_path

    def export(self):
        command = [
            "python",
            "llama.cpp/convert_hf_to_gguf.py",
            self.model_path,
            "--outfile",
            self.output_path,
            "--outtype",
            "q8_0"
        ]

        subprocess.run(command, check=True)
        print(f"Exported -> {self.output_path}")


if __name__ == "__main__":
    exporter = GGUFExporter(
        "outputs/final",
        "outputs/flaw.gguf"
    )
    exporter.export()