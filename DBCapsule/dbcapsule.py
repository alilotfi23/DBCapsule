import typer
from pathlib import Path
from typing import Optional
from backup import backup_database

app = typer.Typer()


@app.command()
def backup(
        db_type: str = typer.Option(..., help="Database type (mysql or postgres)"),
        all: bool = typer.Option(False, help="Backup all databases"),
        single: Optional[str] = typer.Option(None, help="Backup a single database by name"),
        path: Path = typer.Option(..., help="Path to store the backup file"),
        tablespaces: bool = typer.Option(False, help="Dump only tablespaces for PostgreSQL"),
        schema: bool = typer.Option(False, help="Dump only the schema for PostgreSQL"),
):
    if db_type not in ["mysql", "postgres"]:
        typer.echo("Please specify a valid database type: 'mysql' or 'postgres'.")
        raise typer.Exit()

    if not all and not single:
        typer.echo("Please specify either --all or --single <database name>.")
        raise typer.Exit()

    db_name = "all" if all else single

    if not path.exists():
        create_path = typer.confirm(f"Path {path} does not exist. Do you want to create it?")
        if not create_path:
            typer.style("Backup aborted.", fg=typer.colors.MAGENTA)
            raise typer.Exit()
        path.mkdir(parents=True, exist_ok=True)

    username = typer.prompt(f"Enter {db_type.upper()} username")
    password = typer.prompt(f"Enter {db_type.upper()} password", hide_input=True)

    backup_database(db_type, username, password, db_name, path, tablespaces, schema)

if __name__ == "__main__":
    app()
