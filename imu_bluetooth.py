import asyncio # async stuff
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
import signal
import struct # decoding the structs
from signal import SIGINT, SIGTERM # for exiting elgently with ctrl+c
from hapticEngine import createComplexSignal, playSignal
class GracefulExit(SystemExit):
    code = 1

A_freq = 440 # Hz
Csh_freq = A_freq * 2 ** (4 / 12) # Hz (note ** is the exponent operator)
E_freq = A_freq * 2 ** (7 / 12) # Hz
#delay_1 = playSignal(createSignal(0.01, 2))  # play nothing (a very low signal) for 2 seconds
#delay_2 = playSignal(createSignal(0.01, 2))  # play nothing (a very low signal) for 2 seconds

freqs     = [A_freq, 0.01, Csh_freq, 0.01, E_freq] # the chosen frequencies
durations = [0.1, 0.1, 0.1, 0.1, 0.1] # durations for each frequency

audio = createComplexSignal(freqs, durations)

def raise_graceful_exit(*args):
    loop.stop()
    print("Gracefully shutdown")
    raise GracefulExit()


ADDRESS = "DB:52:F5:9F:7C:36" # RFduino Address

count = 0 # counter to keep track of which packet we are on
tmp_array = [] # array to store the data from the packets
imu_data = [] # array to store the imu data
def callback(sender, data):
    '''
    Callback function to handle the data from the sensor.
    The sensor sends 3 packets of data, for a total of 48 bytes.
    The first packet is 20 bytes long, the second is 20 bytes long, and the last is 8 bytes long.
    The data is organized into 12 floats, from each chip there are 3 for the accelerometer, 3 for the gyroscope.
    The first 6 floats are for the first chip the last 6 floats are for the second chip.
    Format: [Ax1, Ay1, Az1, Gx1, Gy1, Gz1, Ax2, Ay2, Az2, Gx2, Gy2, Gz2]
    '''
    global count
    global tmp_array
    global imu_data

    if count == 0 or count == 1: # first two packets are 20 bytes long
        tmp_array.extend(struct.unpack('< f f f f f', data))
    else:
        tmp_array.extend(struct.unpack('< f f', data)) # last packet is 8 bytes long
        imu_data = [x for x in tmp_array] # copy the data to the imu_data array
        tmp_array.clear() # clear the tmp_array
    count += 1
    count %= 3


async def main(ble_address: str) -> object:
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0) # find the device
    if not device:  # if we can't find the device, raise an error
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client: # connect to the device s
        print(f"Connected: {client.is_connected}")
        for count, service in enumerate(client.services): # size should be one
            if count != 2: continue
            write_port = service.characteristics[1] # port to write on (not needed for this example)
            read_port = service.characteristics[0] # port to read on (needed for this example)

        await client.start_notify(read_port.uuid, callback) # start the notification for the read port with the callback function above
        # Define variables to store the last 10 readings for each variable
        last_readings = {'Ax1': [], 'Ay1': [], 'Az1': [], 'Gx1': [], 'Gy1': [], 'Gz1': [], 'Ax2': [], 'Ay2': [],
                         'Az2': [], 'Gx2': [], 'Gy2': [], 'Gz2': []}
        while True: # loop forever, here we can do other stuff such as send audio to the haptic engine
            await asyncio.sleep(1) # sleep for 1 second, this is needed to keep the loop from running too fast
            Ax1, Ay1, Az1, Gx1, Gy1, Gz1, Ax2, Ay2, Az2, Gx2, Gy2, Gz2 = imu_data

            # diff_ax = abs(Ax1 - Ax2)
            # diff_ay = abs(Ay1 - Ay2)
            # diff_az = abs(Az1 - Az2)
            # diff_gx = abs(Gx1 - Gx2)
            # diff_gy = abs(Gy1 - Gy2)
            # diff_gz = abs(Gz1 - Gz2)
            def update_last_readings(variable_name, value):
                last_readings[variable_name].append(value)
                if len(last_readings[variable_name]) > 10:
                    last_readings[variable_name] = last_readings[variable_name][-10:]
            update_last_readings('Ax1', Ax1)
            update_last_readings('Ay1', Ay1)
            update_last_readings('Az1', Az1)
            update_last_readings('Gx1', Gx1)
            update_last_readings('Gy1', Gy1)
            update_last_readings('Gz1', Gz1)
            update_last_readings('Ax2', Ax2)
            update_last_readings('Ay2', Ay2)
            update_last_readings('Az2', Az2)
            update_last_readings('Gx2', Gx2)
            update_last_readings('Gy2', Gy2)
            update_last_readings('Gz2', Gz2)

            avg_ax1 = sum(last_readings['Ax1']) / len(last_readings['Ax1'])
            avg_ay1 = sum(last_readings['Ay1']) / len(last_readings['Ay1'])
            avg_az1 = sum(last_readings['Az1']) / len(last_readings['Az1'])
            avg_gx1 = sum(last_readings['Gx1']) / len(last_readings['Gx1'])
            avg_gy1 = sum(last_readings['Gy1']) / len(last_readings['Gy1'])
            avg_gz1 = sum(last_readings['Gz1']) / len(last_readings['Gz1'])
            avg_ax2 = sum(last_readings['Ax2']) / len(last_readings['Ax2'])
            avg_ay2 = sum(last_readings['Ay2']) / len(last_readings['Ay2'])
            avg_az2 = sum(last_readings['Az2']) / len(last_readings['Az2'])
            avg_gx2 = sum(last_readings['Gx2']) / len(last_readings['Gx2'])
            avg_gy2 = sum(last_readings['Gy2']) / len(last_readings['Gy2'])
            avg_gz2 = sum(last_readings['Gz2']) / len(last_readings['Gz2'])
            LH_ACC_THRESHOLD = 2
            LH_GYR_THRESHOLD = 2
            RH_ACC_THRESHOLD = 2
            RH_GYR_THRESHOLD = 3

            #LH = IMU 2
            #RH = IMU 1
            if (  (avg_ax1 - avg_ax2) > RH_ACC_THRESHOLD):
                print("RH in motion")
                playSignal(audio)
            elif (  (avg_ax2 - avg_ax1) > LH_ACC_THRESHOLD):
                print("LH in motion")
            else:
                print("At rest")
            print(imu_data)
            print(avg_ax1)
            print(avg_ax2)
            #if (avg_ax1 > avg_ax2 + RH_ACC_THRESHOLD or avg_ay1 > avg_ay2 + RH_ACC_THRESHOLD or avg_az1 > avg_az2 + RH_ACC_THRESHOLD or avg_gx1 > avg_gx2 + RH_GYR_THRESHOLD or avg_gy1 > avg_gy2 + RH_GYR_THRESHOLD or avg_gz1 > avg_gz2 + RH_GYR_THRESHOLD):
            #    print("RH in motion")
            #    playSignal(audio)
            #elif (avg_ax2 > avg_ax1 + LH_ACC_THRESHOLD or avg_ay2 > avg_ay1 + LH_ACC_THRESHOLD or avg_az2 > avg_az1 + LH_ACC_THRESHOLD or avg_gx2 > avg_gx1 + LH_GYR_THRESHOLD or avg_gy2 > avg_gy1 + LH_GYR_THRESHOLD or avg_gz2 > avg_gz1 + LH_GYR_THRESHOLD):
            #    print("LH in motion")
            #elif
            #else:
            #    print("Both in motion")
            #print(imu_data) # print the imu data array gathered from the callback function


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(main(ADDRESS))
    signal.signal(signal.SIGINT, raise_graceful_exit)
    signal.signal(signal.SIGTERM, raise_graceful_exit)
    #for signal in [SIGINT, SIGTERM]:
        #loop.add_signal_handler(signal, main_task.cancel)
    try:
        loop.run_until_complete(main_task)
    except GracefulExit:
        pass
    finally:
        loop.close()
