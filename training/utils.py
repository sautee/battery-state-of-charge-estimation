import os
import pandas as pd
import numpy as np
import pandas as pd
import collections
from datetime import datetime, timedelta

def normalization(dataset, minmax_norm):
    # scale (normalize) the dataset 
    # min max normalization
    if(minmax_norm):
        dataset_norm = (dataset - dataset.min())/(dataset.max() - dataset.min())
    # mean normalization
    else:
        dataset_norm = (dataset - dataset.mean())/dataset.std()
        
    return dataset_norm

def lg_get_files(data_path, drive_cycle_files, charge_cycle_files, temperature, get_discharge_only = True):
    
    # some LSTM training models require discharge cycles only
    if get_discharge_only:
        all_cycles = drive_cycle_files
    else:
        all_cycles = drive_cycle_files + charge_cycle_files

    # iterate thru each temperature folder and get drive cycle and corresponding charge files
    lg_csv_files = []
    folders = os.listdir(data_path)
    for folder in folders:
        d = os.path.join(data_path, folder)
        if os.path.isdir(d):
            for file in os.listdir(d):
                if file.endswith('.csv') and any(substring in file for substring in all_cycles):
                    lg_csv_files.append(data_path +'/'+ folder + '/' + file)
     
    # get the first valid index in each file and add it to the 'files' dictionary
    files = {}
    for csv_file in lg_csv_files:
        if any('/'+ substring in csv_file for substring in temperature):
            df = pd.read_csv(csv_file, header=[25,26], index_col=0, parse_dates=True,nrows=26)
            files[str(df.first_valid_index())] = csv_file
    
    # sort the dictionary by time index
    od = collections.OrderedDict(sorted(files.items()))
    filtered = od.copy()

    # the ordered dictionary can have unnecessary charge files, pop them out 
    # incorrect sequence can have - charge, charge, discharge, charge
    # with this section the file sequence will look like - discharge, charge, discharge..
    if not get_discharge_only:
    
        is_previous_charge = False
        is_previous_discharge = False
    
        for key, value in od.items():
            if not is_previous_discharge and any(substring in value for substring in drive_cycle_files):
                is_previous_discharge = True 
                is_previous_charge = False
            elif not is_previous_charge and any(substring in value for substring in charge_cycle_files):
                if not is_previous_charge and not is_previous_discharge:
                    filtered.pop(key)
                is_previous_charge = True
                is_previous_discharge = False
            elif is_previous_discharge and any(substring in value for substring in drive_cycle_files):
                filtered.pop(key)
            elif is_previous_charge and any(substring in value for substring in charge_cycle_files):
                filtered.pop(key)
            
    return list(filtered.values())

def panasonic_get_files(data_path, drive_cycle_files, temperature, get_trise_tests_only=False):
    
    panasonic_csv_files = []
    
    # Loop through each temperature folder in the data folder
    for temperature_folder in os.listdir(data_path):
        temperature_folder_path = os.path.join(data_path, temperature_folder)
    
        # Loop through each test folder in the temperature folder
        for cycle_test_folder in os.listdir(temperature_folder_path):
            cycle_test_folder_path = os.path.join(temperature_folder_path, cycle_test_folder)
            
            if (os.path.isdir(cycle_test_folder_path) and 
                'drive cycles' in cycle_test_folder_path.lower() and 
                not get_trise_tests_only):
  
                for file in os.listdir(cycle_test_folder_path):
                    if (file.endswith('.csv') and
                        any(substring in file for substring in drive_cycle_files) and
                        any('/'+ substring in temperature_folder_path for substring in temperature)):
                            file_path = os.path.join(cycle_test_folder_path, file)
                            panasonic_csv_files.append(file_path)
    
            # 'Trise' folder
            elif get_trise_tests_only:
                file = cycle_test_folder_path
                if (file.endswith('.csv') and 
                    any(substring in file for substring in drive_cycle_files) and 
                    any('/'+ substring in temperature_folder_path for substring in temperature)):
                        file_path = os.path.join(cycle_test_folder_path, file)
                        panasonic_csv_files.append(file_path)
    
    return list(panasonic_csv_files)

def lg_create_dataset(file_paths, drive_cycle_files, charge_cycle_files, vi_averages = True, resample_1hz = True, minmax_norm = True):

    for path in file_paths:
        cycle = pd.read_csv(path, header=[25,26], index_col=0, parse_dates=True)
        
        print(path + " " + str(cycle.shape[0]))
        
        #drop second row in the header
        cycle.columns = cycle.columns.droplevel(1) 
        
        # calculate SOC Percentage + downsample discharge cycles, upsample charge cycles
        # - DISCHARGE FILES
        if any(substring in path for substring in drive_cycle_files):
            if resample_1hz:
                cycle = cycle.resample('1S').first()
                
            max_discharge = abs(min(cycle['Capacity']))
            cycle['Capacity'] = (cycle['Capacity'] + max_discharge)/max_discharge

        # - CHARGE FILES
        elif any(substring in path for substring in charge_cycle_files):
            if resample_1hz:
                cycle = cycle[~cycle.index.duplicated(keep='first')]
                cycle = cycle.resample('1S').ffill()
                
            max_charge = abs(max(cycle['Capacity']))
            cycle['Capacity'] = (cycle['Capacity'])/max_charge

        # leave out 'PAU' rows from the cycle
        options = ['CHA', 'DCH', 'TABLE']
        cycle = cycle[cycle['Status'].isin(options)]

        # calculate 'Power'
        cycle['Power'] = cycle['Voltage'] * cycle['Current']

        # select required features
        parameters = cycle[['Voltage', 'Current', 'Temperature', 'Power', 'Capacity']].copy()

        # calculate 'Voltage', 'Current' and 'Power' averages
        # 500 second rolling window which translates to rougly 500 data points for resampled data and 5000 for raw data
        rolling_window = 5000
        if vi_averages and resample_1hz:
            rolling_window = int(rolling_window / 10)

        if vi_averages:
            parameters['Voltage Average'] = parameters['Voltage'].rolling(rolling_window).mean()
            parameters['Current Average'] = parameters['Current'].rolling(rolling_window).mean()
            parameters['Power Average'] = parameters['Power'].rolling(rolling_window).mean()
        
        # drop rows with NaN or empty values in them, reset the index to reflect
        parameters.dropna(inplace=True)
        parameters.reset_index(drop=True, inplace=True)
        
        # merge datasets
        try:
            merged = pd.concat([merged, parameters], ignore_index=True)
        except:
            merged = parameters.copy()
        
    merged_norm = normalization(merged, minmax_norm)
        
    return merged, merged_norm

def panasonic_create_dataset(file_paths, drive_cycle_files, vi_averages = True, resample_1hz = True, minmax_norm = True):

    for path in file_paths:
        cycle = pd.read_csv(path, index_col=0, parse_dates=True)
        
        print(path + " " + str(cycle.shape[0]))
        
        cycle.rename(columns={"Battery_Temp_degC":"Temperature", "Ah":"Capacity"}, inplace=True)
        
        if resample_1hz:
            cycle = cycle.resample('1S').first()
                
        # Discharge cycles have capcity values <= 0
        # Charge cycles have capcity values > 0
        cycle = cycle[(cycle['Capacity'] <= 0)]
        
         # calculate SOC Percentage + downsample discharge cycles, upsample charge cycles
        # - DISCHARGE FILES
        max_discharge = abs(min(cycle['Capacity']))
        cycle['Capacity'] = (cycle['Capacity'] + max_discharge)/max_discharge
        
        # calculate 'Power'
        cycle['Power'] = cycle['Voltage'] * cycle['Current']

        # select required features
        parameters = cycle[['Voltage', 'Current', 'Temperature', 'Power', 'Capacity']].copy()

        # calculate 'Voltage', 'Current' and 'Power' averages
        # 500 second rolling window which translates to rougly 500 data points for resampled data and 5000 for raw data
        rolling_window = 5000
        if vi_averages and resample_1hz:
            rolling_window = int(rolling_window / 10)

        if vi_averages:
            parameters['Voltage Average'] = parameters['Voltage'].rolling(rolling_window).mean()
            parameters['Current Average'] = parameters['Current'].rolling(rolling_window).mean()
            parameters['Power Average'] = parameters['Power'].rolling(rolling_window).mean()
        
        # drop rows with NaN or empty values in them, reset the index to reflect
        parameters.dropna(inplace=True)
        parameters.reset_index(drop=True, inplace=True)
        
        # merge datasets
        try:
            merged = pd.concat([merged, parameters], ignore_index=True)
        except:
            merged = parameters.copy()
            
    merged_norm = normalization(merged, minmax_norm)
        
    return merged, merged_norm

def app_create_dataset(path, vi_averages = True, resample_1hz = True, minmax_norm = True):
    
    cycle = pd.read_csv(path, index_col=0, parse_dates=True)
    
    if resample_1hz:
        cycle = cycle.resample('1S').first()
    
    # calculate 'Power'
    cycle['Power'] = cycle['Voltage'] * cycle['Current']
    
    if 'Capacity' in cycle:
        parameters = cycle[['Voltage', 'Current', 'Temperature', 'Power', 'Capacity']].copy()

    else:
        parameters = cycle[['Voltage', 'Current', 'Temperature', 'Power']].copy()

    # calculate 'Voltage', 'Current' and 'Power' averages
    # 500 second rolling window which translates to rougly 500 data points for resampled data and 5000 for raw data
    rolling_window = 5000
    if vi_averages and resample_1hz:
        rolling_window = int(rolling_window / 10)

    if vi_averages:
        parameters['Voltage Average'] = parameters['Voltage'].rolling(rolling_window).mean()
        parameters['Current Average'] = parameters['Current'].rolling(rolling_window).mean()
        parameters['Power Average'] = parameters['Power'].rolling(rolling_window).mean()
        
    # drop rows with NaN or empty values in them, reset the index to reflect
    parameters.dropna(inplace=True)
    parameters.reset_index(drop=True, inplace=True)
            
    parameters_norm = normalization(parameters, minmax_norm)
        
    return parameters, parameters_norm

# create_lstm_dataset - https://github.com/KeiLongW/battery-state-estimation
def create_lstm_dataset(dataset, steps):
    dataset.drop(['Power', 'Power Average'], axis=1, inplace=True)
    train_y = dataset.pop('Capacity').to_numpy()
    train_y = train_y.reshape(len(train_y),1)
    train_x = dataset.to_numpy()
    
    x_length = len(train_x[0])
    y_length = len(train_y[0])
    x = np.empty((0, steps, x_length), float)
    y = np.empty((0, steps, y_length), float)
    
    number_subsequences = int(len(train_x)/steps)
    
    for i in range(0, number_subsequences*steps, steps):
        next_x = np.array(train_x[i:i + steps]).reshape(1, steps, x_length)
        next_y = np.array(train_y[i:i + steps]).reshape(1, steps, y_length)
        x = np.concatenate((x, next_x))
        y = np.concatenate((y, next_y))
        
    return x, y

# keep_only_y_end - https://github.com/KeiLongW/battery-state-estimation
def keep_only_y_end(y, step):
    return y[:,::step]
            
            

