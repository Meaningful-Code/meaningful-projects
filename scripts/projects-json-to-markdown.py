# Convert an input JSON project list file to a markdown

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
import sys
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


def generate_markdown_project(data: Dict[str, Any]) -> str:
    """Generates a markdown string for a single project.

    Args:
        data (Dict[str, Any]): Dictionary containing project data.

    Returns:
        str: A markdown formatted string for the project.
    """

    def value_or_empty(value):
        return value if value else ""

    return (
        f"- **[{data['owner']}/{data['name']}]({data['url']})**: \n"
        f"  - **Categories**: {', '.join(data['categories'])}\n"
        f"  - **Description**: {value_or_empty(data.get('description'))}\n"
        f"  - **Website URL**: {value_or_empty(data.get('websiteUrl'))}\n"
    )


def generate_markdown_list(data_list: List[Dict[str, Any]]) -> str:
    """Generates a markdown formatted list from the data.

    Args:
        data_list (List[Dict[str, Any]]): A list of dictionaries containing project data.

    Returns:
        str: A markdown formatted string representing the list of projects.
    """
    # Sort by project owner/name
    sorted_data_list = sorted(data_list, key=lambda x: x["owner"] + x["name"])

    # Convert each project to a Markdown list item
    markdown_list = ["## Impactful Project List\n"] + [
        generate_markdown_project(data) for data in sorted_data_list
    ]
    return "\n".join(markdown_list)


def main():
    if len(sys.argv) != 2:
        sys.exit(
            "Usage: python projects-json-to-markdown.py <path_to_projects_json_file>"
        )

    try:
        file_path = sys.argv[1]
        data_list = read_json_file(file_path)
        markdown_output = generate_markdown_list(data_list)
        print(markdown_output)
    except Exception as e:
        sys.exit(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
