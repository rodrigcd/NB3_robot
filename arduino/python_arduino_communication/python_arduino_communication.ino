int datafromUser=0;
int led_pin=13;
void setup() {
  Serial.begin(9600); // use the same baud-rate as the python side
  pinMode(led_pin , OUTPUT);  
}

void loop() {
  //arduino2python();
  python2arduino();
}

// Source: https://www.instructables.com/id/Arduino-Python-Communication-via-USB/
void arduino2python(){
  	Serial.println("Hello world from Ardunio!"); // write a string
	delay(1000);
}

// Source https://create.arduino.cc/projecthub/Jalal_Mansoori/python3-and-arduino-communication-c33192
void python2arduino(){
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0)
  {
    datafromUser=Serial.read();
  }

  if(datafromUser == '1')
  {
    digitalWrite(led_pin, HIGH );
  }
  else if(datafromUser == '0')
  {
    digitalWrite(led_pin, LOW);
  }
}

