"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment.

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import sys

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

project_slug = "{{ cookiecutter.project_slug }}"
assert ' ' not in project_slug, "'{}' project slug shall not contain spaces.".format(project_slug)
assert project_slug.lower() == project_slug, "'{}' project slug shall be in lowercase letters.".format(project_slug)

app_name = "{{ cookiecutter.app_name }}"
if hasattr(app_name, "isidentifier"):
    assert app_name.isidentifier(), "'{}' app name is not a valid Python identifier.".format(app_name)

assert "\\" not in "{{ cookiecutter.author_name }}", "Don't include backslashes in author name."


if "{{ cookiecutter.use_docker }}".lower() == "n":
    python_major_version = sys.version_info[0]
    if python_major_version == 2:
        print(
            WARNING + "cookiecutter-django-shop does not support Python 2. "
            "Stability is guaranteed with Python 3.6+ only, are you sure you want to proceed (y/n)? " + TERMINATOR
        )
        yes_options, no_options = frozenset(["y"]), frozenset(["n"])
        while True:
            choice = raw_input().lower()
            if choice in yes_options:
                break

            elif choice in no_options:
                print(INFO + "Generation process stopped as requested." + TERMINATOR)
                sys.exit(1)
            else:
                print(
                    HINT
                    + "Please respond with {} or {}: ".format(
                        ", ".join(
                            ["'{}'".format(o) for o in yes_options if not o == ""]
                        ),
                        ", ".join(
                            ["'{}'".format(o) for o in no_options if not o == ""]
                        ),
                    )
                    + TERMINATOR
                )

languages = "{{ cookiecutter.languages }}".replace(' ', '').split(',')
for lang in languages:
    assert len(lang) == 2 and lang.lower() == lang, "Each language code shall consist of two lowercase letters, '" + lang + "' does not."
if "{{ cookiecutter.use_i18n }}" == 'y':
    assert len(languages) > 1, "'use_i18n' is set with less than two languages, which doesn't make sense."
else:
    assert len(languages) == 1, "If 'use_i18n' is unset, only one language shall be specified in 'languages'."
