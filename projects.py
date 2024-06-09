# Convert a list of projects to and from JSON and markdown formats.

import json, sys, os, hashlib
from typing import Any, Dict
from argparse import ArgumentParser

sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from strip import strip_projects
from json_projects import read_json_file
from markdown_projects import (
    read_markdown_file,
    parse_markdown_projects,
    generate_markdown_list,
    get_markdown_project_header,
)


def hashable_project(project: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a project to a hashable stable format."""
    res = []
    for k, v in sorted(project.items()):
        if k == "categories":
            res.append((k, tuple(sorted(v))))
        else:
            res.append((k, v))
    return tuple(res)


def build_arguments_parser() -> ArgumentParser:
    """Returns the argument parser for the CLI."""
    parser = ArgumentParser(
        prog="projects", description="Convert a project to/from JSON and Markdown"
    )

    parser.add_argument("filename")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to-json", action="store_true")
    group.add_argument("--to-md", action="store_true")
    group.add_argument("--to-hash", action="store_true")
    group.add_argument("--to-readme", action="store_true")

    parser.add_argument(
        "--ref-readme",
        required=False,
        help="Reference README.md file required to generate README.md.",
    )
    return parser


def main():
    parser = build_arguments_parser()
    args = parser.parse_args()

    if args.to_readme and not args.ref_readme:
        parser.error("--to-readme requires passing a reference with '--ref-readme'.")

    filename = args.filename

    # Ingest the project data
    if filename.endswith(".json"):
        projects = read_json_file(filename)
    elif filename.endswith(".md"):
        projects = parse_markdown_projects(read_markdown_file(filename))
    else:
        parser.error("Unexpected file format. Please provide a JSON or Markdown file.")

    projects = strip_projects(projects)
    projects = sorted(projects, key=lambda x: x["owner"] + x["name"])

    if args.to_json:
        print(json.dumps(projects, indent=4))
    elif args.to_md:
        print(generate_markdown_list(projects))
    elif args.to_hash:
        data = tuple(hashable_project(p) for p in projects)
        data = str(data).encode()
        digest = hashlib.sha1(data, usedforsecurity=False).hexdigest()
        print(digest)
    elif args.to_readme:
        generate_markdown_list(projects)
        reference_readme = read_markdown_file(args.ref_readme)
        print(get_markdown_project_header(reference_readme), end="")
        print(generate_markdown_list(projects), end="")
    else:
        raise RuntimeError("Unexpected target format.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit(f"An error occurred: {e}")
