from trainers.evaluator import Evaluator

def main():
    evaluator = Evaluator()
    predictions = ["Photosynthesis converts sunlight into chemical energy."]
    references = ["Photosynthesis converts sunlight into chemical energy."]
    result = evaluator.exact_match(predictions, references)
    print(f"Exact Match: {result:.4f}")


if __name__ == "__main__":
    main()