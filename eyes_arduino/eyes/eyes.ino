#include <pyduino_bridge.h>
#include "DFRobot_GDL.h"
/*AVR series mainboard*/
//Pins for Data Command, Chip Select, Reset
#define TFT_DC_L  8
#define TFT_CS_L  10
#define TFT_RST_L 9

#define TFT_DC_R 7
#define TFT_CS_R 5
#define TFT_RST_R 6
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
DFRobot_ST7789_240x320_HW_SPI screenL(/*dc=*/TFT_DC_L,/*cs=*/TFT_CS_L,/*rst=*/TFT_RST_L);
DFRobot_ST7789_240x320_HW_SPI screenR(/*dc=*/TFT_DC_R,/*cs=*/TFT_CS_R,/*rst=*/TFT_RST_R);
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
  screenL.begin();
  screenR.begin();
  screenL.fillScreen(COLOR_RGB565_BACKGROUND);
  screenR.fillScreen(COLOR_RGB565_BACKGROUND);
  for (int r_cell=0; r_cell <= floor(HEIGHT / CELL_SIZE); r_cell++) {
    screenL.drawFastHLine(0, r_cell*CELL_SIZE, WIDTH, 0xFFFF);
    screenL.drawFastHLine(0, r_cell*CELL_SIZE+1, WIDTH, 0xFFFF);
    screenR.drawFastHLine(0, r_cell*CELL_SIZE, WIDTH, 0xFFFF);
    screenR.drawFastHLine(0, r_cell*CELL_SIZE+1, WIDTH, 0xFFFF);
  }
  for (int c_cell=0; c_cell <= floor(WIDTH / CELL_SIZE); c_cell++) {
    screenL.drawFastVLine(c_cell*CELL_SIZE, 0, HEIGHT, 0xFFFF);
    screenL.drawFastVLine(c_cell*CELL_SIZE+1,0,HEIGHT, 0xFFFF);
    screenR.drawFastVLine(c_cell*CELL_SIZE, 0, HEIGHT, 0xFFFF);
    screenR.drawFastVLine(c_cell*CELL_SIZE+1,0,HEIGHT, 0xFFFF);
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
    //draw_pupil_continuous(px, py, 0xFFFF);
    // Use size 2 for now
    pr = 3;
    draw_pupil_cell(px, px_old, py, py_old, pr, pr, 0xFFFF);
    px_old = px;
    py_old = py;
    delay(20);
  }
  //Assuming that the "xyz" header is not related to any programmed command...
  //strcpy(myBridge.headerOfMsg, "xyz");//...this line prevents the Arduino board from keeping executing the last command received cyclically.
}

void draw_pupil_cell(int px, int px_old, int py, int py_old, int size_w, int size_h, int color) {
  int cell_r = floor(py/CELL_SIZE);
  int cell_c = floor(px/CELL_SIZE);

  int cell_r_old = floor(py_old/CELL_SIZE);
  int cell_c_old = floor(px_old/CELL_SIZE);
  
  //assume grid line thickness is 2
  int w = CELL_SIZE - 2; 
  int h = CELL_SIZE - 2;

  //Pick which cells need to be filled in
  int n = size_w * size_h;
  int x_new[n];
  int y_new[n];
  int x_old[n];
  int y_old[n];


  int i = 0;
  for (int r_offset = 0; r < size_h; r++) {
    for (int c_offset = 0; c < size_w; c++) {
      x_new[i] = cell_c + c_offset - floor(size_h/2);
      x_old[i] = cell_c_old + c_offset - floor(size_h/2);
      y_new[i] = cell_r + r_offset - floor(size_w/2);
      y_old[i] = cell_r_old + r_offset - floor(size_w/2);
      i++;
    }
  }
  int x;
  int y;
  
  int clear_arr[n];
  for (int i = 0; i < n; i++) {
    //Check every old cell for membership in new pupil
    x = x_old[i];
    y = y_old[i];
    clear_arr[i] = 1;
    for (int j = 0; j < n; j++) {
      //If coordinates match up, cell should not be cleared. Set clear_flag to 0 and move to next old cell.
      if (x == x_new[j] && y == y_new[j]) {
        clear_arr[i] = 0;
        break;
      }
    }
  }
  
  int draw_arr[n];
  for (int i = 0; i < n; i++) {
    //Check every new cell for membership in old pupil
    x = x_new[i];
    y = x_new[i];
    draw_arr[i] = 1;
    for (int j = 0; j < n; j++) {
      //If coordinates match up, cell should not be drawn. Set draw flag to 0 and move to next new cell.
      if (x == x_old[j] && y == y_old[j]) {
        draw_arr[i] = 0;
        break;
      }
    }
  }
  //Move through new and old cells, drawing and clearing only as needed.
  //Might look better if pupils are drawn first and cleared second, but test this later.
  for (int i = 0; i < n; i++) {
    //If new cell is flagged to be drawn, do so
    if (draw_arr[i]) {
      x = x_new[i];
      y = y_new[i];
      screenL.fillRect(x*CELL_SIZE+2, y*CELL_SIZE+2, w, h, color);
      screenR.fillRect((WIDTH/CELL_SIZE-x)*CELL_SIZE+2, (HEIGHT/CELL_SIZE-y)*CELL_SIZE+2, w, h, color);
    }
  }
  for (int i = 0; i < n; i++) {
    //If old cell is flagged to be cleared, do so 
    if (clear_arr[i]) {
      x = x_old[i];
      y = y_old[i];
      screenL.fillRect(x*CELL_SIZE+2, y*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);
      screenR.fillRect((WIDTH/CELL_SIZE-x)*CELL_SIZE+2, (HEIGHT/CELL_SIZE-y)*CELL_SIZE+2, w, h, COLOR_RGB565_BACKGROUND);  
    }
  }
}

void draw_pupil_cell_exp(int px, int px_old, int py, int py_old, int size, int color) {
  
}
