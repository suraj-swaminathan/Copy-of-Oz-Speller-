# Oz-Speller: A Fast Occipital Channel-Driven Steady-State Visual Evoked Potential-Based Virtual Keyboard

## _**1.2**_-second classification, 85% accuracy, 32 classes
This is the **ultimate EEG spelling machine** combined with a companion app that uses a **GPT-based language model** for locked-in patients to better communicate with their caretakers. All that speed is right in front of your retina, made more available than ever. Only a few lines in the command line, and you have it.</br>

![GIF DEMO](./reports/figures/speller.gif)

## Presentation Video 

</br>

[![PRESENTATION VIDEO](https://img.youtube.com/vi/-5eUUtTdpno/0.jpg)](https://www.youtube.com/watch?v=-5eUUtTdpno)

</br>

---

## Getting Started
- Run `pip install -r requirements.txt` to install the dependencies.
- In [`/scripts`](https://github.com/NeuroTech-UCSD/Project-Template/tree/main/scripts), `python main.py` will run the app.
- Upload the entire project folder to Google drive, and open the .ipynb files in Colab to run the demo notebooks.

## Github Directories
<!-- ![](./figures/github_schema.png) -->
- [`/data`](https://github.com/NeuroTech-UCSD/Project-Template/tree/main/data) - Where the recorded eeg data, intermediate variables, and analysis results for plotting the figures will be stored. 
	- [`/data/eeg_recordings`](https://github.com/NeuroTech-UCSD/Project-Template/tree/main/data/eeg_recordings) - Contains different sessions of EEG recordings.
- [`/figures`](https://github.com/NeuroTech-UCSD/Project-Template/tree/main/figures) Stores all of the figures generated by the scripts. 
- [`/notebooks`](https://github.com/NeuroTech-UCSD/Project-Template/tree/main/notebooks) Demo notebooks illustrating the data processing and modeling pipeline. 
- [`/scripts`](https://github.com/NeuroTech-UCSD/Project-Template/tree/main/scripts) Each script is for a particular processing stage.
	- [`/scripts/main.py`](https://github.com/NeuroTech-UCSD/Project-Template/blob/main/scripts/main.py) - The scripts that runs the entire project pipeline, combining all of the processing scripts.
- [`/src`](https://github.com/NeuroTech-UCSD/Project-Template/tree/main/src) - Modular code files that are meant to be imported by different scripts.
	- [`/src/funcs.py`](https://github.com/NeuroTech-UCSD/Project-Template/blob/main/src/funcs.py) - Modular data processing functions for the script files to use.
	- [`/src/utils.py`](https://github.com/NeuroTech-UCSD/Project-Template/blob/main/src/utils.py) - Modular utility functions such as ploting, loading, and saving the data.
	- [`/src/custom_module.py`](https://github.com/NeuroTech-UCSD/Project-Template/blob/main/src/custom_module.py) - Can have different names. Where we define custom classes for modeling, GUI, etc.

## Reproduce GUI without headset (dockerized)
Editing...

## Reproduce GUI with headset
### Create the dataset
- Configure DSI-24 or configure code for other EEG headsets
- Open [`/scripts/psychopy_competition.py`](https://github.com/NeuroTech-UCSD/Oz-Speller/blob/main/scripts/psychopy_competition.py) with your preferred text editor. Scroll to the subsection `VARIABLES`: 
  - Set `use_dsi_lsl` to `True`
  - Set `test_mode` to `True`
  - Set `make_predictions` to `False`
  - (optional) Set `stim_duration` to `5` or higher if you want to validate the data with spectral analysis
  - Save and exit
- From the root directory, run `python scripts/psychopy_competition.py` and perform the calibration process, which should take at least 5 minutes.
- Move `eeg.csv` and `meta.csv` from the root directory to `/data/eeg_recordings/DSI-24/[YOUR_NAME]/run[x]`. You can replace `DSI-24` with a different folder name if you set up the code to work with a different headset.
- Repeat the last 2 steps at least 3 times if you want to use the dataset to train FBTDCA.
### Train the Model
- Open [`/notebooks/TriggerHubData.ipynb`](https://github.com/NeuroTech-UCSD/Oz-Speller/blob/main/scripts/psychopy_competition.py) with your preferred text editor. 
- On the 3rd cell:
  - Set `sub_dirs` to the appropriate number of runs
  - Within the for loop, find `data_path` and change the first string to `/data/eeg_recordings/DSI-24/[YOUR_NAME]/`.
- Run the first 4 cells in order.
### Use the model in real-time
Once you have successfully trained the model:
- On the 5th cell, change the first string in `open()` to `'/reports/trained_models/32-class_speller/DSI-24/[YOUR_NAME]/fbtdca_1s.pkl'`
- Run the 5th cell
- Open [`/scripts/psychopy_competition.py`](https://github.com/NeuroTech-UCSD/Oz-Speller/blob/main/scripts/psychopy_competition.py) with your preferred text editor. Scroll to the subsection `VARIABLES`: 
  - Set `use_dsi_lsl` to `True`
  - Set `test_mode` to `True` if you want to check the accuracy or `False` if you want to enable the virtual keyboard.
  - Set `make_predictions` to `True`, and set the first string under `open()` to `'/reports/trained_models/32-class_speller/DSI-24/[YOUR_NAME]/fbtdca_1s.pkl'`
- From the root directory, run `python scripts/psychopy_competition.py` 
### Configure DSI-24
- Follow the setup instruction for DSI-24 on the Wearable Sensing's [official website](https://wearablesensing.com/dsi-24/)
- Open [`/scripts/psychopy_competition.py`](https://github.com/NeuroTech-UCSD/Oz-Speller/blob/main/scripts/psychopy_competition.py) with your preferred text editor. Scroll to the subsection `if use_dsi_lsl`: 
  - Change `'--port=COM15'` to the port DSI-24 is assigned to
  - Change the `'COM14'` in `dsi_serial = serial.Serial('COM14', 9600)` to the port the Trigger Hub is assigned to
- Contact Wearable Sensing for further assistence if needed.

## Data validation
### Phase offset check FFT (figure)
### Photosensor (figure)
### Trigger Hub

## Data Analysis & Models
### Arico dataset
### 36-class dataset 
### Competition dataset

## Prepare Data
- `py src/data/make_dataset.py ${RAW_DATA_DIR} ${OUTPUT_PATH}` to parse raw continuous data into bandpass trialized data for modeling. The output data will be numpy data with the shape: (trials, num_targets, channels, timepoints) 
  - ${RAW_DATA_DIR} should have two files in it, meta.csv and eeg.csv.
  - eeg.csv will have the first column being the timestamps, and the rest of the columns
being the channel names. 
  - meta.csv has no headers, its 1st column is the corresponding freq of our targets, 2nd column is the phase offset, and 
3rd column is the time with timepoint as units
- `py src/data/split_dataset.py ${EEG_DATA_PATH} ${LABEL_DATA_PATH} -train -val -test ${OUTPUT_PATH}` 
  - ${EEG_DATA_PATH} should contain data with the shape in npy format: (trials, num_targets, channels, timepoints)
  - ${EEG_DATA_PATH} should contain data with the shape in npy format: (trials, num_targets)
  - `-train` specifies the proportion of training data `-val` and `-test` for the validation and testing data respectively. The proportions must sum up to 1.


## Models
- `py src/models/train.py ${TRAIN_DATA_PATH} ${VALIDATION_DATA_PATH} ${OUTPUT_PATH}` to train the model and save it

## Evaluation
`py src/models/evaluation.py ${CHECKPOINT_PATH} ${TEST_DATA_PATH}` to evaluate model performance

## To trigger frontend
- `python scripts/server.py` to create server
- `python scripts/dsi.py` to start listening to any changes ...
- `python scripts/dsi_helper.py` to ...
- `python scripts/psychopy_competition.py` to ...

## Acknowledgement
Put the team and partners here.
- Wearable Sensing
- Brainda EEG modeling toolkit: 
- TRCA:
- TDCA:
- EEGNet: https://github.com/vlawhern/arl-eegmodels
- Visual Delay: https://www.pnas.org/doi/10.1073/pnas.1508080112
- Frame index flashing: https://sccn.ucsd.edu/~yijun/pdfs/EMBC14c.pdf
