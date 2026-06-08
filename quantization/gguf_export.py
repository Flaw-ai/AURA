import subprocess
from pathlib import Path

class GGUFExporter:
    def __init__(self, llama_cpp_path):
        self.llama_cpp_path = (Path(llama_cpp_path))

    def export(self, model_path, output_path):
        converter = (self.llama_cpp_path/"convert_hf_to_gguf.py")

        command = [
            "python",
            str(converter),
            model_path,
            "--outfile",
            output_path
        ]

        subprocess.run(command, check=True)

        print("GGUF export complete.")

    def export_q4(self, gguf_path):
        quantize_bin = (self.llama_cpp_path / "quantize")

        output_file = (
            gguf_path
            .replace(
                ".gguf",
                "-Q4.gguf"
            )
        )

        command = [
            str(quantize_bin),
            gguf_path,
            output_file,
            "Q4_K_M"
        ]

        subprocess.run(command, check=True)

        return output_file


if __name__ == "__main__":
    print("GGUF exporter ready.")
