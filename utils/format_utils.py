def print_separator(text=""):
    BLUE = "\033[94m"
    RESET = "\033[0m"
    print("\n" + BLUE + "-" * 70 + RESET)  # Ligne bleue
    if text:
        print(BLUE + text.center(70) + RESET)  # Texte centré en bleu
        print(BLUE + "-" * 70 + RESET)