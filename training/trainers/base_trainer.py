from abc import ABC, abstractmethod
from pathlib import Path
import logging
import json

class BaseTrainer(ABC):
    def __init__(
        self,
        config: dict
    ):
        self.config = config
        self.output_dir = Path(
            config.get(
                "output_dir",
                "./outputs"
            )
        )
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(
            self.__class__.__name__
        )
        logger.setLevel(
            logging.INFO
        )
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] "
                "%(levelname)s - "
                "%(message)s"
            )
            handler.setFormatter(
                formatter
            )
            logger.addHandler(
                handler
            )
        return logger

    def save_metrics(
        self,
        metrics: dict,
        filename: str
    ):
        file_path = (
            self.output_dir /
            filename
        )
        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                metrics,
                f,
                indent=4
            )
    @abstractmethod
    def load_dataset(self):
        pass
    @abstractmethod
    def build_model(self):
        pass
    @abstractmethod
    def train(self):
        pass
    @abstractmethod
    def evaluate(self):
        pass