#include <XY2_100.h>
XY2_100 galvo;

int _DELAY = 2;
int _STEP = 1;

uint16_t START_X[] = {};
uint16_t START_Y[] = {};
uint16_t END_X[] = {};
uint16_t END_Y[] = {};
int ARRAY_SIZE = 0; // should be first signal sent from PC

void draw_line(uint16_t start_x, uint16_t start_y, uint16_t end_x, uint16_t end_y, int data_length){
  // data_length = how many data points from start to end

  uint16_t x = start_x;
  uint16_t y = start_y;

  uint16_t step_x = 0;
  uint16_t step_y = 0;
  if(end_x > start_x && end_y > start_y){
    step_x = (uint16_t)((end_x-start_x)/(data_length));
    step_y = (uint16_t)((end_y-start_y)/(data_length));
  }
  else if(end_x < start_x && end_y > start_y){
    step_x = (uint16_t)(-(end_x-start_x)/(data_length));
    step_y = (uint16_t)((end_y-start_y)/(data_length));
  }
  else if(end_x > start_x && end_y < start_y){
    step_x = (uint16_t)((end_x-start_x)/(data_length));
    step_y = (uint16_t)(-(end_y-start_y)/(data_length));
  }
  else{
    step_x = (uint16_t)(-(end_x-start_x)/(data_length));
    step_y = (uint16_t)(-(end_y-start_y)/(data_length));
  }

  // prevent STOP mode
  if(step_x == 0){
    step_x = 1;
  }
  if(step_y ==0){
    step_y = 1;
  }

  galvo.setPos(x,y);
  // State machine for each case
  if(end_x > start_x && end_y > start_y){
      while(x < end_x && y < end_y){
        x += step_x;
        y += step_y;
        galvo.setPos(x,y);
        delay(_DELAY);
      }
  }
  else if(end_x < start_x && end_y > start_y){
      while(x > end_x && y < end_y){
        x -= step_x;
        y += step_y;
        galvo.setPos(x,y);
        delay(_DELAY);
      }
  }
  else if(end_x > start_x && end_y < start_y){
      while(x < end_x && y > end_y){
        x += step_x;
        y -= step_y;
        galvo.setPos(x,y);
        delay(_DELAY);
      }
  }
  else{
      while(x > end_x && y > end_y){
        x -= step_x;
        y -= step_y;
        galvo.setPos(x,y);
        delay(_DELAY);
      }
  }
  galvo.setPos(end_x,end_y);
  

}

void get_points(){
  uint16_t X[ARRAY_SIZE];
  *START_X = &X;
  START_Y = new uint16_t[ARRAY_SIZE];

  String text = "";
  // Careful! Bad practise
  while(true){
    text = Serial.readString();
    // text = Serial.readStringUntil(char terminator)
    if(text.trim() == "END"){
      break;
    }

    // separate string to each: string should look like sX_sY_eX_eY/r/n
    char *ptr; // declare a ptr pointer  
    ptr = strtok(text.trim(), "_"); // use strtok() function to separate string using comma (,) delimiter.   
    // use while loop to check ptr is not null  
    int i = 0;
    while (ptr != NULL)  
    {  
        cout << ptr  << endl; // print the string token  
        ptr = strtok (NULL, "_");  
        if(i==0){
          START_X.append((uint16_t)ptr);
        }
        else if(i==1){
          START_Y.append((uint16_t)ptr);
        }
        else if(i==2){
          END_X.append((uint16_t)ptr);
        }
        else{
          END_Y.append((uint16_t)ptr);
        }
        i+=1;
    }  
  }
}

void set_array_size(int size){
  ARRAY_SIZE = size;
}

void append_points(uint16_t x, uint16_t y){
  ARRAY_SIZE += 1;

}

/*
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
*/



void setup() {
  galvo.begin();
  galvo.setPos(0,0);
}

void loop() {


}


