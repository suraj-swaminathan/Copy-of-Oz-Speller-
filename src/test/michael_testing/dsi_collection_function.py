import asyncio
import socketio
import time
import datetime
import numpy as np
import threading
from dsi import TCPParser

sio = socketio.AsyncClient()
PORT = 4002
global current_trial
global prev
prev = datetime.datetime.now()
current_trial = '*'  # can replace with 0


@sio.event
async def connect():
    print('connected')


@sio.event
async def connect_error(e):
    print(e)


@sio.event
async def disconnect():
    await sio.disconnect()
    print('disconnected')


@sio.event
async def change_trial(data):
    global current_trial
    global prev
    current_trial = data  # data is just a char
    a = datetime.datetime.now()
    diff = a - prev
    diff_s = "%s" % (diff.total_seconds())
    print(diff_s)
    prev = a
    s = "%s:%s.%s" % (a.minute, a.second, str(a.microsecond)[:3])
    print(f'trial changed to \"{data}\" -- {s}')


async def ready():
    global config
    config = await sio.call(
        'dsi ready')  # wait for the server to confirm that server is ready. Server would send config when it's ready


async def fetch_data():
    global current_trial
    '''
    This function will continue fetch data from dsi headset and \
    (1) write the data to the csv
    (2) send it (deque snapshot with k elements with num_channels size each, k should be >= 1) to remote
    Note: we can move (2) outside and have the server ask for it instead
    :return:
    '''
    print('dsi collection initiated -- Start recording data ...')
    # ============= use config instead of hard coding ================
    num_trials = 7
    trial_duration = 3
    inter_trial_interval = 2
    # ================================================================
    dsi_parser = TCPParser('localhost',8844)
    data_thread = threading.Thread(target=dsi_parser.parse_data)
    data_thread.daemon = True
    data_thread.start()
    file = open('./eeg.csv', 'w')
    file.write('time, ch1, ch2, ch3, ch4, ch5, ch6, ch7\n')
    file.close()

    latest_signal_log = np.copy(dsi_parser.signal_log)
    latest_time_log = np.copy(dsi_parser.time_log)
    while latest_time_log[0,0] < 0.1:
        latest_signal_log = np.copy(dsi_parser.signal_log)
        latest_time_log = np.copy(dsi_parser.time_log)
        dsi_parser.signal_log = dsi_parser.signal_log[:,-1:]
        dsi_parser.time_log = dsi_parser.time_log[:,-1:]
        await sio.sleep(0.5)  # provide window for other thread to run

    while True:
        a = datetime.datetime.now()
        s = "%s:%s.%s" % (a.minute, a.second, str(a.microsecond)[:3])
        print(f'current trial {current_trial} -- {s}')
        if (current_trial != '*'):
            current_trial = '*'
        await sio.sleep(2)  # provide window for other thread to run

        # latest_signal_log = np.copy(dsi_parser.signal_log)
        # latest_time_log = np.copy(dsi_parser.time_log)
        # if latest_signal_log.shape[0] > 1: # if new data is appended
        #     dsi_parser.signal_log = np.zeros((1,20))
        #     dsi_parser.time_log = np.zeros((1,20))
        #     latest_signal_log = latest_signal_log.T # put num time points before num channels
        #     latest_time_log = latest_time_log.T
        #     # print(np.concatenate((latest_time_log, latest_signal_log[:,:8]), axis=1).shape)
        #     latest_data = np.concatenate((latest_time_log, latest_signal_log[:,:8]), axis=1)
        #     with open('./eeg.csv', 'a') as csv_file: # 'a' for append
        #         np.savetxt(csv_file, latest_data, delimiter=', ')
        #     await sio.emit('receive data', latest_data.tolist()) # pretend we got 5 samples in buffer
        
        latest_signal_log = np.copy(dsi_parser.signal_log)[:,:-1].T
        latest_time_log = np.copy(dsi_parser.time_log)[:,:-1].T
        dsi_parser.signal_log = dsi_parser.signal_log[:,-1:]
        dsi_parser.time_log = dsi_parser.time_log[:,-1:]
        latest_data = np.concatenate((latest_time_log, latest_signal_log[:,:8]), axis=1)
        with open('./eeg.csv', 'a') as csv_file: # 'a' for append
            np.savetxt(csv_file, latest_data, delimiter=', ')
        await sio.emit('receive data', latest_data.tolist())

            # print(np.stack((latest_time_log,latest_signal_log)).shape)
            # with open('./eeg.csv', 'a') as csv_file: # 'a' for append
            #     np.savetxt(csv_file, fake_data, delimiter=', ')
            # await sio.emit('receive data', fake_data.tolist()) # pretend we got 5 samples in buffer
            # print(latest_signal_log.shape)
            # print(latest_time_log.shape)

        await sio.sleep(0.1)  # provide window for other thread to run

async def fetch_fake_data():
    '''
    This function will continue fetch data from dsi headset and \
    (1) write the data to the csv
    (2) send it (deque snapshot with k elements with num_channels size each, k should be >= 1) to remote
    Note: we can move (2) outside and have the server ask for it instead
    :return:
    '''
    print('dsi collection initiated -- Start recording data ...')
    # ============= use config instead of hard coding ================
    num_trials = 7
    trial_duration = 3
    inter_trial_interval = 2
    # ================================================================
    file = open('./fake_eeg.csv', 'w')
    file.write('ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8\n')
    file.close()
    while True:
        # a = datetime.datetime.now()
        # s = "%s:%s.%s" % (a.minute, a.second, str(a.microsecond)[:3])
        # print(f'current trial {current_trial} -- {s}')
        fake_data = np.random.rand(5,8)
        with open('./fake_eeg.csv', 'a') as csv_file: # 'a' for append
            np.savetxt(csv_file, fake_data, delimiter=', ')
        await sio.emit('receive data', fake_data.tolist()) # pretend we got 5 samples in buffer
        await sio.sleep(0.1)  # provide window for other thread to run


async def main():
    await sio.connect(f'http://localhost:{PORT}')
    await sio.start_background_task(ready)
    # sio.start_background_task(fetch_fake_data)
    sio.start_background_task(fetch_data)
    await sio.wait()  # this line is important, do not delete


asyncio.run(main())
