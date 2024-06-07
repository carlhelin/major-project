from transformers import BertForSequenceClassification, BertTokenizer

# Specify the directory where the model is saved
model_dir = 'models/combined_100_18:36:29'

# Load the model
model = BertForSequenceClassification.from_pretrained(model_dir, device_map='cpu')
tokenizer = BertTokenizer.from_pretrained(model_dir)