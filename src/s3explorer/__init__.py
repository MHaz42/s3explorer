import os
import logging


root_logger = logging.getLogger()
file_handler = logging.FileHandler(f"{os.getcwd()}/log.txt")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
file_handler.setLevel(logging.INFO)
root_logger.addHandler(file_handler)
root_logger.setLevel(logging.INFO)