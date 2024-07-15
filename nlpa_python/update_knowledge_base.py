import getpass
import os
#from langchain.chains import GraphCypherQAChain
#from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
import pandas as pd

#os.environ["OPENAI_API_KEY"] = "sk-proj-pyhqyGcgMQj7PTSR5ZcBT3BlbkFJlefB1BhxK9fPtOOey7QA"
#os.environ["LANGCHAIN_API_KEY"] = "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"
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["NEO4J_URI"] = "atabases.neo4j.io"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "gRjPXYwV2njxNq_tgZ-xa5JV4"

finance_data_url = "https://raw.githubusercontent.com/IAmSudhirGupta/ml_ops/main/bank.csv"

graph = Neo4jGraph()

# Import Banking information

bank_query = """
            LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/IAmSudhirGupta/ml_ops/main/bank.csv' AS row
            WITH row,
                toFloat(REPLACE(row.total_assets_us_b, ",", "")) AS total_assets

            MERGE (b:Bank {name: row.bank})
            MERGE (c:Country {name: row.country})
            MERGE (b)-[:HAS_TOTAL_ASSETS {value: total_assets}]->(:TotalAssets {value: total_assets})
            MERGE (b)-[:LOCATED_IN]->(c)
            MERGE (b)-[:HAS_BALANCE_SHEET_DATE]->(:BalanceSheetDate {date: row.balance_sheet});
            """

graph.query(bank_query)

graph.refresh_schema()
print(graph.schema)

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True)
# response = chain.invoke({"query": "What was the cast of the Casino?"})
# response

df = pd.read_csv(finance_data_url)
print(df.head())
