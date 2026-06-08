import time

class StreamingGenerator:
    def __init__(self, generator):
        self.generator = generator

    def stream(self, text, mode="chat", config=None):
        output = self.generator.generate(
            text=text,
            mode=mode,
            config=config
        )

        words = output.split()
        for word in words:
            yield word + " "
            time.sleep(0.01)

    def stream_to_console(self, text):
        for token in self.stream(text):
            print(
                token,
                end="",
                flush=True
            )

        print()