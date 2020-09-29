int right_counter;
int left_counter;


void setup() {
  Serial.begin(9600);
  motor_control_pin_setup();
  motor_sensor_pin_setup();
}

void loop() {
 int spd = 40;
 Serial.print("Reseting counters");
 reset_motor_counters();
 print_motor_counters();
 delay(2000);

 move_motor(spd, 1, 'L');
 move_motor(spd, 1, 'R');
 for (int i=0; i<1000; i++){
     print_motor_counters();
 }
 
 stop_robot();
 Serial.print("Reseting counters");
 reset_motor_counters();
 print_motor_counters();
 delay(2000);
 
 move_motor(spd, 0, 'L');
 move_motor(spd, 0, 'R');
 for (int i=0; i<1000; i++){
     print_motor_counters();
 }
}



