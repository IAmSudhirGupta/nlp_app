from rdflib import Graph, Namespace, RDF, XSD, Literal
from neo4j import GraphDatabase
import csv
# Replace with your Neo4j connection details
#uri = "neo4j+s://4b8f0e1f.databases.neo4j.io"
#username = "neo4j"
#password = "gPt46qOtoMvRjPXYwV2njxNq_tgb2UpD3wmZ-xa5JV4"

# Replace these variables with your actual Neo4j connection details
URI = "neof0e1f.database.io"
USERNAME = "neo4j"
PASSWORD = "46xNq_tgb2UpD3JV4"
CSV_FILE_PATH = "data/bank.csv"

df = pd.read_csv(finance_data_url)
df.head()

class BankDatabase:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_bank_data(self, rank, bank, country, total_assets_us_b, balance_sheet):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_link_nodes, rank, bank, country, total_assets_us_b, balance_sheet)

    @staticmethod
    def _create_and_link_nodes(tx, rank, bank, country, total_assets_us_b, balance_sheet):
        query = """
        MERGE (c:Country {name: $country})
        MERGE (b:Bank {name: $bank})
        ON CREATE SET 
            b.rank = $rank,
            b.total_assets_us_b = $total_assets_us_b,
            b.balance_sheet_date = $balance_sheet
        MERGE (b)-[:LOCATED_IN]->(c)
        MERGE (b)-[:HAS_TOTAL_ASSETS {value: $total_assets_us_b}]->(ta:TotalAssets {value: $total_assets_us_b})
        MERGE (b)-[:HAS_BALANCE_SHEET_DATE {date: $balance_sheet}]->(bs:BalanceSheetDate {date: $balance_sheet})
        """
        tx.run(query, rank=rank, bank=bank, country=country, total_assets_us_b=total_assets_us_b, balance_sheet=balance_sheet)

def read_csv_and_insert_data(csv_file_path, db):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rank = int(row['rank'])
            bank = row['bank']
            country = row['country']
            total_assets_us_b = float(row['total_assets_us_b'].replace(',', ''))
            balance_sheet = row['balance_sheet']
            db.create_bank_data(rank, bank, country, total_assets_us_b, balance_sheet)

if __name__ == "__main__":
    db = BankDatabase(URI, USERNAME, PASSWORD)
    try:
        read_csv_and_insert_data(CSV_FILE_PATH, db)
    finally:
        db.close()