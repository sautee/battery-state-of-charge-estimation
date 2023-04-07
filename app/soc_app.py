import os
import sys
import functools
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from sidebar_intro import text as side_intro
from sidebar_body import text as side_body
 

base_path = '../'

sys.path.append(base_path)
from training import utils

saved_models_path = base_path + 'pre-trained/'
example_files_path = 'examples'
columns_capacity = ['Voltage', 'Current', 'Voltage Average', 'Current Average', 'Temperature', 'Capacity']
columns = ['Voltage', 'Current', 'Voltage Average', 'Current Average', 'Temperature']
lstm_steps =300

def list_saved_models(path):
    for models in os.listdir(path):
        if not models.startswith('.') and models.startswith('comb'):
            yield models

def list_example_files(path):
    for examples in os.listdir(path):
        if not examples.startswith('.'):
            yield examples
                 
def load_model(model_path):
    model_path = os.path.join(saved_models_path, model_path)
    model = tf.keras.models.load_model(model_path)
    return model

def main() -> None:
    st.header("Predict Battery State of Charge :battery: :bar_chart:")
    
    st.sidebar.markdown(side_intro, unsafe_allow_html=True)
    st.sidebar.subheader(":gear: App Options")
    selected_model = st.sidebar.selectbox("Select pre-trained model", list_saved_models(saved_models_path))
    example_file = st.sidebar.selectbox("Select example file", list_example_files(example_files_path))
    example_file = os.path.join(example_files_path, example_file)
    st.sidebar.markdown(side_body, unsafe_allow_html=True)
    
    resample_1hz = True
    vi_averages = True
    
    is_lstm = False
    if 'lstm' in selected_model:
        is_lstm = True
        resample_1Hz = False

    with st.expander("Getting Started"):
        st.write(Path("getstarted.md").read_text())

    st.subheader("Upload cell discharge cycle CSV file")
    uploaded_data = st.file_uploader(
        "Drag and Drop or Click to Upload", type=".csv", accept_multiple_files=False
    )

    if uploaded_data is None:
        uploaded_data = example_file
        st.info("Using example '{}'. Upload a file above to use your own data".format(uploaded_data))
    else:
        st.success("Uploaded your file!")

    dataset, dataset_norm = utils.app_create_dataset(uploaded_data, vi_averages, resample_1hz)
    
    capacity_available = False
    if 'Capacity' in dataset_norm:
        capacity_available = True
    
    if dataset.empty:
        st.error('Could not read file {}!'.format(uploaded_data), icon="🚨")
        st.stop()
    
    with st.expander("Explore Processed Data"):
        st.markdown("### Chart")
        fig, axes = plt.subplots(5)
        dataset['Voltage'][:100000].plot(ax=axes[0], color='blue'); axes[0].legend(loc='best'); axes[0].get_xaxis().set_visible(False);
        dataset['Current'][:100000].plot(ax=axes[1], color='orange'); axes[1].legend(loc='best'); axes[1].get_xaxis().set_visible(False);
        dataset['Voltage Average'].plot(ax=axes[2], color='blue'); axes[2].legend(loc='best'); axes[2].get_xaxis().set_visible(False);
        dataset['Current Average'].plot(ax=axes[3], color='orange'); axes[3].legend(loc='best'); axes[3].get_xaxis().set_visible(False);
        dataset['Temperature'][:100000].plot(ax=axes[4], color='green'); axes[2].legend(loc='best'); axes[2].get_xaxis().set_visible(False);
        st.pyplot(fig)
        st.markdown("### Statistics")
        st.write(dataset.describe().transpose())

    with st.expander("Explore Noramlized Data"):
        st.markdown("### Chart")
        fig, axes = plt.subplots(5)
        dataset_norm['Voltage'].plot(ax=axes[0], color='blue'); axes[0].legend(loc='best'); axes[0].get_xaxis().set_visible(False);
        dataset_norm['Current'].plot(ax=axes[1], color='orange'); axes[1].legend(loc='best'); axes[1].get_xaxis().set_visible(False);
        dataset_norm['Voltage Average'].plot(ax=axes[2], color='blue'); axes[2].legend(loc='best'); axes[2].get_xaxis().set_visible(False);
        dataset_norm['Current Average'].plot(ax=axes[3], color='orange'); axes[3].legend(loc='best'); axes[3].get_xaxis().set_visible(False);
        dataset_norm['Temperature'].plot(ax=axes[4], color='green'); axes[4].legend(loc='best'); axes[4].get_xaxis().set_visible(False);
        st.pyplot(fig)
        st.markdown("### Statistics")
        st.write(dataset_norm.describe().transpose())
    
    try:
        st.subheader("Evaluating '{}' with model '{}'".format(uploaded_data.name, selected_model))
    except:
        st.subheader("Evaluating '{}' with model '{}'".format(uploaded_data, selected_model))
    
    with st.spinner("Running Prediction.."):
        if capacity_available:
            if is_lstm:
                test_features, test_labels = utils.create_lstm_dataset(dataset_norm, lstm_steps)
                test_labels = utils.keep_only_y_end(test_labels, lstm_steps)
            else:
                test_features = dataset_norm[columns_capacity].copy()
                test_labels = test_features.pop('Capacity')
            
            selected_model = load_model(selected_model)
            model_evaluation = selected_model.evaluate(test_features, test_labels, verbose=2)
            model_metrics = {'Metric':selected_model.metrics_names,'Result':model_evaluation}
            st.table(pd.DataFrame(model_metrics).transpose())
            
            test_predictions = selected_model.predict(test_features).flatten()
            
            if is_lstm:
                test_labels = test_labels.flatten()
                
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
        else:
            if is_lstm:
                test_features, test_labels = utils.create_lstm_dataset(dataset_norm, lstm_steps)
            else:
                test_features = dataset_norm[columns].copy()
            
            selected_model = load_model(selected_model)
            test_predictions = selected_model.predict(test_features).flatten()
            
            fig, ax = plt.subplots()
            fig.suptitle('Model Prediction Results')
            ax.plot(test_predictions[:100000], label='Predicted SOC')
            ax.set_xlabel('Steps'); ax.set_ylabel('SOC')
            ax.legend(loc='best')
            st.pyplot(fig)
            
if __name__ == "__main__":
    st.set_page_config(
        "SOC ML App",
        "🔋",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()