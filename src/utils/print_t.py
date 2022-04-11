from datetime import datetime, timezone, timedelta

TZ_MOSCOW = timezone(timedelta(hours=+3))


def print_t(message):
    print(f'[{datetime.now():%Y-%m-%d %H:%M:%S}]: {message}')
