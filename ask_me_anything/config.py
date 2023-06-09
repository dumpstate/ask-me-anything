import os

from dataclasses import dataclass


_config = None


@dataclass
class Config:
    db_url: str
    openai_api_key: str

    @staticmethod
    def load():
        global _config

        if _config is None:
            _config = Config(
                db_url=os.environ.get("AMA__DB", "postgresql://ama:ama_pass@127.0.0.1:5432/ama_db"),
                openai_api_key=os.environ["OPENAI_API_KEY"],
            )

        return _config
