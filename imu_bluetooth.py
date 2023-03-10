import asyncio # async stuff

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

import struct # decoding the structs
from signal import SIGINT, SIGTERM # for exiting elgently with ctrl+c
import signal
class GracefulExit(SystemExit):
    code = 1


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
        while True: # loop forever, here we can do other stuff such as send audio to the haptic engine
            await asyncio.sleep(1) # sleep for 1 second, this is needed to keep the loop from running too fast
            Ax1, Ay1, Az1, Gx1, Gy1, Gz1, Ax2, Ay2, Az2, Gx2, Gy2, Gz2 = imu_data
            diff_ax = abs(Ax1 - Ax9o92)
            if diff_ax > 10:
                print('Moving!!')
            print(imu_data) # print the imu data array gathered from the callback function

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
