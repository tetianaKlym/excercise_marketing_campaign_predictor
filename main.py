import streamlit as st
import pandas as pd
import pickle
from io import BytesIO
from pathlib import Path

MODELS_DIR = Path("models")

# Page config
st.set_page_config(page_title="Marketing Predictor", layout="wide")


# Load the pre-trained model
@st.cache_resource
def load_model():
    with open(MODELS_DIR / 'model.pkl', 'rb') as file:
        return pickle.load(file)


def check_columns(df):
    categorical_features = ['job', 'marital', 'education', 'contact', 'month', 'day_of_week', 'previous', 'default',
                            'poutcome']
    numerical_features = ['age']
    if not all(col in df.columns for col in categorical_features):
        return False, f"Missing one or more of the required columns: {categorical_features}"
    if not all(col in df.columns for col in numerical_features):
        return False, f"Missing one or more of the required columns: {numerical_features}"
    return True, None


def format_data(df: pd.DataFrame):
    categorical_features = ['job', 'marital', 'education', 'contact', 'month', 'day_of_week', 'previous', 'default',
                            'poutcome']
    numerical_features = ['age']
    return df[categorical_features + numerical_features]


def run_inference(model, df: pd.DataFrame):
    return model.predict(df)


model = load_model()

# App title and description
st.title('Marketing Outcomes Predictor')

if st.button("New Session"):
    st.session_state.clear()
    st.rerun()

st.write('Upload your Excel file to predict marketing outcomes')

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df.head())

        is_valid, error_message = check_columns(df)
        if not is_valid:
            st.error(error_message)
            st.stop()

        predictions = run_inference(model, format_data(df))

        results_df = df.copy()
        results_df['Predicted_Outcome'] = predictions

        st.write("Results Preview:")
        st.dataframe(results_df.head())

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            results_df.to_excel(writer, index=False)
            workbook = writer.book
            for worksheet in workbook.worksheets:
                worksheet.protection.enabled = False
            workbook.properties.lastModifiedBy = 'Marketing Predictor'

        st.download_button(
            label="Download Results",
            data=buffer.getvalue(),
            file_name="marketing_predictions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")