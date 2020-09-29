int left_motor_sensor = 11;
int right_motor_sensor = 12;

volatile int left_motor_counter = 0;
volatile int right_motor_counter = 0;
volatile int left_motor_sensor_state = 0;
volatile int right_motor_sensor_state = 0;

void motor_sensor_pin_setup() {
  pinMode(left_motor_sensor, INPUT);
  pinMode(right_motor_sensor, INPUT);
  attachInterrupt(0, add_left_motor_counter_ISR, CHANGE);
  attachInterrupt(0, add_right_motor_counter_ISR, CHANGE);
}

void add_left_motor_counter_ISR(){
  left_motor_sensor_state = digitalRead(left_motor_sensor);
  if (left_motor_sensor_state == 1){
    left_motor_counter += 1;
  }
}

void add_right_motor_counter_ISR(){
  right_motor_sensor_state = digitalRead(right_motor_sensor);
  if (right_motor_sensor_state == 1){
    right_motor_counter += 1;
  }
}

void reset_motor_counters(){
  right_motor_counter = 0;
  left_motor_counter = 0;
}

int get_left_motor_counter(){
  return left_motor_counter;
}

int get_right_motor_counter(){
  return right_motor_counter;
}

void print_motor_counters(){
  right_counter = get_right_motor_counter();
  left_counter = get_left_motor_counter();
  Serial.print('Right motor:');
  Serial.print(right_counter);
  Serial.print('\n');
  Serial.print('Left motor:');
  Serial.print(left_counter);
  Serial.print('\n');
}
