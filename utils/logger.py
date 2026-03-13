import datetime


def log(message):

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    print(f"[{timestamp}] {message}")