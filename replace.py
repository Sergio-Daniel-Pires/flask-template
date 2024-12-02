import os
from argparse import ArgumentParser

from jinja2 import Template

replace_parser = ArgumentParser(
    prog="Flask backend replacer", usage="python replace.py -n <project_name> -p <port>",
    description= (
        "Replace variables E.g. {{ port }} in backend flask template with user input value."
    )
)

replace_parser.add_argument(
    "-n", "--project_name", help="Project name", required=True, type=str
)

replace_parser.add_argument(
    "-p", "--port", help="Flask Project Port", required=True, type=int
)

replace_parser.add_argument(
    "-a", "--author", help="Author name", required=True, type=str
)

replace_parser.add_argument(
    "-e", "--email", help="Author email", required=True, type=str
)

def main(args: list[str] = None):
    parsed_args = replace_parser.parse_args(args)

    templates = (
        "Dockerfile.template", "docker-compose.template.yml", "pyproject.template.toml"
    )

    for template_file_name in templates:
        with open(template_file_name) as file:
            template = Template(file.read())

            content = template.render(
                project_name=parsed_args.project_name, port=parsed_args.port,
                author=parsed_args.author, author_email=parsed_args.email
            )

        os.remove(template_file_name)
        template_file_name = template_file_name.replace(".template", "")

        with open(template_file_name, "w") as file:
            file.write(content)

if __name__ == "__main__":
    main()
