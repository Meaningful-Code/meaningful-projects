# Convert an input JSON project list file to a markdown

import json
import re
import sys
from typing import List, Dict, Optional

supported_categories = (
    "environment",
    "health",
    "society",
    "education",
    "humanitarian",
    "accessibility",
)


def read_markdown_file(file_path: str) -> str:
    """Reads and returns Markdown text from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e


def parse_single_project(block: str) -> Dict[str, Optional[str]]:
    """Parses a single project block from the markdown text."""
    project: Dict[str, Optional[str]] = {}
    lines = block.split("\n  - **")
    first_line = lines[0].split("**: \n")[0]

    try:
        owner, name, url = re.match(r"\[(.*)/(.*)\]\((.*)\)", first_line).groups()
        project["owner"] = owner
        project["name"] = name
        project["url"] = url.strip()
    except AttributeError:
        raise ValueError(
            "Error parsing the project's first line. Format might be incorrect."
        )

    attribute_map: Dict[str, Optional[str]] = {
        "categories": None,
        "description": None,
        "website": "websiteUrl",
    }

    for line in lines[1:]:
        attribute, value = line.split(":", 1)
        attribute = attribute.replace("*", "").strip().split(" ", 1)[0].lower()
        if attribute not in attribute_map:
            raise ValueError(
                f'Invalid attribute "{attribute}" for project "{owner}/{name}"'
            )

        attribute = attribute_map[attribute] if attribute_map[attribute] else attribute

        value = value.strip()
        if attribute == "categories":
            categories = [cat.strip() for cat in value.split(",")]
            if not all(map(lambda cat: cat in supported_categories, categories)):
                raise ValueError(
                    f'Invalid categories "{categories}" for project "{owner}/{name}"'
                )
        else:
            project[attribute] = value if value else None

    return project


def parse_markdown_to_json(markdown_text: str) -> List[Dict[str, Optional[str]]]:
    """Parses Markdown text to a list of dictionaries representing project data."""
    projects: List[Dict[str, Optional[str]]] = []
    anchor_text = "# Impactful Project List"
    project_start = markdown_text.find(anchor_text)
    if project_start == -1:
        raise ValueError(f"Failed to find anchor text '{anchor_text}'")

    markdown_text = markdown_text[project_start:]
    project_blocks = markdown_text.split("\n- **")

    for block in project_blocks[1:]:
        project = parse_single_project(block)
        projects.append(project)

    return projects


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python projects-markdown-to-json.py <path_to_markdown_file>")

    try:
        file_path = sys.argv[1]
        markdown_text = read_markdown_file(file_path)
        projects_json = parse_markdown_to_json(markdown_text)
        print(json.dumps(projects_json, indent=4))
    except Exception as e:
        sys.exit(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
