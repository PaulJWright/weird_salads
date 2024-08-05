import logging
import sys

from sqlalchemy import MetaData, text

from weird_salads.utils.unit_of_work import UnitOfWork

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Send logs to stdout
)

logger = logging.getLogger(__name__)

# List tables to exclude
EXCLUDE_TABLES = {"alembic_version"}

# !TODO currently only runs if invoked from the root dir.


def clear_data():
    """Clears all data from all tables in the database."""
    with UnitOfWork() as uow:
        session = uow.session
        try:
            # Reflect the database schema to get table names
            # https://docs.sqlalchemy.org/en/20/core/reflection.html#reflecting-all-tables-at-once
            metadata_obj = MetaData()
            metadata_obj.reflect(bind=session.bind)

            tables_to_clear = [
                str(table.name)
                for table in metadata_obj.sorted_tables
                if table.name not in EXCLUDE_TABLES
            ]

            # Print tables that will be cleared
            print("Tables to be cleared:")
            for table in tables_to_clear:
                print(f" - {table}")

            for table in metadata_obj.sorted_tables:
                if table.name not in EXCLUDE_TABLES:
                    quoted_table_name = f'"{table.name}"'
                    session.execute(text(f"DELETE FROM {quoted_table_name}"))

            uow.commit()
            logging.info("Data cleared successfully.")
        except Exception as e:
            logging.warning(f"An error occurred while clearing data: {e}")


if __name__ == "__main__":
    clear_data()
