
# Database Backup Tool

This command-line tool allows you to back up MySQL and PostgreSQL databases easily using Python and Typer (Python cli lib ).

## Features

- **Backup MySQL or PostgreSQL databases**
- **Backup all databases or a single database**
- **Dumps only the definitions of tablespaces no databases or roles (PostgreSQL)**
- **Dumps only the schema no data (PostgreSQL)**
- **Specify custom backup path**

## Prerequisites

- Python 3.x installed
- Required Python packages (`typer`, `pathlib`)
- MySQL (`mysqldump`) or PostgreSQL (`pg_dump`, `pg_dumpall`) command-line tools installed and accessible from the terminal

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/alilotfi23/DBCapsule.git
   cd DBCapsule
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Syntax

```bash
python dbcapsule.py backup [OPTIONS]
```

### Options

- `--db-type`: Specify the type of database (`mysql` or `postgres`).
- `--all`: Backup all databases
- `--single <database_name>`: Backup a single database by name.
- `--path <backup_path>`: Path to store the backup file.

### Examples

1. **Backup all MySQL databases**:

   ```bash
   python dbcapsule.py --db-type mysql --all --path /path/to/your/backup/folder
   ```

2. **Backup single MySQL databases**:

   ```bash
    python dbcapsule.py --db-type mysql --single your_database_name --path /path/to/your/backup/folder
   ```

3. **Backup a all PostgreSQL database**:

   ```bash
    python dbcapsule.py --db-type postgres --all --path /path/to/your/backup/folder
   ```
4. **Backup a single PostgreSQL database**:

   ```bash
   python dbcapsule.py --db-type postgres --single your_database_name --path /path/to/your/backup/folder
   ```
5. **Backup only the tablespaces of a single PostgreSQL database**:
    ```bash
    python dbcapsule.py backup --db-type postgres --single mydatabase --tablespaces --path /path/to/backup
    ```
6. **Backup only the schema of a single PostgreSQL database**:
    ```bash
    python dbcapsule.py backup --db-type postgres --single mydatabase --schema --path /path/to/backup
    ```

## Notes

- Make sure to provide correct database credentials when prompted.
- Ensure the specified backup path exists or allow the tool to create it.
