# haptic-feedback
- ```Arm use asymmetry pilot data_2023Mar24.pptx``` contains the procedure and results from Bev Larssen's pilot study as discussed in the report
- ```Julia interview transcript.pdf``` contains the raw transcript from interview w Julia
- ```Riley interview transcript.pdf``` contains the raw transcript from interview w Riley
- ```cogs 402 raw data - Sheet1.pdf``` contains the raw data from the IMUs during the application example + graphs of that data
- ```find_bluetooth.py``` is a file used to find the address the RFDuino we were using was sending out. 
- ```hapticEngine.py``` is the code that takes an input, such as the pressing of a keyboard space bar, and outputs an audio signal (```playSignal```) which can be converted to vibrations via the haptic engine. This code was modified and implemented in the final main code in ```imu_bluetooth.py``` so that instead of the audio being played when the space bar is pressed, audio is emitted upon sensing right hand movement.
- ```imu_bluetooth.ino``` is the code from Arduino that communicates with PyCharm. This is where IMU data is stored and sent out to be read out and manipulated in PyCharm.
- ```imu_bluetooth.py``` is the main file to run the code for the device.
- ```scanner.py``` searches for all bluetooth devices that are emitting a signal nearby. This was particularly useful in debugging when the RFDuino address would stop working or potentially change.
- ```wiring diagram.jpeg``` is the scheme of how the two IMUs and RFDuino are connected. Detailed descriptions and functions of each of these pins and connections are laid out in the report, as well as a more general diagram overview of the wiring (see Methodology section and Appendix).  

To run any of the ```.py``` files, you must have PyCharm installed. To run ```imu_bluetooth.py```, you must also have the Arduino IDE installed. To see the Arduino code directly, click on ```imu_bluetooth.ino```. You must have the Arduino IDE installed. Please contact owner (Maria) for help in running these. 
