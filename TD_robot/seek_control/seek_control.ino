int spd = 240;
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
    } else if (data_from_user == byte('oo')) {
      stop_motor('L');
      stop_motor('R');
    } else if (data_from_user == byte('of')) {
      stop_motor('L');
      move_motor(spd, 0, 'R');
    } else if (data_from_user == byte('ob')) {
      stop_motor('L')
      move_motor(spd, 1, 'R');
    } else if (data_from_user == byte('fo')) {
      move_motor(spd, 0, 'L');
      stop_motor('R')
    } else if (data_from_user == byte('ff')) {
      move_motor(spd, 0, 'L');
      move_motor(spd, 0, 'R');
    } else if (data_from_user == byte('fb')) {
      move_motor(spd, 0, 'L');
      move_motor(spd, 1, 'R');
    } else if (data_from_user == byte('bo')) {
      move_motor(spd, 1, 'L');
      stop_motor('R')
    } else if (data_from_user == byte('bf')) {
      move_motor(spd, 1, 'L');
      move_motor(spd, 0, 'R');
    } else if (data_from_user == byte('bb')) {
      move_motor(spd, 1, 'L');
      move_motor(spd, 1, 'R');
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


