# Major Project - Entity Matching with LLM

This project is researching different solutions for Entity Matching, where the porpuse is to match different entities that refer to the same real world data. Three different systems has been tested and evaluated. One benchmark dataset called Magellan has been utilised for both training and performance measures.

## Requirements

- Python 3.8 or higher
- pip for package installation
- Llama3 model downloaded from Ollama
- API key from Google to run Gemini
- DistilBERT installation from HuggingFace

## Install fine-tuned model from link

Since git only allows 100MB of files, go to the link below and put the files in the `fine-tune/models/` directory, then you should be able to run the fine-tuned model.

## Installation

Packages are listed below.

```bash
pip install pandas
pip install numpy
pip install transformers
pip install selenium
pip install webdriver_manager
pip install fake_useragent
pip install bs4
pip install pathlib
pip install torch
pip install ollama
```

## Usage

Most of the repository uses notebooks which makes it convinient to use. Clone the repository and run the notebooks provided, the benchmark data is in the repository already. Some extra steps are required for Llama3 and Gemini.

### Data Scraping

Run notebooks below and monitor since websites are good at bot-prevention.  
`scraped data/agi.ipynb`  
`scraped data/coles.ipynb`  
`scraped data/woolworths.ipynb`.

### Train / Prompt models

`fine-tune/bert.ipynb` to train a new fine-tuned model.  
`generative/gemini.ipynb` to prompt Gemini.  
`generative/llama3.py` to prompt Llama3.

### Results

`fine-tune/bert_results.ipynb` for creating results on the test data.  
`generative/gemini_eval.ipynb` to create specific results for Gemini.  
`generative/llama3_eval.ipynb` to create specific results for Llama3.

## Project Structure

This project has the following directory structure:

- `benchmark data`: Magellan benchmark datasets used for training and performance measures. Three subdirectories:
  - `dirty`: With noisy data.
  - `structured`: Structured data.
  - `textual`: Textual dataset.
- `fine-tune`: Files related to model fine-tuning.
  - `encoded`: Directory for encoded files.
  - `models`: Trained models.
- `generative`: Gemini and Llama3 models.
  - `gemini_predictions`: predictions for Gemini.
  - `llama3_predictions`: predictions for Llama3.
- `results`: Gemini, Llama3 and DistilBERT resutls.
- `scraped data`: all scraped data from AGI, Coles, and Woolworths.

Please note that this is a high-level overview. Each directory may contain various other files and subdirectories.

## Authors

- Carl Helin - 2024

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
