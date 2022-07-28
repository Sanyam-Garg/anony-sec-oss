import json, requests, os, subprocess
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
        dependencies = self.load_dependencies(manifest_file)
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
                print(f'[!] Package {key} is deprecated. Update is highly recommended.')
            else:
                # Get latest version of the depencency
                dep = soup.find('span', class_='_657f443d')
                latest_version = dep.text.split(' ')[1]
                installed_version = dependencies[key].split('^')[-1]

                latest_major = latest_version.split('.')[0]
                installed_major = installed_version.split('.')[0]

                # Check backwards incompatible updates
                if int(installed_major) < int(latest_major):
                    print(f'[!] Major update available for {key}: {installed_version} to {latest_version}')
                elif latest_version != installed_version:
                    print(f'[-] Recommended update {key} from {installed_version} to {latest_version}')

    @staticmethod
    def cve_check(dirname):
        # cwd = os.getcwd()
        # path_to_vulns = os.path.join(cwd, "vulns.txt")
        os.chdir(dirname)
        with open("vulns.txt", "w") as fp:
            subprocess.run(["npm", "audit"], stdout=fp)
        
        # Read the number of vulnerabilities
        with open(os.path.join(dirname, 'vulns.txt'), "r") as fp:
            vuln = fp.read().split('\n')[-5]
            print(vuln)
            print(f"[+] More details are available in {os.path.join(dirname, 'vulns.txt')} file.")
            # vuln = vuln.split(' ')
            # print(f'[!] Total vulnerabilities: {vuln[0]}')
            # if len(vuln) == 8:
            #     print(f"[!] Moderate vulnerabilities: {vuln[2].split('(')[-1]}")
            #     print(f'[!] High vulnerabilities: {vuln[4]}')
            #     print(f'[!] Critical vulnerabilities: {vuln[6]}')
