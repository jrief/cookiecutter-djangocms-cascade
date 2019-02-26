"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import os
import subprocess
import random
import shutil
import string


try:
    # Inspired by https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_pycharm_files():
    idea_dir_path = ".idea"
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join("docs", "pycharm")
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_docker_files():
    shutil.rmtree("docker-files")
    file_names = [".dockerignore", "docker-compose.yml"]
    for file_name in file_names:
        os.remove(file_name)


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        symbols += string.punctuation.replace('"', "").replace("'", "").replace(
            "\\", ""
        )
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_secret_key


def set_django_admin_url(file_path):
    django_admin_url = set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_admin_url


def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)


def set_database_password(file_path, value=None):
    database_password = set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=20,
        using_digits=True,
        using_ascii_letters=True,
    )
    return database_password


def pipenv_to_requirements():
    ret = subprocess.check_output(['pipenv', 'lock', '--requirements'])
    with open('requirements.txt', 'w') as fh:
        fh.write(ret.decode('utf-8'))


def main():
    debug = "{{ cookiecutter.debug }}".lower() == "y"

    set_django_secret_key(os.path.join("{{ cookiecutter.app_name }}", "settings.py"))

    if "{{ cookiecutter.use_pycharm }}".lower() == "n":
        remove_pycharm_files()

    if "{{ cookiecutter.use_docker }}".lower() == "y":
        pipenv_to_requirements()
        set_database_password("docker-files/databases.environ")
        next_steps = """
  cd {{ cookiecutter.project_slug }}
  docker-compose up --build -d
"""
    else:
        remove_docker_files()
        next_steps = """
  cd {{ cookiecutter.project_slug }}
  pipenv install --sequential
  npm install
  pipenv run ./manage.py migrate
  pipenv run ./manage.py createsuperuser
  pipenv run ./manage.py runserver
"""
    print(INFO + "Next steps to perform:" + TERMINATOR)
    print(HINT + next_steps + TERMINATOR)
    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
