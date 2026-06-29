import pandas as pd

from pathlib import Path

OUTPUT = Path("output")

OUTPUT.mkdir(exist_ok=True)


class LoadAudit:

    def __init__(self):

        self.records = []

    def add(self, table, rows_loaded, rejected):

        self.records.append({

            "table": table,

            "rows_loaded": rows_loaded,

            "rows_rejected": rejected

        })

    def save(self):

        df = pd.DataFrame(self.records)

        df.to_csv(

            OUTPUT / "load_audit.csv",

            index=False

        )