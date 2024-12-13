import subprocess

import typer
import uvicorn

from to_do_app.core.config import run_settings

APP_PATH = "to_do_app.app:app"
app = typer.Typer()

@app.command()
def start():
    typer.echo("try start --help to check the available options")

@app.command("start:dev")
def start_dev():
    typer.echo("Starting the development server...")
    uvicorn.run(
        app=APP_PATH,
        host=run_settings.host,
        port=run_settings.port,
        reload=True,
        log_level="debug"
    )

@app.command("start:prod")
def start_prod():
    typer.echo("Starting the production server...")
    uvicorn.run(
        app=APP_PATH,
        host=run_settings.host,
        port=run_settings.port,
        reload=False,
        log_level="info"
    )

@app.command()
def code():
    typer.echo("try code --help to check the available options")

@app.command("code:lint")
def code_lint():
    typer.echo("Linting the code")
    subprocess.run("poetry run ruff check .",shell=True, check=False)

@app.command("code:style")
def code_style():
    typer.echo("Formatting the code")
    subprocess.run("poetry run ruff check --fix .", shell=True, check=False)



if __name__ == "__main__":
    app()
