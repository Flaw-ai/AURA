from pathlib import Path
from typing import List

class NCERTLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def load_txt(self) -> List[dict]:
        documents = []
        for file in self.data_dir.rglob("*.txt"):
            try:
                text = file.read_text(encoding="utf-8")
                documents.append({
                    "source": str(file),
                    "text": text
                })

            except Exception as e:
                print(f"Failed loading {file}: {e}")

        return documents

    def load_pdf_metadata(self):
        files = list(self.data_dir.rglob("*.pdf"))

        return [
            {
                "source": str(f),
                "type": "pdf"
            }
            for f in files
        ]

    def stats(self):
        txt_count = len(
            list(self.data_dir.rglob("*.txt"))
        )
        pdf_count = len(
            list(self.data_dir.rglob("*.pdf"))
        )

        return {
            "txt": txt_count,
            "pdf": pdf_count
        }