import os, sys, torch
from torch.utils.data import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Append the configuration path
sys.path.append("..")
import config

class CustomDataset(Dataset):
    def __init__(self, data, size=None):
        self.data = data
        self.size = size if size is not None else len(self.data[list(self.data.keys())[0]])

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.data.items()}
        return item

    def __len__(self):
        return self.size

def count_training_samples(folders, datasets):
    total_preds = 0
    for folder_name in folders:
        for dataset_name in datasets:
            try:
                train, _, _ = config.load_datasets(folder_name, dataset_name)
                total_preds += len(train)
            except:
                print(f"Dataset {folder_name}_{dataset_name} does not exist")
                continue
    print(f"Total training samples: {total_preds}\n")
    return total_preds

def create_dataset_dict(tableA_df, tableB_df, ltable_id, rtable_id, label):
    return {
        "tableA_df": tableA_df, 
        "tableB_df": tableB_df, 
        "ltable_id": ltable_id, 
        "rtable_id": rtable_id, 
        "label": label
    }

def load_and_prepare_datasets(folders, datasets):
    all_datasets = {}
    for folder_name in folders:
        for dataset_name in datasets:
            try:
                train, val, test = config.load_datasets(folder_name, dataset_name)
                tableA_df, tableB_df = config.tableA_tableB(folder_name, dataset_name)
                the_dataset = f"{folder_name}_{dataset_name}"

                all_datasets[f"{the_dataset}_train"] = create_dataset_dict(
                    tableA_df, tableB_df, train['ltable_id'], train['rtable_id'], train['label']
                )
                all_datasets[f"{the_dataset}_val"] = create_dataset_dict(
                    tableA_df, tableB_df, val['ltable_id'], val['rtable_id'], val['label']
                )
                all_datasets[f"{the_dataset}_test"] = create_dataset_dict(
                    tableA_df, tableB_df, test['ltable_id'], test['rtable_id'], test['label']
                )
            except:
                print(f"Dataset {folder_name}_{dataset_name} does not exist")
                continue
    return all_datasets

def preprocess_function(dataset, tokenizer):
    tokenized_inputs = []
    labels = []
    total_count_0 = sum(label == 0 for label in dataset['label'])
    total_count_1 = sum(label == 1 for label in dataset['label'])
    count_0, count_1 = 0, 0
    for l_id, r_id, label in zip(dataset['ltable_id'], dataset['rtable_id'], dataset['label']):
        # If the label is 0 (majority class) and we have already added enough samples of this class, skip this sample
        if label == 0 and count_0 >= total_count_1:
            continue
        entity1 = dataset['tableA_df'].loc[l_id].drop('id')
        entity2 = dataset['tableB_df'].loc[r_id].drop('id')
        entity1 = ' '.join(f'{col}: {val}' for col, val in entity1.items())
        entity2 = ' '.join(f'{col}: {val}' for col, val in entity2.items())
        tokenized_inputs.append(tokenizer(entity1, entity2, truncation=True, padding='max_length', max_length=512))
        labels.append(torch.tensor(label))
        # Update the counts
        if label == 0:
            count_0 += 1
        else:
            count_1 += 1
    return {
        'input_ids': [ti['input_ids'] for ti in tokenized_inputs],
        'attention_mask': [ti['attention_mask'] for ti in tokenized_inputs],
        'labels': labels
    }

def load_encoded_datasets(encoded_dir, all_datasets):
    loaded_datasets = {}
    for dataset_name in all_datasets.keys():
        try:
            loaded_datasets[dataset_name] = torch.load(os.path.join(encoded_dir, f"{dataset_name}.pt"))
        except Exception as e:
            print(f"Failed to load dataset {dataset_name}")
    return loaded_datasets

def combine_datasets(loaded_datasets, suffix):
    combined_data = {key: [] for key in loaded_datasets[list(loaded_datasets.keys())[0]].data.keys()}
    for dataset_name, dataset in loaded_datasets.items():
        if dataset_name.endswith(suffix):
            for key in combined_data.keys():
                combined_data[key].extend(dataset.data[key])
    return CustomDataset(combined_data)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }
    
# Load configuration
folders = [config.STRUCTURED_DIR, config.TEXTUAL_DIR, config.DIRTY_DIR]
datasets = [
    config.DBLP_ACM_DIR, config.ABT_BUY_DIR, config.AMAZON_GOOGLE_DIR,
    config.WALMART_AMAZON_DIR, config.DBLP_GOOGLESCHOLAR_DIR,
    config.FODORS_ZAGATS_DIR, config.BEER_DIR, config.ITUNES_AMAZON_DIR
]

all_datasets = load_and_prepare_datasets(folders, datasets)