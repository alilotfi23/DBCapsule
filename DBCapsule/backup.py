import subprocess
from pathlib import Path
from typing import Optional
from datetime import datetime
import typer


def backup_database(
        db_type: str,
        username: str,
        password: str,
        db_name: Optional[str],
        path: Path,
        tablespaces: bool,
        schema: bool,
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if db_type == "mysql":
        if db_name == "all":
            backup_file = path / f"all_databases_{timestamp}.sql"
            command = ["mysqldump", "-u", username, "-p" + password, "--all-databases"]
        else:
            backup_file = path / f"{db_name}_{timestamp}.sql"
            command = ["mysqldump", "-u", username, "-p" + password, db_name]

    elif db_type == "postgres":
        backup_file = path / f"{db_name}_{timestamp}.sql"
        if db_name == "all":
            command = ["pg_dumpall", "-U", username, "-f", str(backup_file)]
        else:
            command = ["pg_dump", "-U", username, "-d", db_name, "-f", str(backup_file)]
            if tablespaces:
                command.append("--tablespaces-only")
            if schema:
                command.append("--schema-only")

    try:
        subprocess.run(command, check=True)
        typer.style(
            f"Backup successful: {backup_file}", fg=typer.colors.GREEN, bold=True
        )
    except subprocess.CalledProcessError as e:
        typer.style(
            f"Backup failed: {e}", fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True
        )
