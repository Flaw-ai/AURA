class ConversationFormatter:
    def __init__(self):
        pass

    def format_sample(self, sample):
        conversation = ""

        for msg in sample[
            "messages"
        ]:
            role = msg["role"]
            content = msg["content"]

            conversation += (
                f"<|{role}|>\n"
                f"{content}\n"
            )
        return conversation

    def format_dataset(self, dataset):
        formatted = []
        
        for sample in dataset:
            formatted.append({
                "text":
                self.format_sample(
                    sample
                )
            })

        return formatted