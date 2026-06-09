from collect_data import collect_data
from build_dataset import build_dataset
from train_tokenizer import train_tokenizer
from train_flaw import train_flaw
from evaluate import evaluate_model
from export import export_model

def main():
    print("FLAW AUTOMATION PIPELINE")

    collect_data()
    build_dataset()
    train_tokenizer()
    train_flaw()
    evaluate_model()
    export_model()

    print("PIPELINE COMPLETE")


if __name__ == "__main__":
    main()