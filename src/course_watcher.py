import json
import os
import time
import logging

import requests

from src.utils import get_response_hash, load_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_for_updates(config):
    url = config['url']
    headers = config['headers']
    data = config['data']
    interval = config['check_interval']

    previous_hash = None

    while True:
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()

            current_hash = get_response_hash(response.text)

            if previous_hash is None:
                logging.info("Initial data fetched. Monitoring for changes...")
                previous_hash = current_hash
            elif current_hash != previous_hash:
                logging.info("Change detected! New courses might be available.")
                logging.info("Response: %s", json.dumps(response.json(), indent=2))
                previous_hash = current_hash
            else:
                logging.info("No changes detected.")

        except requests.RequestException as e:
            logging.error("Error fetching data: %s", e)

        time.sleep(interval)


def main():
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(script_dir, 'config', 'config.json')

    try:
        config = load_config(config_path)
    except FileNotFoundError:
        logging.error("Config file not found: %s", config_path)
        return
    except json.JSONDecodeError:
        logging.error("Invalid JSON in config file: %s", config_path)
        return

    check_for_updates(config)


if __name__ == "__main__":
    main()