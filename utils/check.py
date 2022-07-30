import os
from pm.npm import NPM
from pm.pip import PIP
from colorama import Fore, Style, Back

# dir = "."

def check_dir(dir):
    pckg_json_found = False
    pckg_lck_json_found = False
    req_txt_found = False

    for fname in os.listdir(dir):
        if fname == 'package.json':
            pckg_json_found = True
        elif fname == 'package-lock.json':
            pckg_lck_json_found = True
        elif fname == 'requirements.txt':
            req_txt_found = True

    if not (pckg_json_found and pckg_lck_json_found) and not req_txt_found:
        print(Fore.RED + "[!] Error: Manifest files for npm or python not found")
        print(Style.RESET_ALL)
    elif pckg_lck_json_found and pckg_json_found:
        # NPM Check
        print(Fore.LIGHTYELLO_EX + "="*50)
        print("Performing NPM dependency version checks....")
        print("="*50)
        print(Style.RESET_ALL)
        version_score = NPM.version_comparison(os.path.join(dir, 'package.json'))
        print(Fore.LIGHTYELLOW_EX + "="*50)
        print("Performing NPM vulnerabilities check....")
        print("="*50)
        print(Style.RESET_ALL)
        package_cve_score = NPM.cve_check(dir)
        score = (version_score + package_cve_score) / 2
        print(Back.LIGHTBLUE_EX + "="*50)
        print(f'Repository dependency version rating: {version_score:.2f}/10')
        print(f'Repository dependency vulnerability rating: {package_cve_score:.2f}/10')
        print(f'Repository overall security rating: {score}/10')
        print("="*50)
        print(Style.RESET_ALL)
    elif req_txt_found:
        # Python checks
        print(Fore.LIGHTYELLOW_EX + "="*50)
        print("Performing PIP dependency version checks.")
        print("="*50)
        print(Style.RESET_ALL)
        version_score = PIP.version_comparison(os.path.join(dir, 'requirements.txt'))
        print(Fore.LIGHTYELLOW_EX + "="*50)
        print("Performing PIP vulnerabilities check.")
        print("="*50)
        print(Style.RESET_ALL)
        package_cve_score = PIP.cve_check(dir, os.path.join(dir, 'requirements.txt'))
        print(Fore.LIGHTYELLOW_EX + "="*50)
        print("Performing static code analysis")
        print("="*50)
        print(Style.RESET_ALL)
        sast_score = PIP.examine_code(dir)
        score = (version_score + package_cve_score + sast_score) / 3
        print("="*50)
        print(Back.LIGHTBLUE_EX + f'Repository dependency version rating: {version_score:.2f}/10')
        print(f'Repository dependency vulnerability rating: {package_cve_score:.2f}/10')
        print(f'Repository static code analysis rating: {sast_score:.2f}/10')
        print(f'Repository overall security rating: {score:.2f}/10')
        print(Style.RESET_ALL)
        print("="*50)
