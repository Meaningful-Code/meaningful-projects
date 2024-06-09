import re
from typing import Any, Dict, List, Optional

CATEGORIES = (
    "environment",
    "health",
    "society",
    "education",
    "humanitarian",
    "accessibility",
)

PROJECTS_TITLE = "## Impactful Project List"


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
            if not all(map(lambda cat: cat in CATEGORIES, categories)):
                raise ValueError(
                    f'Invalid categories "{categories}" for project "{owner}/{name}"'
                )
        else:
            project[attribute] = value if value else None

    return project


def find_project_title(markdown_text: str) -> Optional[int]:
    """Finds the index of the project title in the markdown text."""
    project_start = markdown_text.find(PROJECTS_TITLE)
    return project_start if project_start != -1 else None


def get_markdown_project_header(markdown_text: str) -> str:
    """Returns the text present before the project list in the markdown text."""
    project_start = find_project_title(markdown_text)
    if project_start is None:
        raise ValueError(f"Failed to find anchor text '{PROJECTS_TITLE}'")

    return markdown_text[:project_start]


def parse_markdown_projects(markdown_text: str) -> List[Dict[str, Optional[str]]]:
    """Parses Markdown text to a list of dictionaries representing project data."""
    projects: List[Dict[str, Optional[str]]] = []
    project_start = find_project_title(markdown_text)
    if project_start is None:
        raise ValueError(f"Failed to find anchor text '{PROJECTS_TITLE}'")

    markdown_text = markdown_text[project_start:]
    project_blocks = markdown_text.split("\n- **")

    for block in project_blocks[1:]:
        project = parse_single_project(block)
        projects.append(project)

    return projects


def generate_markdown_project(data: Dict[str, Any]) -> str:
    """Generates a markdown string for a single project.

    Args:
        data (Dict[str, Any]): Dictionary containing project data.

    Returns:
        str: A markdown formatted string for the project.
    """

    def value_or_empty(value):
        return value if value else ""

    website = value_or_empty(data.get("websiteUrl"))
    return (
        f"- **[{data['owner']}/{data['name']}]({data['url']})**:\n\n"
        f"  - **Categories**: {', '.join([cat.strip() for cat in data['categories']])}\n"
        f"  - **Description**: {value_or_empty(data.get('description')).strip()}\n"
        f"  - **Website URL**:{' ' + website if website else ''}\n"
    )


def generate_markdown_list(project_list: List[Dict[str, Any]]) -> str:
    """Generates a markdown formatted list from the data.

    Args:
        project_list (List[Dict[str, Any]]): A list of dictionaries containing project data.

    Returns:
        str: A markdown formatted string representing the list of projects.
    """
    # Convert each project to a Markdown list item
    markdown_list = ["## Impactful Project List\n"] + [
        generate_markdown_project(data) for data in project_list
    ]
    return "\n".join(markdown_list)
