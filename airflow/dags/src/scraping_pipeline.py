import logging
import os
from .data_manager import save_miniO

from .config import load_config

config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "scraping_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


def scrape_documents():
    logging.info("Scraping pipeline started")
    documents = []
    logging.info("Scraping pipeline finished")
    save_miniO(documents, path="", object_name="")


if __name__ == "__main__":
    scrape_documents()
