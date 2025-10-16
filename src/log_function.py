from datetime import datetime


def log(log_file: str, message: str) -> None:

    log_information = f"------------------\n{datetime.now()}: {message}\n"

    with open(log_file, "a", encoding="UTF-8") as file:
        file.write(log_information)
