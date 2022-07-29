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
        score = 10.0
        dependencies = self.load_dependencies(manifest_file)
        cnt = len(dependencies)
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
                score -= (1/cnt) * score
            else:
                installed_version = dependencies[key].split('^')[-1]
                
                latest_major = latest_version.split('.')[0]
                installed_major = installed_version.split('.')[0]

                if latest_major > installed_major:
                    print(f'[!] Major update available for {key}: {installed_version} to {latest_version}')
                    score -= (0.7/cnt) * score
                elif latest_version != installed_version:
                    print(f'[-] Recommended update {key} from {installed_version} to {latest_version}')
                    score -= (0.4/cnt) * score
        return score
    
    @classmethod
    def cve_check(self, dirname, requirements_file):
        # https://pypi.org/project/safety/
        score = 10.0
        dependencies = self.load_dependencies(requirements_file)
        cnt = len(dependencies)
        os.chdir(dirname)
        subprocess.run(["safety", "check", "-r", requirements_file, "--save-json", "vulns.json"], stdout=subprocess.DEVNULL)
        with open('vulns.json', 'r') as fp:
            parsed_data = json.load(fp)
            print(f'Total vulnerabilites found in installed packages: {parsed_data["report_meta"]["vulnerabilities_found"]}')
            score -= (int(parsed_data["report_meta"]["vulnerabilities_found"])/cnt) * score
            print(f"[+] More details are available in {os.path.join(dirname, 'vulns.json')} file.")
        return score
    
    @staticmethod
    def examine_code(path):
        score = 10.0
        os.chdir(path)
        with open("code_analysis.txt", "w+") as fp:
            subprocess.run(["bandit", "-r", path], stdout=fp)
        with open("code_analysis.txt", "r") as fp:
            analysis = fp.readlines()
            print("Vulnerabilities on the basis of severity:")
            for i in [-10, -9, -8, -7]:
                spec = analysis[i].strip().split(':')
                num = spec[1].split(' ')[-1]
                print(f"{spec[0]}: {num}")
                if i == -10:
                    score -= (int(num) * 7) / 10
                elif i == -9:
                    score -= (int(num) * 5) / 10
                elif i == -8:
                    score -= (int(num) * 3) / 10

            print("Vulnerabilities on the basis of confidence:")
            for i in [-5, -4, -3, -2]:
                spec = analysis[i].strip().split(':')
                print(f"{spec[0]}: {spec[1].split(' ')[-1]}")
        print(f"[+] More details are available in {os.path.join(path, 'code_analysis.txt')} file.")
        return score