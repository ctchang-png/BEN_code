#include <pyduino_bridge.h>
#include "DFRobot_GDL.h"
/*AVR series mainboard*/
//Pins for Data Command, Chip Select, Reset
#define TFT_DC  8
#define TFT_CS  10
#define TFT_RST 9
/*Define parameters for serial data transfer between python and arduino*/
#define numIntVals_fromPy = 1
#define numFloatVals_fromPy = 1

/**
 * @brief Constructor Constructor of hardware SPI communication
 * @param dc Command/data line pin for SPI communication
 * @param cs Chip select pin for SPI communication
 * @param rst reset pin of the screen
 */
DFRobot_ST7789_240x320_HW_SPI screen(/*dc=*/TFT_DC,/*cs=*/TFT_CS,/*rst=*/TFT_RST);


/*
 *User-selectable macro definition color
 *COLOR_RGB565_BLACK   COLOR_RGB565_NAVY    COLOR_RGB565_DGREEN   COLOR_RGB565_DCYAN 
 *COLOR_RGB565_MAROON  COLOR_RGB565_PURPLE  COLOR_RGB565_OLIVE    COLOR_RGB565_LGRAY     
 *COLOR_RGB565_DGRAY   COLOR_RGB565_BLUE    COLOR_RGB565_GREEN    COLOR_RGB565_CYAN  
 *COLOR_RGB565_RED     COLOR_RGB565_MAGENTA COLOR_RGB565_YELLOW   COLOR_RGB565_ORANGE           
 *COLOR_RGB565_WHITE   
 */

//=============

void setup() {
  // initialize the serial object
  Serial.begin(115200);
  Serial.println("<Arduino is ready>"); // tell the PC we are ready
  screen.begin();
}
//Create the Bridge_ino object for communication with Python
Bridge_ino myBridge(Serial);

//=============

void loop() {
  myBridge.curMillis = millis(); 
  myBridge.read();
  
  /*since in Arduino code, arrays are blocks of static memory whose size must be determined at compile time, before the program runs,
    you need to define the number of integer and float values received in the .h and .cpp files of the library
    in pyduino_bridge.h and pyduino_bridge.cpp, change the lines:
    #define numIntValues_FromPy 1
    #define numFloatValues_FromPy 1
    the values in both files must be the same
    */
  const char* header = myBridge.headerOfMsg;   //myBridge.headerOfMsg is the header characters received from Python
  uint16_t fill_color_565 = myBridge.intsRecvd[0];       //myBridge.intsRecvd is the array containing the integer values received from Python
  //For now, ints_recieved = {fill_color_565}
  float float0 = myBridge.floatsRecvd[0];      //myBridge.floatsRecvd is the array containing the integer values received from Python
  //For now, floats_recieved = {0.0}
  myBridge.writeEcho();
  //myBridge.writeEcho(); //sends to Python the same values received, and the millis time scaled by a bit shifting.
  //Internally, the following bit shifting is applied: `millis >> rightBitShifter`. This is equal to `millis/pow(2,rightBitShifter)`.
  //By default, Arduino sends to Python the millis value in apprx seconds, since the default bitShifter value is 10.
  //Arduino always sends a time value to Python.
  
  //the line below gives the same result as using myBridge.writeEcho(), since we receive from Python only 1 int and 1 float.
  //myBridge.writeTwoArrays(myBridge.intsRecvd,1,myBridge.floatsRecvd,1);
  
  screen.fillScreen(fill_color_565);
  //Assuming that the "xyz" header is not related to any programmed command...
  strcpy(myBridge.headerOfMsg, "xyz");//...this line prevents the Arduino board from keeping executing the last command received cyclically.
}
