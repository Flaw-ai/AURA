import subprocess

def run_step(script):
    print(f"\nRunning: {script}")
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        raise RuntimeError(f"{script} failed")


def build_dataset():
    run_step(
        "datasets/pipeline/clean_dataset.py"
    )
    run_step(
        "datasets/pipeline/deduplicate.py"
    )
    run_step(
        "datasets/pipeline/quality_filter.py"
    )
    run_step(
        "datasets/pipeline/ranking_pipeline.py"
    )
    run_step(
        "datasets/pipeline/merge_datasets.py"
    )
    print(
        "Dataset build complete."
    )

if __name__ == "__main__":
    build_dataset()