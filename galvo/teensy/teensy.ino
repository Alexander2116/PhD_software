#include <XY2_100.h>
XY2_100 galvo;

int _DELAY = 2;
int _STEP = 1;

int[] START_X = [];
int[] START_Y = [];
int[] END_X = [];
int[] END_Y = [];

void draw_line(uint16_t start_x, uint16_t start y, uint16_t end_x, uint16_t end_y){

}

void get_points(){

}

// actually x and y are inverted (function name indicated actual movement)
void line_y_down(uint16_t initial_x, uint16_t initial_y, int length=4000, int step = 5){

  uint16_t in_x = initial_x;
  galvo.setPos(initial_x, initial_y);
  for(uint16_t x= initial_x; x<(length+initial_x); x += step){
    in_x -= step;
    galvo.setPos(in_x, initial_y);
    delay(_DELAY);
  }
}
void line_y_up(uint16_t initial_x, uint16_t initial_y, int length=4000, int step = 5){

  uint16_t in_x = initial_x;
  galvo.setPos(initial_x, initial_y);
  for(uint16_t x= initial_x; x<(length+initial_x); x += step){
    in_x += step;
    galvo.setPos(in_x, initial_y);
    delay(_DELAY);
  }
}

  
void line_x_left(uint16_t initial_x, uint16_t initial_y, int length=4000, int step = 5){

  uint16_t in_y = initial_y;
  galvo.setPos(initial_x, initial_y);
  for(uint16_t y= initial_y; y<(length+initial_y); y+= step){
    in_y -= step;
    galvo.setPos(initial_x, in_y);
    delay(_DELAY);
  }
}
void line_x_right(uint16_t initial_x, uint16_t initial_y, int length=4000, int step = 5){

  uint16_t in_y = initial_y;
  galvo.setPos(initial_x, initial_y);
  for(uint16_t y= initial_y; y<(length+initial_y); y+= step){
    in_y += step;
    galvo.setPos(initial_x, in_y);
    delay(_DELAY);
  }
}

void line_xy(uint16_t initial_x, uint16_t initial_y, int length=4000, int step = 5){
  uint16_t x = initial_x;
  uint16_t y_in = initial_y;
  galvo.setPos(initial_x, initial_y);
  for(uint16_t y= initial_y; y<(length+initial_y); y+= step){
    x += step;
    y_in += step;
    galvo.setPos(x, y_in);
    delay(_DELAY);
  }
}




void setup() {
  galvo.begin();
  galvo.setPos(1000,3000);
}

void loop() {
  uint16_t Len = 4000;
  line_xy(1000,3000, Len, _STEP);
  line_x(1000+Len,3000+Len, Len, _STEP);
  line_y(1000,3000+Len, Len, _STEP);
  //const uint16_t pause = 1;

}


