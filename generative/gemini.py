import gemini
import pandas as pd
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

import sys, os
sys.path.append("..")
import config

def product_info(table):
    return table['name'], table['description'], table['price']

def generate_prompt(table_a_id, table_b_id, label, a_df, b_df, gemini_model, name=''):
    name_a, desc_a, price_a = product_info(a_df.loc[table_a_id])
    name_b, desc_b, price_b = product_info(b_df.loc[table_b_id])
    
    # Prompt gemini
    prompt = f"""Given the following information about two products:
    
                Product A:
                            Name: {name_a}
                            Description: {desc_a}
                            Price: {price_a}
                Product B:
                            Name: {name_b}
                            Description: {desc_b}
                            Price: {price_b}
                            
                Are these products the same? Answer yes or no."""
    return prompt

def main():
    # Used to securely store the API key
    api_key = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=api_key)
    
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

    model = genai.GenerativeModel('gemini-pro')
    
    textual_abt_buy = config.load_datasets(config.TEXTUAL_DIR, config.ABT_BUY_DIR)
    tableA_df, tableB_df = config.tableA_tableB(config.TEXTUAL_DIR, config.ABT_BUY_DIR)
    
    textual_abt_buy_train = textual_abt_buy[0]
    textual_abt_buy_valid = textual_abt_buy[1]
    textual_abt_buy_test = textual_abt_buy[2]
    
    # Get two matches from the training set
    match1 = textual_abt_buy_train.groupby('label').get_group(1).iloc[0]
    match2 = textual_abt_buy_train.groupby('label').get_group(1).iloc[1]
    match3 = textual_abt_buy_train.groupby('label').get_group(1).iloc[2]
    
    # Get three non-matches from the training set
    non_match1 = textual_abt_buy_train.groupby('label').get_group(0).iloc[0]
    non_match2 = textual_abt_buy_train.groupby('label').get_group(0).iloc[1]
    non_match3 = textual_abt_buy_train.groupby('label').get_group(0).iloc[2]
    
    list = [match1, match2, match3, non_match1, non_match2, non_match3]
    labels = [i['label'] for i in list]
    
    print(f"\nLabels: {labels}")
    
    for i in list:
        l_table, r_table, label = i['ltable_id'], i['rtable_id'], i['label']
        prompt = generate_prompt(l_table, r_table, label, tableA_df, tableB_df, model)
    
        response = model.generate_content(prompt)
        
        for chunk in response:
            print(chunk.text)
            print("_"*80)
        

if __name__ == "__main__":
    main()