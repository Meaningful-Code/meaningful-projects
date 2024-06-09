# Data format:
# {
#     "url": "https://github.com/example/example-repo",
#     "categories": ["accessibility", "education"],
#     "pitch": "example pitch",
#     "tags": ["example"],
#     "websiteUrl": "https://example.com",
#     "owner": "exampleowner",
#     "name": "example-repo",
#     "description": "Example description",
#     "stars": 1000,
#     "languages": ["Python", "HTML"],
#     "lastCommitTimestamp": 1704646040,
#     "archived": true
# }

import json
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Reads and returns JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing project data.

    Raises:
        FileNotFoundError: If the file is not found.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Error: The file '{file_path}' does not contain valid JSON."
        ) from e
