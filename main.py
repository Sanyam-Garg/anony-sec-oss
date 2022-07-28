import typer
from dependencecheck.main import check_dir

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f'Hello {name}')

@app.command()
def analyse(dir: str):
    check_dir(dir)

app()