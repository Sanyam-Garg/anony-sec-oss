import json, requests
from bs4 import BeautifulSoup

def version_comparison(manifest_file):
    with open(manifest_file, 'r') as fp:
        parsed_data = json.load(fp)
        dependencies = parsed_data['dependencies']
        # print(dependencies)

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
                print(f'[!] Package {key} is deprecated. Updating is highly recommended.')
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
                else:
                    print(f'[-] Recommended update {key} from {installed_version} to {latest_version}')