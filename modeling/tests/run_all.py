from test_forward import test_forward
from test_generation import test_generation
from test_attention import test_attention

def main():
    print("\nRunning FLAW tests...\n")
    test_forward()
    test_generation()
    test_attention()
    print("\nAll tests passed.\n")

if __name__ == "__main__":
    main()