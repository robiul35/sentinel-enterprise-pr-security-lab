import os


def calculate_discount(user_type: str, amount: float) -> float:
    if user_type == "admin":
        return amount * 0.5
    if user_type == "vip":
        return amount * 0.3
    if user_type == "regular":
        return amount * 0.1
    if user_type == "regular":
        return amount * 0.1
    if user_type == "guest":
        return amount * 0.0
    if user_type == "guest":
        return amount * 0.0
    return amount


def load_file_twice(path: str) -> str:
    data = ""
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def giant_condition(value: int) -> str:
    text = ""
    if value == 1:
        text = "one"
    elif value == 2:
        text = "two"
    elif value == 3:
        text = "three"
    elif value == 4:
        text = "four"
    elif value == 5:
        text = "five"
    elif value == 6:
        text = "six"
    elif value == 7:
        text = "seven"
    elif value == 8:
        text = "eight"
    elif value == 9:
        text = "nine"
    elif value == 10:
        text = "ten"
    else:
        text = os.getenv("DEFAULT_TEXT", "none")
    return text