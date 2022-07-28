import os
from utils.npm import NPM
from utils.pip import PIP

DIR_PATH = "F:\\Django Projs\\ardportal\\api"

pckg_json_found = False
pckg_lck_json_found = False
req_txt_found = False
req_dev_txt_found = False

for fname in os.listdir(DIR_PATH):
    if fname == 'package.json':
        pckg_json_found = True
    elif fname == 'package-lock.json':
        pckg_lck_json_found = True
    elif fname == 'requirements.txt':
        req_txt_found = True
    elif fname == 'requirements-dev.txt':
        req_dev_txt_found = True

if not (pckg_json_found and pckg_lck_json_found) and not (req_txt_found or req_dev_txt_found):
    print("[!] Error: Manifest files for npm or python not found")
elif pckg_lck_json_found and pckg_json_found:
    # NPM Check
    print("#"*50)
    print("Performing NPM dependency version checks....")
    print("#"*50)
    NPM.version_comparison(os.path.join(DIR_PATH, 'package.json'))
    print("#"*50)
    print("Performing NPM vulnerabilities check....")
    print("#"*50)
    NPM.cve_check(DIR_PATH)
elif req_txt_found:
    # Python checks
    print("#"*50)
    print("Performing PIP dependency version checks....")
    print("#"*50)
    PIP.version_comparison(os.path.join(DIR_PATH, 'requirements.txt'))
    print("#"*50)
    print("Performing PIP vulnerabilities check....")
    print("#"*50)
    PIP.cve_check(DIR_PATH, os.path.join(DIR_PATH, 'requirements.txt'))
    pass
elif req_dev_txt_found:
    # Python checks
    print("#"*50)
    print("Performing PIP dependency version checks....")
    print("#"*50)
    PIP.version_comparison(os.path.join(DIR_PATH, 'requirements.txt'))
    pass