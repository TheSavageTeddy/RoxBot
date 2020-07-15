from termcolor import colored


def info(text):
    print(f"[{colored('+', 'green')}] {text}")

def warning(text):
    print(f"[{colored('-', 'red')}] {text}")

def process(text):
    print(f"[{colored('*', 'blue')}] {text}")