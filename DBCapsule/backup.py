import subprocess  # To run shell commands
from pathlib import Path  # To handle file paths
from typing import Optional  # For optional type hinting
from datetime import datetime  # To work with date and time
import typer  # For command-line interface (CLI) functionality


def backup_database(
        db_type: str,  # Type of the database (e.g., 'mysql' or 'postgres')
        username: str,  # Database username
        password: str,  # Database password
        db_name: Optional[str],  # Name of the database to back up; can be 'all'
        path: Path,  # Path where the backup file will be stored
        tablespaces: bool,  # Flag to indicate if tablespaces should be included in the backup (Postgres only)
        schema: bool,  # Flag to indicate if only the schema should be backed up (Postgres only)
):
    # Generate a timestamp to append to the backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Handle MySQL backup
    if db_type == "mysql":
        if db_name == "all":
            # Create a backup file name for all databases
            backup_file = path / f"all_databases_{timestamp}.sql"
            # Construct the mysqldump command to back up all databases
            command = ["mysqldump", "-u", username, "-p" + password, "--all-databases"]
        else:
            # Create a backup file name for the specified database
            backup_file = path / f"{db_name}_{timestamp}.sql"
            # Construct the mysqldump command for the specified database
            command = ["mysqldump", "-u", username, "-p" + password, db_name]

    # Handle PostgreSQL backup
    elif db_type == "postgres":
        # Create a backup file name for the specified database
        backup_file = path / f"{db_name}_{timestamp}.sql"
        if db_name == "all":
            # Construct the pg_dumpall command to back up all databases
            command = ["pg_dumpall", "-U", username, "-f", str(backup_file)]
        else:
            # Construct the pg_dump command for the specified database
            command = ["pg_dump", "-U", username, "-d", db_name, "-f", str(backup_file)]
            if tablespaces:
                # If tablespaces flag is set, include tablespaces in the backup
                command.append("--tablespaces-only")
            if schema:
                # If schema flag is set, include only the schema in the backup
                command.append("--schema-only")

    try:
        # Execute the backup command
        subprocess.run(command, check=True)
        # Print a success message if the backup was successful
        typer.style(
            f"Backup successful: {backup_file}", fg=typer.colors.GREEN, bold=True
        )
    except subprocess.CalledProcessError as e:
        # Print an error message if the backup failed
        typer.style(
            f"Backup failed: {e}", fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True
        )
