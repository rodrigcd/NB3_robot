int base_speed = 200;
int led_state = 0;
int led_pin=13;

void setup() {
  Serial.begin(9600);
  motor_control_pin_setup();
  pinMode(led_pin, OUTPUT);
}

void loop() {
  if(Serial.available() > 0)
  {
    char data_from_user=Serial.read();
    if (data_from_user == byte('led')){
      change_led();
    } else if (data_from_user == byte('rig')) {
      turn_robot_right(base_speed);
    } else if (data_from_user == byte('lef')) {
      turn_robot_left(base_speed);
    } else if (data_from_user == byte('for')) {
      move_robot_forward(base_speed);
    } else if (data_from_user == byte('bac')) {
      move_robot_backwards(base_speed);
    } else if (data_from_user == byte('res')) {
      stop_robot();
    }
    Serial.print(data_from_user);
  }

}

void change_led(){
  if (led_state == 0){
    led_state = 1;
    digitalWrite(led_pin, HIGH);
  } else {
    led_state = 0;
    digitalWrite(led_pin, LOW);
  }
}

