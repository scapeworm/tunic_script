import json

from pyscript import document  # type: ignore


def setup(words_file):
    with open(words_file) as f:
        words = json.load(f)
    return words


def run(words):
    print(f"words: {len(words):,}")


def main():
    loading = document.getElementById("loading")
    try:
        words = setup(words_file="words.json")
    finally:
        loading.close()

    run(words)


if __name__ == "__main__":
    main()
