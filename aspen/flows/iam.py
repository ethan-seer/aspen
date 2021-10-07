import argparse
import subprocess
import logging
import os

from jinja2 import Template

from cli import iam
from storage import Storage
from storage import Read
from storage import options

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

# default, will be overwritten if arguments are given
credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get IAM data.")
    parser.add_argument(
        "--flow",
        "-f",
        type=str,
        nargs=1,
        choices=["all-project-recommendations"],
        help="Choose the flow.",
    )

    parser.add_argument(
        "--credentials",
        "-c",
        type=str,
        nargs=1,
        help="You must identify where credentials are coming from",
    )

    parser.add_argument(
        "--project-write-raw-file",
        "-pwrf",
        type=str,
        nargs=3,
        help="You must identify the file method, format, and  name, .",
    )
    parser.add_argument(
        "--recommendations-raw-file",
        "-rrf",
        type=str,
        nargs=3,
        help="Where the recommendations will be read for parsing. You must identify the file method, format, and  name. You can use Jinja2 templates with variables: project_id.",
    )
    parser.add_argument(
        "--recommendations-write-parsed-file",
        "-rwpf",
        type=str,
        nargs=3,
        help="Where the recommendatYou must identify the file method, format, and  name. You can use Jinja2 templates with variables: project_id.",
    )
    parser.add_argument(
        "--project-limit",
        "-pl",
        type=int,
        nargs=1,
        help="Limits the projects investigated.",
    )
    args = parser.parse_args()

    (
        flow,
        credentials,
        project_write_raw_file,
        recommendations_raw_file,
        recommendations_write_parsed_file,
        project_limit,
    ) = (
        args.flow[0],
        args.credentials[0],
        args.project_write_raw_file,
        args.recommendations_raw_file,
        args.recommendations_write_parsed_file,
        args.project_limit[0] if args.project_limit else None,
    )

    (
        project_write_raw_file_method,
        project_write_raw_file_format,
        project_write_raw_file_name,
    ) = project_write_raw_file

    (
        recommendations_raw_file_method,
        recommendations_raw_file_format,
        recommendations_raw_file_name,
    ) = recommendations_raw_file

    (
        recommendations_write_parsed_file_method,
        recommendations_write_parsed_file_format,
        recommendations_write_parsed_file_name,
    ) = recommendations_write_parsed_file

    project_write_file_name_template = Template(project_write_raw_file_name)

    recommendations_raw_file_name_template = Template(recommendations_raw_file_name)
    recommendations_write_parsed_file_name_template = Template(
        recommendations_write_parsed_file_name
    )

    if "all-project-recommendations" == flow:
        # get projects
        command = [
            "python3",
            "-m",
            "cli.iam",
            "-s",
            "cloudresourcemanager",
            "-a",
            "fetch",
            "-c",
            credentials,
            "-wf",
            project_write_raw_file_method,
            project_write_raw_file_format,
            project_write_raw_file_name,
        ]

        subprocess.run(command)

        # read the projects
        method = options(method=project_write_raw_file_method)

        read_obj = Read(
            destination=project_write_raw_file_name,
            extension="jsonl",
            method=method,
            service_account=credentials,
        )

        storage = Storage(read_obj=read_obj)
        projects = storage.read()

        # list the projects

        for project in projects[:project_limit]:

            # get recommendations for each project

            project_id = project["id"]
            logging.info(f"Getting data for {project_id}")
            command = [
                "python3",
                "-m",
                "cli.iam",
                "-s",
                "recommender",
                "-a",
                "fetch",
                "-c",
                credentials,
                "-wf",
                recommendations_raw_file_method,
                recommendations_raw_file_format,
                recommendations_raw_file_name_template.render(project_id=project_id),
                "-pid",
                project_id,
            ]
            subprocess.run(command)

            command = [
                "python3",
                "-m",
                "cli.iam",
                "-s",
                "recommender",
                "-a",
                "parse",
                "-c",
                credentials,
                "-wf",
                recommendations_write_parsed_file_method,
                recommendations_write_parsed_file_format,
                recommendations_write_parsed_file_name_template.render(
                    project_id=project_id
                ),
                "-rf",
                recommendations_raw_file_method,
                recommendations_raw_file_format,
                recommendations_raw_file_name_template.render(project_id=project_id),
                "-pid",
                project_id,
            ]
            subprocess.run(command)
