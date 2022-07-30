# Open Source Security Software
A python based open source security software developed during the round 2 of the Flipkart Grid 4.0 Information Security track. The aim is to create an open source repository analysis tool to inspect the contents of the repository and provide a security rating. This will help developers using these repositories in their projects to make an informed decision about what repositories to use and build secure and trustworthy applications.

## Parameters
The tool calculates the security rating of a repository based on the following parameters:

1. **The version of the dependencies installed:**
One of the most easily overlooked and yet the most common vectors of security flaws in a repository is the usage of outdated or deprecated depencencies. The tool reads the manifest file provided in the repository and then compares the latest version available on the corressponding cloud repository for any update requirements.<br>
2. **The vulnerabilities in the dependencies installed:**
Sometimes, even if the current dependency version is not the latest, there may not be any security vulnerabilites in the dependency, since the updated versions might just have added new features. In such cases, an update is not required on a high priority. Hence in this step, the tool scans the dependencies and looks for any vulnerabilities that have been identified in any of them. If found, it prints them out where the developers can make decision for themselves.<br>
3. **Static code analysis**
Finally, after the dependencies have been analysed, the tool then perform static application security testing on the code with the aim of identifying possible attack vectors that may be exploited. These type of tests aren't a 100% accurate, but provide a benchmark to the developer with regards to the quality of code in the repository.

## Requirements
* `npm`
* `python`
* `pip`
* python `virtualenv`

## Installation
1. Create a virtual environment using `python -m virtualenv <ENV_NAME>`. 
2. `cd` into the environment folder.
3. Activate the virtual environment: `.\Scripts\activate` for Windows; `source bin/activate` for Linux and Mac users.
4. Clone this repository: `git clone https://github.com/Sanyam-Garg/anony-sec-oss`
5. `cd` into the project folder: `cd anony-sec-oss`
6. Install the dependencies: `pip install -r requirements.txt`

## Usage
This is a command line tool that can function with a repository link, or if the repository is already cloned on your pc, the path to the repository.
1. **Using repository link**
    * From the project folder, run the following command: `python main.py analyse <Repository GitHub link>`
        > Since the libraries or packages available on pip or npm both have their source code on GitHub, we take the GitHub link as the input.
2. **Using path to downloaded repository**
From the project folder, run the following command : `python main.py analyse <path-to-downloaded-repo> --with-dir`
>The tool then prints out the security information of the repository onto the terminal and stores some additional files in the cloned repositories folder.