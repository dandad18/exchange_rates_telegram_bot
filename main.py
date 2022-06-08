from tbot import telegram_bot
from config import configuration

def main() -> None:
    telegram_bot(TOKEN=configuration['TOKEN'])


if __name__ == '__main__':
    main()
