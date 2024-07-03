import subprocess
from pathlib import Path
from typing import Optional
from datetime import datetime
import typer


def backup_database(db_type: str, username: str, password: str, db_name: Optional[str], path: Path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if db_type == "mysql":
        if db_name == "all":
            backup_file = path / f"all_databases_{timestamp}.sql"
            command = f"mysqldump -u {username} -p{password} --all-databases > {backup_file}"
        else:
            backup_file = path / f"{db_name}_{timestamp}.sql"
            command = f"mysqldump -u {username} -p{password} {db_name} > {backup_file}"

    elif db_type == "postgres":
        if db_name == "all":
            backup_file = path / f"all_databases_{timestamp}.sql"
            command = f"pg_dumpall -U {username} -f {backup_file}"
        else:
            backup_file = path / f"{db_name}_{timestamp}.sql"
            command = f"pg_dump -U {username} -d {db_name} -f {backup_file}"

    try:
        subprocess.run(command, shell=True, check=True)
        typer.style(f"Backup successful: {backup_file}", fg=typer.colors.GREEN, bold=True)
    except subprocess.CalledProcessError as e:
        typer.style(f"Backup failed: {e}", fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True)
