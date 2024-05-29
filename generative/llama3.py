import ollama

import sys, os, inspect, time
sys.path.append("..")
import config

class LLama3:
    def __init__(self):
        self.chatbot_role = ""
        self.entity_task = ""
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]
        self.response = None
        self.response_content = None

    def chat(self):
        if self.entity_task:
            self.response = ollama.chat(model='llama3', messages=self.messages)
            self.response_content = self.response['message']['content']
        return self.response_content

    def set_entity_task(self, entity_task):
        self.entity_task = entity_task
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]

    def set_chatbot_role(self, chatbot_role):
        self.chatbot_role = chatbot_role
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]

    def set_messages(self, chatbot_role, entity_task):
        self.chatbot_role = chatbot_role
        self.entity_task = entity_task
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]

    def get_response(self):
        return self.response_content
    
    def get_messages(self):
        return self.messages

    def get_chatbot_role(self):
        return self.chatbot_role

    def get_entity_task(self):
        return self.entity_task

    def llama_chat_get_response(llama, prompt):
        llama.set_chatbot_role("llama3")
        llama.set_entity_task(prompt)
        response = llama.chat()
        return response

def general_simple():
    return "Do the two entity descriptions match?"

def general_complex():
    return "Do the two entity descriptions refer to the same real-world entity?"

def domain_simple(dataset_comparison):
    return f"Do the two {dataset_comparison} descriptions match?"

def domain_complex(dataset_comparison):
    return f"Do the two {dataset_comparison} descriptions refer to the same real-world {dataset_comparison}?"

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
    
def main():
    # return
    
    # Different prompt-techniques
    prompt_techniques = [general_simple]
    
    # 1 for force yes or no response, 0 for not
    extra_correction = [1]
    
    # Different folder and datasets
    folders = [config.STRUCTURED_DIR, config.DIRTY_DIR, config.TEXTUAL_DIR]
    
    datasets = [config.AMAZON_GOOGLE_DIR, config.BEER_DIR, config.DBLP_ACM_DIR, 
                config.DBLP_GOOGLESCHOLAR_DIR, config.FODORS_ZAGATS_DIR, 
                config.ITUNES_AMAZON_DIR, config.WALMART_AMAZON_DIR, config.ABT_BUY_DIR
    ]
    
    save_folder = 'llama3_predictions'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    total_preds = 0
    for folder_name in folders:
        for dataset_name in datasets:
            try:
                train, val, test = config.load_datasets(folder_name, dataset_name)
                total_preds += len(test)
            except:
                print(f"Dataset {folder_name}_{dataset_name} does not exist.")
                continue
    print(f"Total predictions: {total_preds}")
    
    llama3 = LLama3()
    lenght = 0
    for x, folder_name in enumerate(folders):
        for y, dataset_name in enumerate(datasets):
            try:
                csv_name = f"{folder_name}_{dataset_name}"               

                # if not os.path.exists(f"{save_folder}/{csv_name}.csv"):
                #     with open(f"{save_folder}/{csv_name}.csv", 'w') as f:
                #         f.write("general_or_domain,simple_or_complex,force_or_not,tableA_id,tableB_id,pred,label, time\n")

                train, val, test = config.load_datasets(folder_name, dataset_name)
                tableA_df, tableB_df = config.tableA_tableB(folder_name, dataset_name)

                columns = tableA_df.columns
                if 'id' in columns:
                    columns = columns.drop('id')

                tableA, tableB, label = test['ltable_id'], test['rtable_id'], test['label']
                
                for z in range(len(tableA)):
                    idA, idB, single_label = tableA.iloc[z], tableB.iloc[z], label.iloc[z]
                    rowA = tableA_df[tableA_df['id'] == idA].drop(columns='id')
                    rowB = tableB_df[tableB_df['id'] == idB].drop(columns='id')
                    sentenceA = format_columns_string(*columns).format(**rowA.to_dict('records')[0])
                    sentenceB = format_columns_string(*columns).format(**rowB.to_dict('records')[0])

                    for prompt in prompt_techniques:
                        for force in extra_correction:
                            domain = determine_domain(dataset_name) if prompt not in [general_simple, general_complex] else None
                            prompt_sentence = generate_prompt_sentence(sentenceA, sentenceB, force, prompt, domain)
                            lenght += len(prompt_sentence)
                            start = time.time()
                            # print(prompt_sentence)
                            response = llama3.llama_chat_get_response(prompt_sentence)
                            print(response)
                            end = time.time()
                            time_taken = end - start

                            # pred = parse_response(response)
                            simple_or_complex = determine_complexity(prompt)
                            general_or_domain = 'domain' if prompt in [domain_simple, domain_complex] else 'general'
                            yes_or_no = 1 if force else 0

                            # save_predictions(f"{save_folder}/{csv_name}.csv", general_or_domain, simple_or_complex, yes_or_no, idA, idB, pred, single_label, time_taken)
            except:
                print(f"Dataset {folder_name}_{dataset_name} does not exist.")
                continue
    print(f"Total lenght: {lenght} of {total_preds} predictions. Average = {lenght/total_preds}")
    
if __name__ == "__main__":
    main()
    