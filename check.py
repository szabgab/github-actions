import os
from contextlib import contextmanager
import tempfile
import shutil
import yaml

@contextmanager
def tmpdir():
    dd = tempfile.mkdtemp()
    try:
        yield dd
    finally:
        shutil.rmtree(dd)


repos = [
    'https://github.com/szabgab/github-actions-python/',
    'https://github.com/szabgab/github-actions-perl-build/'
]

error = False
for repo in repos:
    print(repo)
    with tmpdir() as temp:
        print(temp)
        os.system(f"git clone {repo} {temp}")
        yaml_file = os.path.join(temp, '.github', 'workflows', 'ci.yml')
        if not os.path.exists(yaml_file):
            error = True
            print(f"Yaml file '{yaml_file}' missing from {repo}")

if error:
    exit("There was an error")
