- Upload a CSV file that includes these ***exact*** column names among other columns
    - **`Time Stamp`**
    - **`Voltage`**
    - **`Current`**
    - **`Temperature`**
    - **`Capacity`**

    
- For best results, values are expected in Voltage(V), Current(A), Temperature(ºC) and Capacity (Ah).

- The 'Capacity' column is optional and only used to compare Predicted SOC with True SOC. 
    
- Once pre-processing is complete, prediction is run using the selected SOC model.
    
- Example file format -
    
| Time Stamp             | Step | Voltage | Current  | Temperature | Capacity    | Cycle       |
|------------------------|------|---------|----------|-------------|-------------|-------------|
| 01/30/2022  2:41:07 PM | 53   | 4.17262 | -0.05108 | 23.97615    | -0.00001    | 1           |
| 01/30/2022  2:41:08 PM | 53   | 4.17178 | -0.09706 | 23.97615    | -0.00001    | 1           |
| 01/30/2022  2:41:09 PM | 53   | 4.16982 | -0.9706  | 23.97521    | -0.00001    | 1           |

- Pre-processing note:
    - All uploaded files are re-sampled to 1Hz.
    - Averages are calculated with a 500 second rolling window.
    - Min-Max normalization is used by default.
    - Rows with null values are dropped.
    
