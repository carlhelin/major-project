import sys, inspect
sys.path.append("..")
import config

def general_simple():
    return "Do the two entity descriptions match?"

def general_complex():
    return "Do the two entity descriptions refer to the same real-world entity?"

def domain_simple(dataset_comparison):
    return f"Do the two {dataset_comparison} descriptions match?"

def domain_complex(dataset_comparison):
    return f"Do the two {dataset_comparison} descriptions refer to the same real-world {dataset_comparison}s?"

def force_or_not():
    return "Answer with 'Yes' if they do and 'No' if they do not."

def save_predictions(filepath, general_or_domain, simple_or_complex, force_or_not, tableA_id, tableB_id, pred, label, time_taken):
    with open(filepath, 'a') as f:
        f.write(f"{general_or_domain},{simple_or_complex},{force_or_not},{tableA_id},{tableB_id},{pred},{label},{time_taken}\n")

def format_columns_string(*columns):
    formatted_columns = ', '.join([f'{column}: {{{column}}}' for column in columns])
    string_A = f"{formatted_columns}"
    return string_A

def determine_domain(dataset_name):
    if dataset_name in [config.DBLP_ACM_DIR, config.DBLP_GOOGLESCHOLAR_DIR]:
        return 'book'
    elif dataset_name == config.ITUNES_AMAZON_DIR:
        return 'song'
    elif dataset_name in [config.WALMART_AMAZON_DIR, config.AMAZON_GOOGLE_DIR, config.ABT_BUY_DIR]:
        return 'product'
    elif dataset_name == config.BEER_DIR:
        return 'beer'
    elif dataset_name == config.FODORS_ZAGATS_DIR:
        return 'resturant'
    else:
        return None

def generate_prompt_sentence(sentenceA, sentenceB, force, prompt, domain=None):
    # Check if prompt takes an argument
    takes_argument = len(inspect.signature(prompt).parameters) > 0

    if force:
        prompt_text = prompt(domain) if takes_argument else prompt()
        return f"{sentenceA}\n{sentenceB}\n{force_or_not()} {prompt_text}"
    else:
        prompt_text = prompt(domain) if takes_argument else prompt()
        return f"{sentenceA}\n{sentenceB}\n{prompt_text}"

def determine_complexity(prompt):
    return 'simple' if prompt == domain_simple or prompt == general_simple else 'complex'

def parse_response(response):
    # Method that checks for yes or no in the response and returns the label
    if 'yes' in response.lower():
        return 1
    elif 'no' in response.lower():
        return 0
    else:
        return -1