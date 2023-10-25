#include <XY2_100.h>
XY2_100 galvo;

int _DELAY = 2;
int _STEP = 1;

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

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void get_points(uint16_t X[], uint16_t Y[]){
  String text = "";
  // Careful! Bad practise
  int index = 0;
  while(true){
    text = (Serial.readString()).trim();
    // text = Serial.readStringUntil(char terminator)
    if(text == "END" || index == ARRAY_SIZE){
      break;
    }

    String xval = getValue(text, '_', 0);
    String yval = getValue(text, '_', 1);
    // separate string to each: string should look like sX_sY_eX_eY/r/n
    X[index] = (uint16_t)xval.toInt();
    Y[index] = (uint16_t)yval.toInt();
    index += 1;
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
  String command = Serial.readString();
  // Set array size
  if(getValue(command, '_', 0) == "AS"){
  }
  // Get Data
  else if(command == "GD"){
    uint16_t X_POINTS[ARRAY_SIZE];
    uint16_t Y_POINTS[ARRAY_SIZE];
    get_points(X_POINTS,Y_POINTS);
  }

}


