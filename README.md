# Marketing Campaign Success Prediction

The project aims to train a model to predict the success of a marketing campaign for a bank using tabular data.

## Structure:
- `data/` - contains the dataset (only the results of the test set are provided)
- `notebooks/` - contains the Jupyter notebooks used for the analysis
- `models/` - contains the trained model
- `main.py` - the main script to run the model inference via streamlit app


## How to run the files in the project:
1. Clone the repository
2. Install the required libraries using poetry: `poetry install`
3. For EDA reproducibility, run the notebook in the `notebooks/` folder with adding the dataset in the `data/` folder
4. For inference on new data: run the main.py script to start the streamlit app: 
```poetry run streamlit run main.py```