import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Parser:
    api_key: str


@dataclass
class Config:
    tg_bot: TgBot
    parser: Parser


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    parser = config["parser"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"]
        ),
        parser=Parser(
            api_key=parser["api_key"],
        )
    )
