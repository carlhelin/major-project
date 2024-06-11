# Major Project - Entity Matching with LLM

This project is researching different solutions for Entity Matching, where the purpose is to match different entities that refer to the same real-world data. Three different systems have been tested and evaluated. One benchmark dataset called Magellan has been utilised for both training and performance measures.

## Requirements

- Python 3.8 or higher
- Llama3 model downloaded from Ollama
- API key from Google to run Gemini
- DistilBERT installed from HuggingFace

## Fine-tuned Model Installation

[Link](https://drive.google.com/drive/folders/1ZvDsY_5Ot0U8rd1DjiWkZdLfSVPIiOw-?usp=drive_link)  
Since git only allows 100MB of files, go to the link, download the folder, put the whole folder in the `fine-tune/models/` directory, then you should be able to run the fine-tuned model in `fine-tune/bert_results.ipynb`.

## Installation

All necessary Python packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Usage

Most of the repository consists of notebooks, which makes it convenient to use. Clone the repository and run the provided notebooks, the benchmark data is already in the repository. Some extra steps are required for Llama3 and Gemini.

### Data Scraping

Run the notebooks below and monitor them, as websites are good at bot prevention.  
`scraped data/agi.ipynb`  
`scraped data/coles.ipynb`  
`scraped data/woolworths.ipynb`

### Train / Prompt Models

`fine-tune/bert.ipynb` to train a new fine-tuned model. NB: this takes really long.  
`generative/gemini.ipynb` to prompt Gemini. NB: this requires Google API key.  
`generative/llama3.py` to prompt Llama3. NB: this requires downloaded model.

### Results

`generative_results.ipynb` for creating general results for Gemini and Llama3.  
`fine-tune/bert_results.ipynb` for creating general results on DistilBERT.

`generative/gemini_eval.ipynb` to create specific results for Gemini.  
`generative/llama3_eval.ipynb` to create specific results for Llama3.

## Project Structure

This project has the following directory structure:

- `benchmark data`: Magellan benchmark datasets used for training and performance measures. Three subdirectories:
  - `dirty`: With noisy data.
  - `structured`: Structured data.
  - `textual`: Textual dataset.
- `fine-tune`: Files related to model fine-tuning.
  - `encoded`: Directory for tokenized Magellan dataset.
  - `models`: Trained models, currently empty, need to download and put folder here.
- `generative`: Gemini and Llama3 models.
  - `gemini_predictions`: result of predictions for Gemini.
  - `llama3_predictions`: result of predictions for Llama3.
- `results`: Gemini, Llama3 and DistilBERT results.
- `scraped data`: All scraped data from AGI, Coles, and Woolworths.

Please note that this is a high-level overview. Each directory may contain various other files and subdirectories. Also run of certain notebooks may create new directories/files.

## Authors

- Carl Helin - 2024

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
