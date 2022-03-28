#include <pyduino_bridge.h>
#include "DFRobot_GDL.h"
/*AVR series mainboard*/
//Pins for Data Command, Chip Select, Reset
#define TFT_DC  8
#define TFT_CS  10
#define TFT_RST 9
/*Define parameters for serial data transfer between python and arduino*/
#define numIntVals_fromPy  4
#define numFloatVals_fromPy  0

/**
 * @brief Constructor Constructor of hardware SPI communication
 * @param dc Command/data line pin for SPI communication
 * @param cs Chip select pin for SPI communication
 * @param rst reset pin of the screen
 */
DFRobot_ST7789_240x320_HW_SPI screen(/*dc=*/TFT_DC,/*cs=*/TFT_CS,/*rst=*/TFT_RST);
int px;
int py;
int pr;
int pc;

/*
 *User-selectable macro definition color
 *COLOR_RGB565_BLACK   COLOR_RGB565_NAVY    COLOR_RGB565_DGREEN   COLOR_RGB565_DCYAN 
 *COLOR_RGB565_MAROON  COLOR_RGB565_PURPLE  COLOR_RGB565_OLIVE    COLOR_RGB565_LGRAY     
 *COLOR_RGB565_DGRAY   COLOR_RGB565_BLUE    COLOR_RGB565_GREEN    COLOR_RGB565_CYAN  
 *COLOR_RGB565_RED     COLOR_RGB565_MAGENTA COLOR_RGB565_YELLOW   COLOR_RGB565_ORANGE           
 *COLOR_RGB565_WHITE   
 */

//=============
#define COLOR_RGB565_GREEN 0x0FF0

void setup() {
  // initialize the serial object
  Serial.begin(115200);
  Serial.println("<Arduino is ready>"); // tell the PC we are ready
  screen.begin();
  screen.fillScreen(COLOR_RGB565_GREEN);
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
  myBridge.writeEcho();
  const char* header = myBridge.headerOfMsg;   //myBridge.headerOfMsg is the header characters received from Python
  px = myBridge.intsRecvd[0];              //myBridge.intsRecvd is the array containing the integer values received from Python
  py = myBridge.intsRecvd[1];
  pr = myBridge.intsRecvd[2];
  pc = myBridge.intsRecvd[3];

  int int_arr[] = {px, py, pr, pc};
  float float_arr[] = {};
  myBridge.write_HeaderAndTwoArrays("Arduino Data", int_arr, numIntVals_fromPy, float_arr, numFloatVals_fromPy);
  //For now, ints_recieved = {pupil_x, pupil_y, pupil_r, pupil_c}
  //float float0 = myBridge.floatsRecvd[0];      //myBridge.floatsRecvd is the array containing the integer values received from Python
  //For now, floats_recieved = {0.0}
  screen.fillCircle(px, py, 10, 0xFFFF);
  

  //Assuming that the "xyz" header is not related to any programmed command...
  strcpy(myBridge.headerOfMsg, "xyz");//...this line prevents the Arduino board from keeping executing the last command received cyclically.
}
