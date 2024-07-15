import spacy
from neo4j import GraphDatabase
import re

# Neo4j connection details
uri = "###"
username = "###"
password = "###"

# Load the English language model
nlp = spacy.load('en_core_web_sm')

def parse_question(question):
    doc = nlp(question)
    parsed = {
        'text': question,
        'tokens': [token.text for token in doc],
        'pos_tags': [(token.text, token.pos_) for token in doc],
        'entities': [(ent.text, ent.label_) for ent in doc.ents]
    }
    return parsed

def analyze_question(parsed_question):
    #  semantic analysis based on parsed data
    entities = [entity[0] for entity in parsed_question['entities']]
    main_verb = None
    for token in parsed_question['tokens']:
        if token.lower() in ['do', 'does', 'did', 'have', 'has', 'had']:
            main_verb = token
            break
    return {
        'text': parsed_question['text'],
        'entities': entities,
        'main_verb': main_verb
    }

# Function to execute Cypher query
def execute_cypher_query(query):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run(query)
        records = [record for record in result]
    driver.close()
    return records

# Function to convert natural language question to Cypher query
def question_to_cypher(question):
    if "total assets" in question.lower():
        return generate_total_assets_query(question)
    elif "banks" in question.lower() and ("total assets" in question.lower() or "assets" in question.lower()):
        return generate_banks_with_assets_query(question)
    elif "total assets" in question.lower() and ("in" in question.lower() or "of" in question.lower()):
        return generate_assets_in_specific_year_query(question)
    else:
        return "Unsupported question type."

def extract_bank_name_from_question(question):
    parsed_question = parse_question(question)
    # org_entities = [entity.text for entity in parsed_question['entities'] if entity.label_ == 'ORG']
    org_entities = next((entity for entity, label in parsed_question['entities'] if label == 'ORG'), None)
    return org_entities

def extract_threshort_amount(question):
    parsed_question = parse_question(question)
    # org_entities = [entity.text for entity in parsed_question['entities'] if entity.label_ == 'ORG']
    org_entities = next((entity for entity, label in parsed_question['entities'] if label == 'CARDINAL'), None)
    amounts = re.findall(r'\d+', org_entities)
    return amounts[0] if amounts else None

def extract_year_from_question(question):
    parsed_question = parse_question(question)
    # y_entities = [entity.text for entity in parsed_question['entities'] if entity.label_ == 'DATE']
    y_entities = next((entity for entity, label in parsed_question['entities'] if label == 'DATE'), None)
    return y_entities

# Generate query for total assets of a specific bank
def generate_total_assets_query(question):
    bank_name = extract_bank_name_from_question(question)  # Function to extract bank name
    print(bank_name)
    return (
        f"MATCH (b:Bank {{name: '{bank_name}'}})-[r:HAS_TOTAL_ASSETS]->(a:TotalAssets) "
        f"RETURN b.name AS bankName, a.value AS totalAssets"
    )

# Generate query for banks with total assets greater than a specified amount
def generate_banks_with_assets_query(question):
    threshold_amount = extract_threshort_amount(question)  # Function to extract threshold amount
    return (
        f"MATCH (b:Bank)-[r:HAS_TOTAL_ASSETS]->(a:TotalAssets) "
        f"WHERE a.value > {threshold_amount}"
        f" RETURN b.name AS bankName, a.value AS totalAssets"
    )

# Generate query for total assets of a bank in a specific year
def generate_assets_in_specific_year_query(question):
    bank_name = extract_bank_name_from_question(question)  # Function to extract bank name
    year = extract_year_from_question(question)  # Function to extract year
    return (
        f"MATCH (b:Bank {{name: '{bank_name}'}})-[r:HAS_TOTAL_ASSETS]->(a:TotalAssets)"
        f"WHERE a.balance_sheet = '{year}-12-31'"
        f"RETURN b.name AS bankName, a.value AS totalAssets"
    )

# Function to rank and retrieve answers based on relevance and confidence
def rank_and_retrieve_answers(question):
    cypher_query = question_to_cypher(question)
    print("\nCypher Query:")
    print(cypher_query)

    if cypher_query != "Unsupported question type.":
        results = execute_cypher_query(cypher_query)
        ranked_results = rank_results(results)  # Rank results based on relevance and confidence
        return ranked_results
    else:
        return []

# Function to rank results based on relevance ( implementation)
def rank_results(results):
    # Placeholder implementation, replace with actual ranking logic based on relevance and confidence scores
    ranked_results = []
    for result in results:
        relevance_score = calculate_relevance(result)  #  calculate relevance based on properties
        confidence_score = calculate_confidence(result)  #  calculate confidence based on query match
        ranked_results.append((result, relevance_score * confidence_score))
    ranked_results.sort(key=lambda x: x[1], reverse=True)  # Sort results by combined score
    return ranked_results

# function to calculate relevance score (replace with actual logic)
def calculate_relevance(result):
    total_assets = result["totalAssets"]
    relevance_score = total_assets / 1000000  #  relevance scoring based on asset value
    return relevance_score

#  function to calculate confidence score (replace with actual logic)
def calculate_confidence(result):
    confidence_score = 1.0 
    return confidence_score

def generate_response(question):
    parsed_question = parse_question(question)
    analyzed_question = analyze_question(parsed_question)
    
    print("Parsed Question:")
    print(parsed_question)
    
    print("\nAnalyzed Question:")
    print(analyzed_question)

    ranked_results = rank_and_retrieve_answers(question)
    return {
        'parsed_question': parsed_question,
        'analyzed_question': analyzed_question,
        'ranked_results': ranked_results
    }
# usage
if __name__ == "__main__":
    # question = "What were the total assets of Mitsubishi UFJ Financial Group in 2017?"
    question = "Which all are banks with assets more than 1000?"
    response = generate_response(question)
    
    if response['ranked_results']:
        print("\n")
        for idx, (result, score) in enumerate(response['ranked_results']):
            print(f"Rank {idx + 1}: Bank Name: {result['bankName']}, Total Assets: {result['totalAssets']}, Score: {score}")
    else:
        print("No results found or unsupported question type.")