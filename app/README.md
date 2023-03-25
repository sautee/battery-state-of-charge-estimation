To get started, 

- Upload a raw CSV file that includes these exact column names among other columns
    - 'Time Stamp'
    - 'Voltage'
    - 'Current'
    - 'Temperature'
    - 'Capacity'
    
Example -
    
| Time Stamp             | Step | Voltage | Current  | Temperature | Capacity    | Cycle       |
|------------------------|------|---------|----------|-------------|-------------|-------------|
| 01/30/2022  2:41:07 PM | 53   | 4.17262 | -0.05108 | 23.97615    | -0.00001    | 1           |
| 01/30/2022  2:41:08 PM | 53   | 4.17178 | -0.09706 | 23.97615    | -0.00001    | 1           |
| 01/30/2022  2:41:09 PM | 53   | 4.16982 | -0.9706  | 23.97521    | -0.00001    | 1           |
    

- Required columns should be measured in V, A, deg.C and Ah
    

- The following pre-processing steps are taken on the uploaded data
    - Normalized using min-max normalization.
    - Resampled to 1Hz. 
    - Average values calculated for Voltage, Current and Power using a hardcoded 500 second window.
    
    
- Once pre-processing is complete, prediction is run using the selected state of charge model.


- To run the same set of data against another model, choose a pre-trained model from the dropdown on the left pane.