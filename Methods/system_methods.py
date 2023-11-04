import datetime


def console_log(message, err=None):
    try:
        print(f"[{datetime.datetime.now()}] [INFO    ] {message}")
        if err:
            console_log(err)
    except Exception as e:
        print(e)
