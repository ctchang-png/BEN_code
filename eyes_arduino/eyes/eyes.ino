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

#define COLOR_RGB565_BACKGROUND 0xF00F //Note that this is a stupid ass library written by monkeys and RGB565 values are inverted b/c backlight
#define CELL_SIZE 20 //20x20 eye cells
#define HEIGHT 320
#define WIDTH 240
/**
 * @brief Constructor Constructor of hardware SPI communication
 * @param dc Command/data line pin for SPI communication
 * @param cs Chip select pin for SPI communication
 * @param rst reset pin of the screen
 */
DFRobot_ST7789_240x320_HW_SPI screen(/*dc=*/TFT_DC,/*cs=*/TFT_CS,/*rst=*/TFT_RST);
int px = WIDTH/2;
int py = HEIGHT/2;
int pr;
int pc;
int px_old = 0;
int py_old = 0;

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
  screen.fillScreen(COLOR_RGB565_BACKGROUND);
  for (int r_cell=0; r_cell <= floor(HEIGHT / CELL_SIZE); r_cell++) {
    screen.drawFastHLine(0, r_cell*CELL_SIZE, WIDTH, 0xFFFF);
    screen.drawFastHLine(0, r_cell*CELL_SIZE+1, WIDTH, 0xFFFF);
  }
  for (int c_cell=0; c_cell <= floor(WIDTH / CELL_SIZE); c_cell++) {
    screen.drawFastVLine(c_cell*CELL_SIZE, 0, HEIGHT, 0xFFFF);
    screen.drawFastVLine(c_cell*CELL_SIZE+1,0,HEIGHT, 0xFFFF);
  }
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
  //myBridge.write_HeaderAndTwoArrays("Arduino-Data", int_arr, numIntVals_fromPy, float_arr, numFloatVals_fromPy);
  //For now, ints_recieved = {pupil_x, pupil_y, pupil_r, pupil_c}
  //For now, floats_recieved = {}
  if (px_old != px || py_old != py){ //Only write if something moves
    draw_pupil_continuous(px, py, 0xFFFF);
    //draw_pupil_cell(px, px_old, py, py_old, 0xFFFF);
    px_old = px;
    py_old = py;
    delay(20);
  }
  //Assuming that the "xyz" header is not related to any programmed command...
  //strcpy(myBridge.headerOfMsg, "xyz");//...this line prevents the Arduino board from keeping executing the last command received cyclically.
}

void draw_pupil_continuous(int px, int py, int color) {
  screen.fillRect(px_old-CELL_SIZE, py_old-CELL_SIZE, 2*CELL_SIZE, 2*CELL_SIZE, COLOR_RGB565_BACKGROUND);
  delay(50);
  screen.fillRect(px-CELL_SIZE, py-CELL_SIZE, 2*CELL_SIZE, 2*CELL_SIZE, color);
  delay(50);
  int cell_r = floor(py / CELL_SIZE);
  int cell_c = floor(px / CELL_SIZE);
  int rem_r = py - cell_r;
  int rem_c = px - cell_c;
  screen.drawFastVLine(cell_c*CELL_SIZE, 0, HEIGHT, 0xFFFF);
  screen.drawFastVLine(cell_c*CELL_SIZE+1, 0, HEIGHT, 0xFFFF);
  screen.drawFastVLine((cell_c+1)*CELL_SIZE, 0, HEIGHT, 0xFFFF);
  screen.drawFastVLine((cell_c+1)*CELL_SIZE+1, 0, HEIGHT, 0xFFFF);
  screen.drawFastHLine(0, cell_r*CELL_SIZE, WIDTH, 0xFFFF);
  screen.drawFastHLine(0, cell_r*CELL_SIZE+1, WIDTH, 0xFFFF);
  screen.drawFastHLine(0, (cell_r+1)*CELL_SIZE, WIDTH, 0xFFFF);
  screen.drawFastHLine(0, (cell_r+1)*CELL_SIZE+1, WIDTH, 0xFFFF);
  delay(50);
  /*for (int r_cell=0; r_cell <= floor(HEIGHT / CELL_SIZE); r_cell++) {
    screen.drawFastHLine(0, r_cell*CELL_SIZE, WIDTH, 0xFFFF);
    screen.drawFastHLine(0, r_cell*CELL_SIZE+1, WIDTH, 0xFFFF);
  }
  for (int c_cell=0; c_cell <= floor(WIDTH / CELL_SIZE); c_cell++) {
    screen.drawFastVLine(c_cell*CELL_SIZE, 0, HEIGHT, 0xFFFF);
    screen.drawFastVLine(c_cell*CELL_SIZE+1,0,HEIGHT, 0xFFFF);
  }*/
}

void draw_pupil_cell(int px, int px_old, int py, int py_old, int color) {
  int cell_r = floor(py/CELL_SIZE);
  int rem_r = py-cell_r;
  int cell_c = floor(px/CELL_SIZE);
  int rem_c = px-cell_c;

  int cell_r_old = floor(py_old/CELL_SIZE);
  int rem_r_old = py_old - cell_r_old;
  int cell_c_old = floor(px_old/CELL_SIZE);
  int rem_c_old = px_old - cell_c_old;
  
  //Pick which cells need to be filled in
  //For now just do 4 with nearest cell as origin and go down and right


  int w = CELL_SIZE - 2; //assume grid line thickness is 2
  int h = CELL_SIZE - 2;
  screen.fillRect(cell_c*CELL_SIZE+2, cell_r*CELL_SIZE+2, w, h, color);
  screen.fillRect((cell_c+1)*CELL_SIZE+2, cell_r*CELL_SIZE+2, w, h, color);
  screen.fillRect(cell_c*CELL_SIZE+2, (cell_r+1)*CELL_SIZE+2, w, h, color);
  screen.fillRect((cell_c+1)*CELL_SIZE+2, (cell_r+1)*CELL_SIZE+2, w, h, color);
  if (cell_r > cell_r_old) {
    screen.fillRect(cell_c*CELL_SIZE+2, (cell_r-1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
    screen.fillRect((cell_c+1)*CELL_SIZE+2, (cell_r-1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
  }
  if (cell_r < cell_r_old) {
    screen.fillRect(cell_c*CELL_SIZE+2, (cell_r+1+1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
    screen.fillRect((cell_c+1)*CELL_SIZE+2, (cell_r+1+1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);    
  }
  if (cell_c > cell_c_old) {
    screen.fillRect((cell_c-1)*CELL_SIZE+2, (cell_r)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
    screen.fillRect((cell_c-1)*CELL_SIZE+2, (cell_r+1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
  }
  if (cell_c < cell_c_old) {
    screen.fillRect((cell_c+1+1)*CELL_SIZE+2, (cell_r)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
    screen.fillRect((cell_c+1+1)*CELL_SIZE+2, (cell_r+1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
  }
  if (cell_c < cell_c_old && cell_r < cell_r_old) {
    screen.fillRect((cell_c+1+1)*CELL_SIZE+2, (cell_r+1+1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
  }
  if (cell_c > cell_c_old && cell_r > cell_r_old) {
    screen.fillRect((cell_c-1)*CELL_SIZE+2, (cell_r-1)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
  }
}

void draw_pupil_cell_exp(int px, int px_old, int py, int py_old, int size, int color) {
  
}
