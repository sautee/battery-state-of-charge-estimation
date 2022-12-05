# battery-state-of-charge-estimation

By Andrew Chacko, Talha Kamran and Nemesh Weerawarna at Memorial University of Newfoundland, Canada.

_(this repository is still a work in progress)_

The State of Charge (SOC) performs the same function as the fuel gauge in a fossil fuel powered vehicle, indicating how much energy is remaining inside a battery to power a vehicle. Properly measuring SOC is a difficult undertaking since it cannot be measured directly due to non-linear, time-varying properties and electrochemical processes. Moreover, battery SOC is impacted by other factors such as age, temperature variations, charge discharge cycles, and so on. This presentation showcases machine learning to estimate the State of Charge of an LG HG2 18650 lithium-ion cell using publicly available battery test data from McMaster University in Ontario, Canada. Several experiments are run against Deep Neural Networks (DNN), Convolutional Neural Networks (CNN) and Long Short-Term Memory Networks (LSTM). The prediction results from these are then compared to each other.
