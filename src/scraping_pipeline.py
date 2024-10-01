import logging
import os

from .config import load_config

config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "scraping_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


def scraping_pipeline():
    logging.info("Scraping pipeline started")
    pass


if __name__ == "__main__":
    scraping_pipeline()
