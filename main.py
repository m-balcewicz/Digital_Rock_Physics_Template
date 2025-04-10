# This is a sample Python script.
from pathlib import Path
import os


# Press ⇧F10 to execute it or replace it with your drp_template.
# Press Double ⇧ to search everywhere for classes, files, tools windows, actions, and settings.

def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome')
    print('developed 05/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def add_project():
    project_id = input('Define the name of your new project: ')

    # Create the directory if it doesn't exist
    project_path = Path('projects') / project_id
    try:
        project_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        print(f'Error creating project directory: {project_path}')
        return

    # Create a new Python script with some basic content
    script_path = project_path / f'main_{project_id}.py'
    cwd = os.getcwd()
    try:
        with open(script_path, 'w') as file:
            file.write('# New Python script\n\n')
            file.write('import sys\n')
            file.write(f'sys.path.append(\'{cwd}\')\n\n')
            file.write('if __name__ == \'__main__\':\n')
            file.write('    print("Hello, world!")\n')
    except OSError:
        print(f'Error creating Python script: {script_path}')
        return

    # Print a message to confirm the creation of the project
    print(f'Project "{project_id}" created successfully at "{project_path}"')


# ------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    main()
    add_project()
