import os
from contextlib import contextmanager
import tempfile
import shutil
import yaml
import sys

@contextmanager
def tmpdir():
    dd = tempfile.mkdtemp()
    try:
        yield dd
    finally:
        shutil.rmtree(dd)


repos = [
    'https://github.com/szabgab/github-actions-python/',
    'https://github.com/szabgab/github-actions-perl-build/',
    'https://github.com/szabgab/github-actions-perl-makefile/',
    'https://github.com/szabgab/github-actions-perl-dist-zilla/',
    'https://github.com/szabgab/github-actions-crystal',
]

limit = False
if len(sys.argv) == 2:
    limit = True

errors = []
for repo in repos:
    print(repo)
    with tmpdir() as temp:
        print(temp)
        os.system(f"git clone {repo} {temp}")
        yaml_file = os.path.join(temp, '.github', 'workflows', 'ci.yml')
        if not os.path.exists(yaml_file):
            errors.append(f"ERROR: Yaml file '{yaml_file}' missing from {repo}")
            continue
        with open(yaml_file) as fh:
            config = yaml.load(fh, Loader=yaml.Loader)

        if config['name'] != 'CI':
            errors.append(f"ERROR: Incorrect name: '{config['name']}' not CI in {repo}")

        if config[True] != {
            'push': None,
            'pull_request': None,
            'workflow_dispatch': None,
            'schedule': [{'cron': '42 5 * * *'}]
        }:
            errors.append(f"ERROR: Incorrect 'on' field: '{config[True]}' in {repo}")

        if ['test'] != list(config['jobs'].keys()):
            errors.append(f"ERROR: Incorrect job names: '{config['jobs'].keys()}' in {repo}")
            continue

        if config['jobs']['test']['strategy']['fail-fast'] != False:
            errors.append(f"ERROR: fail-fast issue: '{config['jobs']['test']['strategy']}' in {repo}")
        if 'matrix' not in config['jobs']['test']['strategy']:
            errors.append(f"ERROR: no matrix in '{config['jobs']['test']['strategy']}' in {repo}")

        # TODO: Check if the checkout step is v3, but what should be the name?
        # if config['jobs']['test']['steps'][0] != {'name': 'Checkout', 'uses': 'actions/checkout@v3'}:
        #     errors.append(f"ERROR first step is not the expected Checkout. It is {config['jobs']['test']['steps'][0]} in {repo}")

        if limit:
            print(config)
            exit()

if errors:
    for error in errors:
        print(error)
    exit("There was an error")
