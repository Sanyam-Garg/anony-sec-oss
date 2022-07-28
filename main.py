import typer, subprocess, os, stat
from dependencecheck.main import check_dir

app = typer.Typer()

def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            if name == 'vulns.txt' or name == 'vulns.json':
                pass
            else:
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name)) 

@app.command()
def hello(name: str):
    print(f'Hello {name}')

@app.command()
def analyse(src: str, with_dir: bool = False):
    if with_dir:
        check_dir(src)
    else:
        subprocess.run(["git", "clone", src], stdout=subprocess.DEVNULL)
        dirname = src.split("/")[-1]
        dirpath = os.path.join(os.getcwd(), dirname)
        check_dir(dirpath)
        rmtree(dirpath)

app()