#!/usr/bin/env python3
# coding=utf-8

import os
import subprocess

repo_root = os.path.dirname(os.path.abspath(__file__))

project = {
    "project_name": "Store Supervisor",
    "project_root": os.path.join(repo_root, "supervisor"),
    "management": os.path.join(repo_root, "supervisor", "manage.py"),
    "venv_path": os.path.join(repo_root, "supervisor", "venv"),
    "python_path": os.path.join(repo_root, "supervisor", "venv", "bin", "python"),
    "pip_path": os.path.join(repo_root, "supervisor", "venv", "bin", "pip"),
    "requirements_file": os.path.join(repo_root, "supervisor", "supervisor", "requirements", "requirements.txt")
}


def print_update(description):
    """
    Print a nice title surrounded by stars and new lines for each task.
    :param description: Str, description of the task being run.
    """
    stars = "".join(["*" for _ in range(len(description))])
    print("\n\n\n")
    print(stars)
    print(description)
    print(stars)
    print("\n")


class Setup:
    """
    Setup Python developmemnt environments.
    """

    @staticmethod
    def virtualenivronments():
        """
        Setup a virtualenvironment named 'venv' in the root of each Django project.
        """
        print_update("Setting up Virtual Environment for {}".format(project.get("project_name")))
        subprocess.run("python3 -m venv {venv}".format(venv=project.get("venv_path")), shell=True)

    @staticmethod
    def requirements():
        """
        Run pip install on all the environments.
        """
        print_update("Installing requirements for {}".format(project.get("project_name")))
        install_commands = [
            '{pip} install -U pip'.format(pip=project.get("pip_path")),
            '{pip} install wheel'.format(pip=project.get("pip_path")),
            '{pip} install -r {requirements} --no-warn-script-location'.format(
                pip=project.get("pip_path"),
                requirements=project.get("requirements_file")
            )
        ]
        for command in install_commands:
            subprocess.run(command, shell=True, cwd=project.get("project_root"))

    @staticmethod
    def migrations():
        """
        Migrate databases on all the projects (local dbs will be in their respective project roots).
        """
        print_update("Running migrations for {}".format(project.get("project_name")))
        migrate_command = "{python} {manage} migrate".format(
            python=project.get("python_path"),
            manage=project.get("management")
        )
        subprocess.run(migrate_command, shell=True, cwd=project.get("project_root"))

    @staticmethod
    def populate_databases():
        """
        Run populate database management task to generate development data.
        """
        print_update("Populating database for {}".format(project.get("project_name")))
        populate_command = "{python} {manage} populate_database".format(
            python=project.get("python_path"),
            manage=project.get("management")
        )
        subprocess.run(populate_command, shell=True, cwd=project.get("project_root"))


if __name__ == "__main__":
    Setup.virtualenivronments()
    Setup.requirements()
    Setup.migrations()
    Setup.populate_databases()
