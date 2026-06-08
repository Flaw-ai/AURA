class BatchInference:
    def __init__(self, generator):
        self.generator = generator

    def run_batch(self, prompts, mode="chat", config=None):
        outputs = []
        for prompt in prompts:
            result = (
                self.generator.generate(
                    text=prompt,
                    mode=mode,
                    config=config
                )
            )
            outputs.append(result)

        return outputs

    def benchmark(self, prompts):
        results = self.run_batch(prompts)
        return {
            "requests": len(prompts),
            "responses": len(results)
        }