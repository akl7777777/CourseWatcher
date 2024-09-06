import json
import hashlib

def get_response_hash(response_text):
    return hashlib.md5(response_text.encode()).hexdigest()

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)
