import os
from utils.npm import version_comparison, cve_check

DIR_PATH = "F:\\Node.JS\\weather-app"

pckg_json_found = False
pckg_lck_json_found = False
req_txt_found = False

for fname in os.listdir(DIR_PATH):
    if fname == 'package.json':
        pckg_json_found = True
    elif fname == 'package-lock.json':
        pckg_lck_json_found = True
    elif fname == 'requirements.txt' or fname == 'requirements-dev.txt':
        req_txt_found = True

if not (pckg_json_found and pckg_lck_json_found) and not req_txt_found:
    print("[!] Error: Manifest files for npm or python not found")
elif pckg_lck_json_found and pckg_json_found:
    # NPM Check
    print("#"*50)
    print("Performing NPM dependency version checks....")
    print("#"*50)
    version_comparison(os.path.join(DIR_PATH, 'package.json'))
    print("#"*50)
    print("Performing NPM vulnerabilities check....")
    print("#"*50)
    cve_check(DIR_PATH)
elif req_txt_found:
    # Python checks
    pass