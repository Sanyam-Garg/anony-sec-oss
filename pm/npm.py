import json, requests, os, subprocess
from colorama import Fore, Style, Back
from bs4 import BeautifulSoup

class NPM:

    @staticmethod
    def load_dependencies(manifest_file):
        with open(manifest_file, 'r') as fp:
            parsed_data = json.load(fp)
            dependencies = parsed_data['dependencies']
            return dependencies

    @classmethod
    def version_comparison(self, manifest_file):
        score = 10.0
        dependencies = self.load_dependencies(manifest_file)
        cnt = len(dependencies)
        for key in dependencies:
            # print(key, dependencies[key])
            url = 'https://www.npmjs.com/search?q='+key
            r = requests.get(url)

            # Create soup object
            soup = BeautifulSoup(r.content, 'html.parser')

            # Get title
            first_result_title = soup.find('h3', class_='db7ee1ac fw6 f4 black-90 dib lh-solid ma0 no-underline hover-black').text

            # If first result is not equal to the key, the package is deprecated
            if first_result_title != key:
                print(Fore.RED + f'[!] Package {key} is deprecated. Update is highly recommended.')
                print(Style.RESET_ALL)
                score -= (1/cnt) * score
            else:
                # Get latest version of the depencency
                dep = soup.find('span', class_='_657f443d')
                latest_version = dep.text.split(' ')[1]
                installed_version = dependencies[key].split('^')[-1]

                latest_major = latest_version.split('.')[0]
                installed_major = installed_version.split('.')[0]

                # Check backwards incompatible updates
                if int(installed_major) < int(latest_major):
                    print(Fore.YELLOW + f'[!] Major update available for {key}: {installed_version} to {latest_version}')
                    print(Style.RESET_ALL)
                    score -= (0.7/cnt) * score
                elif latest_version != installed_version:
                    print(Fore.CYAN + f'[-] Recommended update {key} from {installed_version} to {latest_version}')
                    print(Style.RESET_ALL)
                    score -= (0.4/cnt) * score
        return score
    @staticmethod
    def cve_check(dirname):
        # cwd = os.getcwd()
        # path_to_vulns = os.path.join(cwd, "vulns.txt")
        score = 10.0
        os.chdir(dirname)
        with open("vulns.txt", "w") as fp:
            if os.name == 'nt':
                subprocess.run(["npm", "audit"], stdout=fp, shell=True)
            elif os.name == 'posix':
                subprocess.run(["npm", "audit"], stdout=fp)
        
        # Read the number of vulnerabilities
        with open(os.path.join(dirname, 'vulns.txt'), "r") as fp:
            vuln = fp.read().split('\n')[-5]
            print(Fore.RED + vuln)
            print(Style.RESET_ALL)
            print(f"[+] More details are available in {os.path.join(dirname, 'vulns.txt')} file.")
            vuln = vuln.split(' ')
            # print(f'[!] Total vulnerabilities: {vuln[0]}')
            if vuln[0] == 'no':
                return score
            if len(vuln) == 8:
                # print(f"[!] Moderate vulnerabilities: {vuln[2].split('(')[-1]}")
                score -= (int(vuln[4]) * 0.5) / 10
                # print(f'[!] High vulnerabilities: {vuln[4]}')
                score -= (int(vuln[4])) * 0.7 / 10
                # print(f'[!] Critical vulnerabilities: {vuln[6]}')
                score -= (int(vuln[4]) * 1) / 10
            else:
                score -= (int(vuln[0]) * 0.6) / 10
            
        return score
