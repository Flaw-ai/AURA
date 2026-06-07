import json
from training.evaluate import (ModelEvaluator)

def main():
    evaluator = ModelEvaluator(model_path="outputs/final")
    results = evaluator.run()

    with open(
        "evaluation_results.json",
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=4
        )
    print(results)


if __name__ == "__main__":
    main()