#include <SoftwareSerial.h>
#include <Servo.h>
#include <LCD_I2C.h>
LCD_I2C lcd(0x27, 16, 2);

#define trigPin3 A0                              
#define echoPin3 A1
#define trigPin2 5                             
#define echoPin2 6
#define trigPin1 3                               
#define echoPin1 4                         
#define LED 13                     
 
int servoPin1 = A2;
int servoPin2 = 9;
int servoPin3 = 8;
int servo_state ;
Servo Servo1;Servo Servo2;Servo Servo3;
long duration1, distance1, UltraSensor1;
long duration2, distance2, UltraSensor2;
long duration3, distance3, UltraSensor3;

void setup(){
   lcd.begin();
   lcd.backlight();
Serial.begin(9600);                             
pinMode(trigPin1, OUTPUT);                      
pinMode(echoPin1, INPUT);  
pinMode(trigPin2, OUTPUT);                      
pinMode(echoPin2, INPUT);  
pinMode(trigPin3, OUTPUT);                      
pinMode(echoPin3, INPUT);                        
pinMode(LED, OUTPUT);                     
pinMode(servoPin1, OUTPUT);
Servo1.attach(servoPin3);
Servo2.attach(servoPin2);
Servo3.attach(servoPin1);
Servo1.write(140);
delay(500);
Servo2.write(140);
delay(500);
Servo3.write(140);
delay(500);
digitalWrite(13, LOW);
delay(500);

}

void loop() {
openBin();
ultra_1();
ultra_2();
ultra_3();
}
/////////////////////////////////////////////////////////////////////////////////
void openBin() {
  if (Serial.available()>1) {
    int position = Serial.parseInt();   
    if (position == 1) {
      Servo1.write(140);
      Servo2.write(0);
      Servo3.write(0);
    } else if (position == 2) {
      Servo1.write(0);
      Servo2.write(140);
      Servo3.write(0);
    } else if (position == 3) {
      Servo1.write(0);
      Servo2.write(0);
      Servo3.write(140);
    }
  }
}
/////////////////////////////////////////////////////////////////////////////////
void ultra_1()
{

digitalWrite(trigPin1, LOW);
delayMicroseconds(2);
digitalWrite(trigPin1, HIGH);
delayMicroseconds(10); //
digitalWrite(trigPin1, LOW);
duration1 = pulseIn(echoPin1, HIGH);
distance1= (duration1/2) / 29.1;
delay(10);
UltraSensor1 = distance1; 
if(UltraSensor1 <=10 && UltraSensor1 !=0)
{
lcd.setCursor(0, 0);
lcd.print("D1=");
lcd.setCursor(3, 0);
lcd.print("OPEN");
digitalWrite(13,HIGH);
Serial.println("distance1");
Serial.print(distance1);
Servo1.write(60);
delay(2000);
digitalWrite(13, LOW);

}
else
{
lcd.setCursor(0, 0);
lcd.print("D1=");
lcd.setCursor(3, 0);
lcd.print("CLOS");
digitalWrite(13, LOW);
Serial.println("distance1");
Serial.print(distance1);
Servo1.write(140);
}
delay(100);
}
///////////////////////////////////////////////////////////////////////////////
void ultra_2()
{
digitalWrite(trigPin2, LOW);
delayMicroseconds(2);
digitalWrite(trigPin2, HIGH);
delayMicroseconds(10); //
digitalWrite(trigPin2, LOW);
duration2 = pulseIn(echoPin2, HIGH);
distance2= (duration2/2) / 29.1;
delay(10);
UltraSensor2 = distance2; 
if(UltraSensor2 <=10 && UltraSensor2 !=0)
{
lcd.setCursor(8, 0);
lcd.print("D2=");
lcd.setCursor(12, 0);
lcd.print("OPEN");
digitalWrite(13,HIGH);
Serial.println("distance2");
Serial.print(distance2);
Servo2.write(60);
delay(2000);
digitalWrite(13, LOW);
}
else
{
lcd.setCursor(8, 0);
lcd.print("D2=");
lcd.setCursor(12, 0);
lcd.print("CLOSE");
digitalWrite(13, LOW);
Serial.println("distance2");
Serial.print(distance2);
Servo2.write(140);
}
delay(100);
}
////////////////////////////////////////////////////////////////
void ultra_3()
{

digitalWrite(trigPin3, LOW);
delayMicroseconds(2);
digitalWrite(trigPin3, HIGH);
delayMicroseconds(10); //
digitalWrite(trigPin3, LOW);
duration3 = pulseIn(echoPin3, HIGH);
distance3= (duration3/2) / 29.1;
delay(10);
UltraSensor3 = distance3; 
if(UltraSensor3 <=10 && UltraSensor3 !=0)
{
lcd.setCursor(0, 1);
lcd.print("DUST BIN3=");
lcd.setCursor(12, 1);
lcd.print("OPEN");
digitalWrite(13,HIGH);
Serial.println("distance3");
Serial.print(distance3);
Servo3.write(60);
delay(2000);
digitalWrite(13, LOW);
}
else
{
lcd.setCursor(0, 1);
lcd.print("DUST BIN3=");
lcd.setCursor(12, 1);
lcd.print("CLOSE");
digitalWrite(13, LOW);
Serial.println("distance3");
Serial.print(distance3);
Servo3.write(140);
}
delay(100);
}