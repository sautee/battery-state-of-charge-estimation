import functools
from pathlib import Path
import os

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import os 


saved_models = '../pre-trained/'

def list_saved_models(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f
                 
def load_model(model_path):
    model_path = os.path.join(saved_models, model_path)
    model = tf.keras.models.load_model(model_path)
    return model
            
def create_dataset(cycle, vi_averages = True, resample_1hz = True): 
    cycle = cycle[['Voltage', 'Current', 'Temperature', 'Capacity']]
    
    # calculate 'Power'
    cycle['Power'] = cycle['Voltage'] * cycle['Current']
    
    # resample to 1Hz
    if resample_1hz:
        cycle = cycle.resample('1S').first()
    
    # calculate 'Voltage', 'Current' and 'Power' averages
    # 500 second rolling window which translates to rougly 500 data points
    rolling_window = 500
    
    if vi_averages:
        cycle['Voltage Average'] = cycle['Voltage'].rolling(rolling_window).mean()
        cycle['Current Average'] = cycle['Current'].rolling(rolling_window).mean()
        cycle['Power Average'] = cycle['Power'].rolling(rolling_window).mean()
        
    # drop rows with NaN or empty values in them, reset the index to reflect
    cycle.dropna(inplace=True)
    cycle.reset_index(drop=True, inplace=True)
    
    # scale (normalize) the dataset using mean normalization
    # merged_norm = (merged-merged.mean())/merged.std()
    # min-max normalization
    cycle_norm = (cycle - cycle.min())/(cycle.max() - cycle.min())
    return cycle_norm

def main() -> None:
    st.header("Battery State of Charge :battery: :bar_chart:")

    with st.expander("How to Use This Application"):
        st.write(Path("README.md").read_text())

    st.subheader("Upload your CSV file")
    uploaded_data = st.file_uploader(
        "Drag and Drop or Click to Upload", type=".csv", accept_multiple_files=False
    )

    if uploaded_data is None:
        st.info("Using example data. Upload a file above to use your own data!")
        uploaded_data = open("example_file.csv", "r")
    else:
        st.success("Uploaded your file!")
        
    st.sidebar.subheader("Choose ML model")
    selected_model = st.sidebar.selectbox("Select model to use", list_saved_models(saved_models))

    df = pd.read_csv(uploaded_data, index_col=0, parse_dates=True)
    with st.expander("Explore Raw Data"):
        st.markdown("### Chart")
        fig, axes = plt.subplots(4)
        df['Voltage'][:100000].plot(ax=axes[0], color='blue'); axes[0].legend(loc='best'); axes[0].get_xaxis().set_visible(False);
        df['Current'][:100000].plot(ax=axes[1], color='orange'); axes[1].legend(loc='best'); axes[1].get_xaxis().set_visible(False);
        df['Temperature'][:100000].plot(ax=axes[2], color='green'); axes[2].legend(loc='best'); axes[2].get_xaxis().set_visible(False);
        df['Capacity'][:100000].plot(ax=axes[3], color='red'); axes[3].legend(loc='best')
        st.pyplot(fig)
        st.markdown("### Statistics")
        st.write(df.describe().transpose())
        st.markdown("### Data (500 rows)")
        st.write(df[:500])
    
    df = create_dataset(df)
    with st.expander("Explore Noramlized Data"):
        st.markdown("### Chart")
        fig, axes = plt.subplots(6)
        df['Voltage'].plot(ax=axes[0], color='blue'); axes[0].legend(loc='best'); axes[0].get_xaxis().set_visible(False);
        df['Current'].plot(ax=axes[1], color='orange'); axes[1].legend(loc='best'); axes[1].get_xaxis().set_visible(False);
        df['Voltage Average'].plot(ax=axes[2], color='blue'); axes[2].legend(loc='best'); axes[2].get_xaxis().set_visible(False);
        df['Current Average'].plot(ax=axes[3], color='orange'); axes[3].legend(loc='best'); axes[3].get_xaxis().set_visible(False);
        df['Temperature'].plot(ax=axes[4], color='green'); axes[4].legend(loc='best'); axes[4].get_xaxis().set_visible(False);
        df['Capacity'].plot(ax=axes[5], color='red'); axes[5].legend(loc='best')
        st.pyplot(fig)
        st.markdown("### Statistics")
        st.write(df.describe().transpose())
        st.markdown("### Data (500 rows)")
        st.write(df[:500])
        
    st.subheader("Evaluating '{}' with model '{}'".format(uploaded_data.name, selected_model))
    
    with st.spinner("Running Prediction"):
        test_features = df.copy()
        test_labels = test_features.pop('Capacity')
    
        selected_model = load_model(selected_model)
        model_evaluation = selected_model.evaluate(test_features, test_labels, verbose=2)
        model_metrics = {'Metric':selected_model.metrics_names,'Result':model_evaluation}
        st.table(pd.DataFrame(model_metrics).transpose())
    
        test_predictions = selected_model.predict(test_features).flatten()
        fig.suptitle('Model Prediction Results')
    
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.scatter(test_labels, test_predictions)
        ax1.set_xlabel('True SOC'); ax1.set_ylabel('Predicted SOC')
        ax1.set_xlim([0, 1.7]); ax1.set_ylim([0, 1.7])
    
        ax2.plot(test_predictions[:100000], label='Predicted SOC')
        ax2.plot(test_labels[:100000], label='True SOC')
        ax2.set_xlabel('Steps'); ax2.set_ylabel('SOC')
        ax2.legend(loc='best')
        fig.tight_layout(pad=2.0)
        st.pyplot(fig)
                    
                    
  
if __name__ == "__main__":
    st.set_page_config(
        "990B ML App",
        "🔋",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()