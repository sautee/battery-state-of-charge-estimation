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
- Run Streamlit app `streamlit run soc_app.py`.

## Environment Setup
Recommend using Anaconda. Create a `battery-soc` environment by running the following command.
````
conda env create -f environment.yml
````

## Acknowledgements
### Datasets
Kollmeyer, Philip; Vidal, Carlos; Naguib, Mina; Skells, Michael  (2020), “LG 18650HG2 Li-ion Battery Data and Example Deep Neural Network xEV SOC Estimator Script”, Mendeley Data, V3, doi: 10.17632/cp3473x7xv.3

Kollmeyer, Phillip (2018), “Panasonic 18650PF Li-ion Battery Data”, Mendeley Data, V1, doi: 10.17632/wykht8y7tg.1

### LSTM model architecture, dataset preparation
*Li-Ion Batteries State-of-Charge Estimation Using Deep LSTM at Various Battery Specifications and Discharge Cycles* [[DOI](https://doi.org/10.1145/3462203.3475878)]

```
@inproceedings{10.1145/3462203.3475878,
author = {Wong, Kei Long and Bosello, Michael and Tse, Rita and Falcomer, Carlo and Rossi, Claudio and Pau, Giovanni},
title = {Li-Ion Batteries State-of-Charge Estimation Using Deep LSTM at Various Battery Specifications and Discharge Cycles},
year = {2021},
isbn = {9781450384780},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3462203.3475878},
doi = {10.1145/3462203.3475878},
booktitle = {Proceedings of the Conference on Information Technology for Social Good},
pages = {85–90},
numpages = {6},
location = {Roma, Italy},
series = {GoodIT '21}
}
```

