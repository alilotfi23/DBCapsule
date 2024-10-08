import typer  # Importing the Typer library for creating command-line interfaces
from pathlib import Path  # Importing Path for handling filesystem paths
from typing import Optional  # Importing Optional for optional type hinting
from backup import backup_database  # Importing the backup_database function from the backup module

app = typer.Typer()  # Creating an instance of Typer for the command-line application


@app.command()  # Defining a command for the Typer application
def backup(
        db_type: str = typer.Option(..., help="Database type (mysql or postgres)"),  # Required option for database type
        all: bool = typer.Option(False, help="Backup all databases"),  # Option to backup all databases
        single: Optional[str] = typer.Option(None, help="Backup a single database by name"),  # Option for single database backup
        path: Path = typer.Option(..., help="Path to store the backup file"),  # Required option for specifying backup file path
        tablespaces: bool = typer.Option(False, help="Dump only tablespaces for PostgreSQL"),  # Option for PostgreSQL tablespaces
        schema: bool = typer.Option(False, help="Dump only the schema for PostgreSQL"),  # Option for PostgreSQL schema only
):
    # Validate the database type
    if db_type not in ["mysql", "postgres"]:
        typer.echo("Please specify a valid database type: 'mysql' or 'postgres'.")  # Error message for invalid type
        raise typer.Exit()  # Exit the application

    # Ensure that either 'all' or 'single' is specified
    if not all and not single:
        typer.echo("Please specify either --all or --single <database name>.")  # Error message for missing options
        raise typer.Exit()  # Exit the application

    # Determine the database name to backup
    db_name = "all" if all else single  # Set db_name to 'all' if all is True, otherwise use the single database name

    # Check if the specified path exists
    if not path.exists():
        # Prompt the user to create the path if it doesn't exist
        create_path = typer.confirm(f"Path {path} does not exist. Do you want to create it?")
        if not create_path:
            typer.style("Backup aborted.", fg=typer.colors.MAGENTA)  # Style the abort message
            raise typer.Exit()  # Exit the application
        path.mkdir(parents=True, exist_ok=True)  # Create the directory with parents if necessary

    # Prompt the user for database credentials
    username = typer.prompt(f"Enter {db_type.upper()} username")  # Prompt for username
    password = typer.prompt(f"Enter {db_type.upper()} password", hide_input=True)  # Prompt for password (hidden input)

    # Call the backup_database function with the provided parameters
    backup_database(db_type, username, password, db_name, path, tablespaces, schema)  # Perform the backup operation

if __name__ == "__main__":  # Check if the script is being run directly
    app()  # Run the Typer application
