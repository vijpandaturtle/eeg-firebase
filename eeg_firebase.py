import time
import argparse
import numpy as np
import threading
import pandas as pd

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

import firebase_admin
from firebase_admin import db, credentials


# Fetch the service account key JSON file contents
cred = credentials.Certificate('eeg-stress-companion-firebase-adminsdk-pgufe-22017970db.json')
# Initialize the app with a custom auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {'databaseURL': 'https://eeg-stress-companion-default-rtdb.firebaseio.com'})


def liveStream():
    BoardShim.enable_dev_board_logger()
    # use synthetic board for demo
    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)
    args = parser.parse_args()
    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    
    board = BoardShim(args.board_id, params)
    eeg_channels = BoardShim.get_eeg_channels(args.board_id)
    sampling_rate = BoardShim.get_sampling_rate(args.board_id)
    timestamp = BoardShim.get_timestamp_channel(args.board_id)
    board.prepare_session()
    board.start_stream()
    keepAlive = 0

    #ganglion_data = pd.DataFrame()
    while keepAlive < 1:
        #get board data removes data from the buffer
        while board.get_board_data_count()<250:
            time.sleep(0.005)
        data = board.get_board_data()

        #creating a dataframe of the eeg data to extract eeg values later
        eegdf = pd.DataFrame(np.transpose(data[eeg_channels]))
        eegdf_col_names = ["AF7", "AF8", "TP9", "TP10"]
        eegdf.columns = eegdf_col_names
        for index,item in eegdf.iterrows():
            result = db.reference('/AF7').push().set(item['AF7'])
            result = db.reference('/AF8').push().set(item['AF8'])
            result = db.reference('/TP9').push().set(item['TP9'])
            result = db.reference('/TP10').push().set(item['TP10'])
        #to keep it simple, making another dataframe for the timestamps to access later
        #timedf = pd.DataFrame(np.transpose(data[timestamp]))
        #ganglion_data = pd.concat([ganglion_data,eegdf],ignore_index=False)
        keepAlive += 1
    #ganglion_data.to_csv('data.csv')
    board.stop_stream()
    board.release_session()

liveStream()