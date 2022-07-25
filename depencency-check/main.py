import os
from utils.npm import version_comparison

DIR_PATH = "."

flag = False
for fname in os.listdir(DIR_PATH):
    if fname == 'package.json':
        flag = True
        print("Performing NPM dependency version checks..")
        version_comparison(os.path.join(DIR_PATH, 'package.json'))
        pass
    elif fname == 'requirements.txt' or fname == 'requirements-dev.txt':
        flag = True
        print("Performing Python dependency version checks..")
        pass

if not flag:
    print("[!] Error: Dependency file for npm or python not found")