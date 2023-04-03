#include <Adafruit_Sensor.h>
#include <RFduinoBLE.h>  // bluetooth communication

#include <basicMPU6050.h>  // MPU stuff

//-- Input parameters:

// Gyro settings:
#define LP_FILTER 3     // Low pass filter.                    Value from 0 to 6
#define GYRO_SENS 0     // Gyro sensitivity.                   Value from 0 to 3
#define ACCEL_SENS 0    // Accelerometer sensitivity.          Value from 0 to 3
#define ADDRESS_A0 LOW  // I2C address from state of A0 pin.   A0 -> GND : ADDRESS_A0 = LOW \
                        //                                     A0 -> 5v  : ADDRESS_A0 = HIGH
// Accelerometer offset:
constexpr int AX_OFFSET = 0;  // Use these values to calibrate the accelerometer. The sensor should output 1.0g if held level.
constexpr int AY_OFFSET = 0;  // These values are unlikely to be zero.
constexpr int AZ_OFFSET = 0;

// Output scale:
constexpr float AX_SCALE = 1.0;  // Multiplier for accelerometer outputs. Use this to calibrate the sensor. If unknown set to 1.
constexpr float AY_SCALE = 1.0;
constexpr float AZ_SCALE = 1.0;

constexpr float GX_SCALE = 1.0;  // Multiplier to gyro outputs. Use this to calibrate the sensor. If unknown set to 1.
constexpr float GY_SCALE = 1.0;
constexpr float GZ_SCALE = 1.0;

// Bias estimate:
#define GYRO_BAND 64     // Standard deviation of the gyro signal. Gyro signals within this band (relative to the mean) are suppresed.
#define BIAS_COUNT 10  // Samples of the mean of the gyro signal. Larger values provide better calibration but delay suppression response.

//-- Set the template parameters:

basicMPU6050<LP_FILTER, GYRO_SENS, ACCEL_SENS, ADDRESS_A0,
             AX_OFFSET, AY_OFFSET, AZ_OFFSET,
             &AX_SCALE, &AY_SCALE, &AZ_SCALE,
             &GX_SCALE, &GY_SCALE, &GZ_SCALE,
             GYRO_BAND, BIAS_COUNT >
  imu1;

basicMPU6050<LP_FILTER, GYRO_SENS, ACCEL_SENS, HIGH,
             AX_OFFSET, AY_OFFSET, AZ_OFFSET,
             &AX_SCALE, &AY_SCALE, &AZ_SCALE,
             &GX_SCALE, &GY_SCALE, &GZ_SCALE,
             GYRO_BAND, BIAS_COUNT >
  imu2;

sensors_event_t acc[2], gyro[2];  // sensor readings

union {  // using a union, writing to the float part also writes to the array part
  float floats[12];
  char chars[12 * sizeof(float)];  // char is 1 byte, float is 4 bytes
} float_2_bytes;

void setup() {
  Serial.begin(9600);
  RFduinoBLE.advertisementData = "RFduino";  // setup the name for the bluetooth
  RFduinoBLE.begin();                        // begin advertising bluetooth signal (python will need to listen)


//  Wire.begin();                           //begin the wire comunication  
//  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68)              
//  Wire.write(0x6B);                       //make the reset (place a 0 into the 6B register)
//  Wire.write(0x00);
//  Wire.endTransmission(true);             //end the transmission
//  //Gyro config
//  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68) 
//  Wire.write(0x1B);                       //We want to write to the GYRO_CONFIG register (1B hex)
//  Wire.write(0x10);                       //Set the register bits as 00010000 (1000dps full scale)
//  Wire.endTransmission(true);             //End the transmission with the gyro
//  //Acc config
//  Wire.beginTransmission(0x68);           //Start communication with the address found during search.
//  Wire.write(0x1C);                       //We want to write to the ACCEL_CONFIG register
//  Wire.write(0x10);                       //Set the register bits as 00010000 (+/- 8g full scale range)
//  Wire.endTransmission(true);
//
//  Wire.begin();                           //begin the wire comunication  
//  Wire.beginTransmission(0x69);           //begin, Send the slave adress (in this case 68)              
//  Wire.write(0x6B);                       //make the reset (place a 0 into the 6B register)
//  Wire.write(0x00);
//  Wire.endTransmission(true);             //end the transmission
//  //Gyro config
//  Wire.beginTransmission(0x69);           //begin, Send the slave adress (in this case 68) 
//  Wire.write(0x1B);                       //We want to write to the GYRO_CONFIG register (1B hex)
//  Wire.write(0x10);                       //Set the register bits as 00010000 (1000dps full scale)
//  Wire.endTransmission(true);             //End the transmission with the gyro
//  //Acc config
//  Wire.beginTransmission(0x69);           //Start communication with the address found during search.
//  Wire.write(0x1C);                       //We want to write to the ACCEL_CONFIG register
//  Wire.write(0x10);                       //Set the register bits as 00010000 (+/- 8g full scale range)
//  Wire.endTransmission(true);


  // Set registers - Always required
  imu1.setup();
  imu2.setup();

  // Initial calibration of gyro
  imu1.setBias();
  imu2.setBias();
}

void loop() {


//  //////////////////////////////////////Acc read/////////////////////////////////////      
//
//  Wire.beginTransmission(0x68);     //begin, Send the slave adress (in this case 68)   //talk from this address
//  Wire.write(0x3B);                 //Ask for the 0x3B register- correspond to AcX     //read from this address
//  Wire.endTransmission(false);      //keep the transmission and next                   //end code after talking (over and out)
//  Wire.requestFrom(0x68,12,true);    //We ask for next 12 registers starting with the 3B   //request from imu the data from 12 registers (don't care about temp, all in order)
 

//int i = 0;
//acc[i].acceleration.x = (Wire.read() << 8 | Wire.read())/16384.0;    //bitwise OR
//       acc[i].acceleration.y = (Wire.read() << 8 | Wire.read())/16384.0; 
//       acc[i].acceleration.z = (Wire.read() << 8 | Wire.read())/16384.0; 
//       gyro[i].gyro.x = (Wire.read() << 8 | Wire.read())/131.0;
//       gyro[i].gyro.y = (Wire.read() << 8 | Wire.read())/131.0;
//       gyro[i].gyro.z = (Wire.read() << 8 | Wire.read())/131.0;


//delay(100);
//
//  Wire.beginTransmission(0x69);     //begin, Send the slave adress (in this case 68)   //talk from this address
//  Wire.write(0x3B);                 //Ask for the 0x3B register- correspond to AcX     //read from this address
//  Wire.endTransmission(false);      //keep the transmission and next                   //end code after talking (over and out)
//  Wire.requestFrom(0x69,12,true);    //We ask for next 12 registers starting with the 3B   //request from imu the data from 12 registers (don't care about temp, all in order)


//i = 1;
//acc[i].acceleration.x = (Wire.read() << 8 | Wire.read())/16384;    //bitwise OR
//       acc[i].acceleration.y = (Wire.read() << 8 | Wire.read())/16384.0; 
//       acc[i].acceleration.z = (Wire.read() << 8 | Wire.read())/16384.0; 
//       gyro[i].gyro.x = (Wire.read() << 8 | Wire.read())/131.0;
//       gyro[i].gyro.y = (Wire.read() << 8 | Wire.read())/131.0;
//       gyro[i].gyro.z = (Wire.read() << 8 | Wire.read())/131.0;
//       
// 

//  /*We have asked for the 0x3B register. The IMU will send a burst of register.
//  * The amount of register to read is specify in the requestFrom function.
//  * In this case we request 6 registers. Each value of acceleration is made out of
//  * two 8bits registers, low values and high values. For that we request the 6 of them  
//  * and just make then sum of each pair. For that we shift to the left the high values 
//  * register (<<) and make an or (|) operation to add the low values.
//  If we read the datasheet, for a range of+-8g, we have to divide the raw values by 4096*/    
//  Serial.println((Wire.read()<<8|Wire.read())/4096.0) ; //each value needs two registres
//  (Wire.read()<<8|Wire.read())/4096.0 ;
//  (Wire.read()<<8|Wire.read())/4096.0 ; 
// 
  imu1.updateBias();
  imu2.updateBias();

  for (int i = 0; i < 2; i++) {
    acc[i].acceleration.x = 1 + 6 * i;
    acc[i].acceleration.y = 2 + 6 * i;
    acc[i].acceleration.z = 3 + 6 * i;
    gyro[i].gyro.x = 4 + 6 * i;
    gyro[i].gyro.y = 5 + 6 * i;
    gyro[i].gyro.z = 6 + 6 * i;
  }

   for (int i = 0; i < 2; i++) {    //when adding imu2, make i < 2
     if (i == 0) {
       acc[i].acceleration.x = imu1.ax();
       acc[i].acceleration.y = imu1.ay();
       acc[i].acceleration.z = imu1.az();
       gyro[i].gyro.x = imu1.gx();
       gyro[i].gyro.y = imu1.gy();
       gyro[i].gyro.z = imu1.gz();
     } else {
      delay(100); // delay between reading imu1 and imu2
       acc[i].acceleration.x = imu2.ax();
       acc[i].acceleration.y = imu2.ay();
       acc[i].acceleration.z = imu2.az();
       gyro[i].gyro.x = imu2.gx();
       gyro[i].gyro.y = imu2.gy();
       gyro[i].gyro.z = imu2.gz();
     }
   }

   //Serial.println(imu1.ax());

  // send the sample to the bluetooth client
  // each float is 4 bytes and we have 12 floats to send (2 chips x 6 values per chip), hence a total of 48 bytes
  // we send this as a char array, where each char is 1 byte.
  for (int i = 0; i < 2; i++) {
    float_2_bytes.floats[0 + 6 * i] = acc[i].acceleration.x;
    float_2_bytes.floats[1 + 6 * i] = acc[i].acceleration.y;
    float_2_bytes.floats[2 + 6 * i] = acc[i].acceleration.z;
    float_2_bytes.floats[3 + 6 * i] = gyro[i].gyro.x;
    float_2_bytes.floats[4 + 6 * i] = gyro[i].gyro.y;
    float_2_bytes.floats[5 + 6 * i] = gyro[i].gyro.z;
  }

  // send the data here. Note there is a limit of 20 bytes for each send according to the docs
  // we will send three packets with a short delay in between
  RFduinoBLE.send(float_2_bytes.chars, 5 * sizeof(float));                       // send 20 bytes
  RFduinoBLE.send(&float_2_bytes.chars[5 * sizeof(float)], 5 * sizeof(float));   // send the next 20
  RFduinoBLE.send(&float_2_bytes.chars[10 * sizeof(float)], 2 * sizeof(float));  // send the last 8
  RFduino_ULPDelay(100);                                                         // delay 100ms before next send
}


void RFduinoBLE_onConnect() {
  Serial.println("Bluetooth Connected");
}

void RFduinoBLE_onDisconnect() {
  Serial.println("Bluetooth Disconnected");
}
