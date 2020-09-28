// Left motor pins
int pin_left_bridge_input1 = 3;
int pin_left_bridge_input2 = 5;
int enable_left_bridge_pin = 4;

// Right motor pins
int pin_right_bridge_input1 = 10;
int pin_right_bridge_input2 = 9;
int enable_right_bridge_pin = 8;

void motor_control_pin_setup(){
  pinMode(pin_left_bridge_input1, OUTPUT);
  pinMode(pin_left_bridge_input2, OUTPUT);
  pinMode(enable_left_bridge_pin, OUTPUT);
  
  
  pinMode(pin_right_bridge_input1, OUTPUT);
  pinMode(pin_right_bridge_input2, OUTPUT);
  pinMode(enable_right_bridge_pin, OUTPUT);
}

void move_motor(int spd, int backward_forward, char L_or_R) {
  if (L_or_R == 'L'){
    digitalWrite(enable_left_bridge_pin, HIGH);
    if (backward_forward == 1){
      digitalWrite(pin_left_bridge_input2, LOW);
      analogWrite(pin_left_bridge_input1, spd);
    } else {
      digitalWrite(pin_left_bridge_input1, LOW);
      analogWrite(pin_left_bridge_input2, spd);
    }
  } else {
    digitalWrite(enable_right_bridge_pin, HIGH);
    if (backward_forward == 1){
      digitalWrite(pin_right_bridge_input2, LOW);
      analogWrite(pin_right_bridge_input1, spd);
    } else {
      digitalWrite(pin_right_bridge_input1, LOW);
      analogWrite(pin_right_bridge_input2, spd);
    }
  }
}

void stop_motor(char L_or_R) {
  if (L_or_R=='L') {
    digitalWrite(enable_left_bridge_pin, LOW);
  } else {
    digitalWrite(enable_right_bridge_pin, LOW);
  }
}

void stop_robot() {
  stop_motor('L');
  stop_motor('R');
}

void move_robot_forward(int spd){
  move_motor(spd, 0, 'L');
  move_motor(spd, 0, 'R');
}

void move_robot_backwards(int spd){
  move_motor(spd, 1, 'L');
  move_motor(spd, 1, 'R');
}

void turn_robot_left(int spd){
  move_motor(spd, 1, 'L');
  move_motor(spd, 0, 'R');
}

void turn_robot_right(int spd){
  move_motor(spd, 0, 'L');
  move_motor(spd, 1, 'R');
}

