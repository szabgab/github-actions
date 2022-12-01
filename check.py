import yaml
import os
import shutils

repos = [
    'https://github.com/szabgab/github-actions-python/',
    'https://github.com/szabgab/github-actions-perl-build/'
]

for repo in repos:
    temp = 'temp'
    if os.path.exists(temp):
        shutil.rmdir(temp)
    os.system("git clone repo ${temp}")
