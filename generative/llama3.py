import ollama

import sys
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


def format_song_string(Song_Name, Artist_Name, Album_Name, Genre, Price, CopyRight, Time, Released):
    string_A = f"Song Name: {Song_Name}, Artist Name: {Artist_Name}, Album Name: {Album_Name}, Genre: {Genre}, Price: {Price}, CopyRight: {CopyRight}, Time: {Time}, Released: {Released}"
    return string_A

def llama_songA_songB(llama, songA, songB):
    llama.set_chatbot_role("Analyse the two songs, and tell me if they are the same song or not. Answer just with 'Yes' or 'No'")
    llama.set_entity_task(f"Song A: {songA} \n Song B: {songB} \n Are these two songs the same?")
    response = llama.chat()
    return response

def domain_simple(dataset_comparison):
    return f"Do the two {dataset_comparison} descriptions match?"

def general_simple():
    return "Do the two entity descriptions match?"

def domain_complex(dataset_comparison):
    return f"Do the two {dataset_comparison} descriptions refer to the same real-world {dataset_comparison}?"

def general_complex():
    return "Do the two entity descriptions refer to the same real-world entity?"

def force_or_not():
    return "Answer with 'Yes' if they do and 'No' if they do not"

def save_predictions(structured_dirty_textual, dataset, domain_general_simple_complex, force_or_not, name='llama3'):
    pass

        
        
        

def process_songs(tableA, tableB, label, tableA_df, tableB_df, llama_model, pred, name=''):
    print(f"\nProcessing songs with {name} model")
    count = 0
    for i, y, x in zip(tableA, tableB, label):
        print(f"{count}/{len(label)}")
        _,Song_Name,Artist_Name,Album_Name,Genre,Price,CopyRight,Time,Released = tableA_df.loc[tableA_df['id'] == i].values[0]
        string_A = format_song_string(Song_Name, Artist_Name, Album_Name, Genre, Price, CopyRight, Time, Released)
        _,Song_Name,Artist_Name,Album_Name,Genre,Price,CopyRight,Time,Released = tableB_df.loc[tableB_df['id'] == y].values[0]
        string_B = format_song_string(Song_Name, Artist_Name, Album_Name, Genre, Price, CopyRight, Time, Released)
        count += 1
        pred.append(llama_songA_songB(llama_model, string_A, string_B))
    return pred

def main():
    llama3 = LLama3()
        
    # Load dataset
    structured_itunes_amazon_data = config.load_datasets(config.STRUCTURED_DIR, config.ITUNES_AMAZON_DIR)
        
    # Train, valid, test
    structured_itunes_amazon_train = structured_itunes_amazon_data[0]
    structured_itunes_amazon_valid = structured_itunes_amazon_data[1]
    structured_itunes_amazon_test = structured_itunes_amazon_data[2]
    tableA_df, tableB_df = config.tableA_tableB(config.STRUCTURED_DIR, config.ITUNES_AMAZON_DIR)
    
    # Different prompt-techniques
    prompt_techniques = [domain_simple, general_simple, domain_complex, general_complex]
    # Force or not
    force_or_not = [True, False]
    
    # list of the different folder and datasets
    
    folders = [config.STRUCTURED_DIR, config.DIRTY_DIR, config.TEXTUAL_DIR]
    
    datasets = [config.AMAZON_GOOGLE_DIR, config.BEER_DIR, config.DBLP_ACM_DIR, 
                config.DBLP_GOOGLESCHOLAR_DIR, config.FODORS_ZAGATS_DIR, 
                config.ITUNES_AMAZON_DIR, config.WALMART_AMAZON_DIR
    ]
    
    for x, folder_name in enumerate(folders):
        for y, dataset_name in enumerate(datasets):
            try:
                train, val, test = config.load_datasets(folder_name, dataset_name)
                print(f"Processing: {folder_name}_{dataset_name}")
                
                tableA, tableB, label = test['ltable_id'], test['rtable_id'], test['label']
            except:
                print(f"Could not load {folder_name}_{dataset_name}")
                continue
                
    
    
    # Five first of structured_itunes_amazon_train
    train = structured_itunes_amazon_train
    tableA, tableB, label = train['ltable_id'], train['rtable_id'], train['label']
    
    pred = []
    process_songs(tableA, tableB, label, tableA_df, tableB_df, llama3, pred, name='llama3')
    sum_label, sum_pred = sum(label), sum([1 if x == 'Yes' else 0 for x in pred])
    print(f"Sum label: {sum_label}, Sum pred: {sum_pred}")
    
    
if __name__ == "__main__":
    main()
    