from trainers.evaluator import (
    Evaluator
)

def main():
    evaluator = Evaluator()
    result = (
        evaluator.exact_match(
            ["hello"],
            ["hello"]
        )
    )
    print(result)

if __name__ == "__main__":
    main()