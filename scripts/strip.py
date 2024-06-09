# Strips project data from a JSON file to exclude attributes that are subject to frequent changes.

from typing import List, Dict, Any

attributes_to_keep = set(
    ["categories", "description", "name", "owner", "url", "websiteUrl"]
)


def strip_projects(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Strips project project data subject to frequent changes

    Args:
        data_list (List[Dict[str, Any]]): A list of dictionaries containing project data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing stripped project data.
    """
    striped_projects = []
    for project in data_list:
        striped_projects.append(
            {k: v for k, v in project.items() if k in attributes_to_keep}
        )
    return striped_projects
