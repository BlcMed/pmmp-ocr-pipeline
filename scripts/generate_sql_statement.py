import json
import os
import logging


def load_config(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "info_extraction_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)

table_name = "airflow_table"
create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"

# dynamic SQL statement
for field in config["SQL_TABLE_FIELDS"]:
    field_name = field["name"]
    field_type = field["type"]
    create_table_sql += f"    {field_name} {field_type},\n"
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

logging.info("Generated SQL statement to create the table:")
logging.info(create_table_sql)

sql_file_path = os.path.join(config["SCRIPTS_FOLDER_PATH"], "create_table.sql")
try:
    with open(sql_file_path, "w") as sql_file:
        sql_file.write(create_table_sql)
    logging.info(f"SQL statement saved to {sql_file_path}")
except IOError as e:
    logging.error(f"Failed to save SQL statement to file: {e}")
