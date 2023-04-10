# Battery State of Charge Prediction

Predict battery state of charge (SOC) using machine learning. Use the Streamlit web app easily browse available models and predict SOC on cell dischrage data.

Models are built using Tensorflow and trained on ***[LG 18650HG2](https://data.mendeley.com/datasets/cp3473x7xv/3)*** and ***[Panasonic 18650PF](https://data.mendeley.com/datasets/wykht8y7tg/1)*** Li-ion battery datasets.

## Repository Contents
- `datasets/`: Download datasets and load into this folder as 'LG_18650HG2' and 'Panasonic_18650PF'. 
- `training/`: Jupyter notebooks to analyze and train DNN, CNN, and LSTM models.
- `training/model_evals`: Compare model performance.
- `pre-trained/`: Pre-trained DNN, CNN, and LSTM models.
- `app/`: Streamlit app that allows users to play with their own data using the pre-trained models.

## Convert MAT to CSV
Use the `/training/panasonic/convert_mat_to_csv.ipynb` notebook to convert MAT files to CSV. Useful for the Panasonic dataset where only MAT files are available.

## Usage
To get started
- Clone this repository to your local machine.
- Download datasets, locate them under the 'datasets' folder.
- Convert Panasonic .mat files to .csv.
- Run training notebooks, or use pre-trained models.
- Navigate to `app` folder and run Streamlit app `streamlit run soc_app.py`.
- To deploy to Streamlit Cloud visit [soc-cloud-app](https://github.com/sautee/soc-cloud-app).

## Environment Setup
Using 'pip install'. Run the following command to install requirements.
```
pip install -r requirements.txt
```

Using Anaconda. Create a `battery-soc` environment by running the following command.
```
conda env create -f environment.yml
```

## Contributors
Andrew C, Talha K, Nemesh W, Xili D -- Memorial Univserity of Newfoundland

## Other Research Areas
**Battery Surface Temperature Estimation** - using the [Panasonic 18650PF](https://data.mendeley.com/datasets/wykht8y7tg/1) dataset used here.

M. Naguib, P. Kollmeyer and A. Emadi, "Application of Deep Neural Networks for Lithium Ion 
Battery Surface Temperature Estimation Under Driving and Fast Charge Conditions," IEEE 
Transactions on Transportation Electrification, p. 12, 2022. 

**Predicting Battery Remaining Useful Life** - using data from [TRI](https://data.matr.io/1/projects/5c48dd2bc625d700019f3204), [NASA Prognostics](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository), [UNIBO PowerTools Dataset](https://data.mendeley.com/datasets/n6xg5fzsbv/1).
- [petermattia/predicting-battery-lifetime](https://github.com/petermattia/predicting-battery-lifetime)
- [michaelbosello/battery-rul-estimation](https://github.com/MichaelBosello/battery-rul-estimation)

## Acknowledgements
Kollmeyer, Philip; Vidal, Carlos; Naguib, Mina; Skells, Michael  (2020), “LG 18650HG2 Li-ion Battery Data and Example Deep Neural Network xEV SOC Estimator Script”, Mendeley Data, V3, doi: 10.17632/cp3473x7xv.3

Kollmeyer, Phillip (2018), “Panasonic 18650PF Li-ion Battery Data”, Mendeley Data, V1, doi: 10.17632/wykht8y7tg.1

K. Wong, M. Bosello, R. Tse, C. Falcomer, C. Rossi and G. Pau, "Li-Ion Batteries State-of-Charge 
Estimation Using Deep LSTM at Various Battery Specifications and Discharge Cycles," in 
Conference on Information Technology for Social Good (GoodIT ’21), Roma, Italy, 2021, doi: 10.1145/3462203.3475878

