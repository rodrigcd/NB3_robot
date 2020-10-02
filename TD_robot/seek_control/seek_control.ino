int spd = 240;
int led_state = 0;
int led_pin=13;

void setup() {
  Serial.begin(9600);
  motor_control_pin_setup();
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, LOW);
}

void loop() {
  if(Serial.available() > 0)
  {
    char data_from_user=Serial.read();
    Serial.print(data_from_user);
    if (data_from_user == byte('led')){
      change_led();
    } else if (data_from_user == byte('s')) {
      digitalWrite(led_pin, LOW);
    } else if (data_from_user == byte('0')) {
      stop_motor('L');
      stop_motor('R');
    } else if (data_from_user == byte('1')) {
      stop_motor('L');
      move_motor(spd, 0, 'R');
    } else if (data_from_user == byte('2')) {
      stop_motor('L');
      move_motor(spd, 1, 'R');
    } else if (data_from_user == byte('3')) {
      move_motor(spd, 0, 'L');
      stop_motor('R');
    } else if (data_from_user == byte('4')) {
      move_motor(spd, 0, 'L');
      move_motor(spd, 0, 'R');
    } else if (data_from_user == byte('5')) {
      move_motor(spd, 0, 'L');
      move_motor(spd, 1, 'R');
    } else if (data_from_user == byte('6')) {
      move_motor(spd, 1, 'L');
      stop_motor('R');
    } else if (data_from_user == byte('7')) {
      move_motor(spd, 1, 'L');
      move_motor(spd, 0, 'R');
    } else if (data_from_user == byte('8')) {
      move_motor(spd, 1, 'L');
      move_motor(spd, 1, 'R');
    }
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


