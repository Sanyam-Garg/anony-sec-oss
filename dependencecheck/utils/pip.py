import requests, requirements, subprocess, os, json
from bs4 import BeautifulSoup

class PIP:
    
    def load_dependencies(manifest_file):
        dependencies = {}
        with open(manifest_file, 'r', encoding='utf-8') as fp:
            try:
                for req in requirements.parse(fp):
                    dependencies[req.name] = req.specs[-1][-1]
            except:
                raise Exception("[!] Error parsing requirements.txt file: Format not compatible.")
        return dependencies
            

    @classmethod
    def version_comparison(self, manifest_file):
        dependencies = self.load_dependencies(manifest_file)
        for key in dependencies:
            url = 'https://pypi.org/search/?q='+key
            r = requests.get(url)

            soup = BeautifulSoup(r.content, 'html.parser')
            latest_version = None
            temp = soup.find_all('span', class_='package-snippet__name')
            key_found = False
            for i in range(0, 3):
                if temp[i].text.lower() == key.lower():
                    key_found = True
                    latest_version = soup.find_all('span', class_='package-snippet__version')[i].text
                    break
            if not key_found:
                print(f'[!] Package {key} is deprecated. Update is highly recommended.')
            else:
                installed_version = dependencies[key].split('^')[-1]
                
                latest_major = latest_version.split('.')[0]
                installed_major = installed_version.split('.')[0]

                if latest_major > installed_major:
                    print(f'[!] Major update available for {key}: {installed_version} to {latest_version}')
                elif latest_version != installed_version:
                    print(f'[-] Recommended update {key} from {installed_version} to {latest_version}')
    
    @staticmethod
    def cve_check(dirname, requirements_file):
        # https://pypi.org/project/safety/
        os.chdir(dirname)
        subprocess.run(["safety", "check", "-r", requirements_file, "--save-json", "vulns.json"], stdout=subprocess.DEVNULL)
        with open('vulns.json', 'r') as fp:
            parsed_data = json.load(fp)
            print(f'Total vulnerabilites found in installed packages: {parsed_data["report_meta"]["vulnerabilities_found"]}')
            print(f"[+] More details are available in {os.path.join(dirname, 'vulns.json')} file.")