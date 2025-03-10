#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <Wire.h>
#include <LCD_I2C.h>

#define BLYNK_TEMPLATE_ID "TMPL33ck1ocY4"
#define BLYNK_TEMPLATE_NAME "smart dust bin "
#define BLYNK_AUTH_TOKEN "bXlIvzpcT-hGUwGnmXeITmfEQthb9tYD"
#define BLYNK_PRINT Serial

LCD_I2C lcd(0x27, 16, 2);
#define trigPin1 D6
#define echoPin1 D7
#define trigPin2 D5
#define echoPin2 D3
#define trigPin3 D0
#define echoPin3 D8
#define VPIN_BUTTON_1 V12

int servoPin = D4;
int servo_state;
int mode = 0;
char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "JMD";
char pass[] = "1234@5678";
//WidgetLCD lcd(V1);
long duration, distance1, distance2, distance3, UltraSensor1, UltraSensor2, UltraSensor3;
char data;
String SerialData = "";

void setup() {
  lcd.begin();
  lcd.backlight();
  delay(500);
  lcd.clear();
  Serial.begin(9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);
  pinMode(servoPin, OUTPUT);
  Blynk.begin(auth, ssid, pass);
}

void loop() {
  dustbin1_read();
  dustbin2_read();
  dustbin3_read();
  notification();
  Blynk.run();
}

void SonarSensor1() {
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  duration = pulseIn(echoPin1, HIGH);
  distance1 = (duration / 2) / 29.1;
  UltraSensor1 = distance1;
}
void SonarSensor2() {
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  duration = pulseIn(echoPin2, HIGH);
  distance2 = (duration / 2) / 29.1;
  UltraSensor2 = distance2;
}
void SonarSensor3() {
  digitalWrite(trigPin3, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW);
  duration = pulseIn(echoPin3, HIGH);
  distance3 = (duration / 2) / 29.1;
  UltraSensor3 = distance3;
}

void dustbin1_read() {
  SonarSensor1();
  if (UltraSensor1 < 3) {
    UltraSensor1 = 10;
    UltraSensor1 = UltraSensor1 * 10;
    Blynk.virtualWrite(V0, UltraSensor1);
    Serial.println("Dustbin1=");
    Serial.print(UltraSensor1);
    lcd.setCursor(0, 0);
    lcd.print("D1=");
    lcd.print("    ");
    lcd.setCursor(3, 0);
    lcd.print(UltraSensor1);
    delay(10);
  } else if (UltraSensor1 > 10) {
    UltraSensor1 = 0;
    Blynk.virtualWrite(V0, UltraSensor1);
    Serial.println("Dustbin1=");
    Serial.print(UltraSensor1);
    lcd.setCursor(0, 0);
    lcd.print("D1=  ");
    lcd.print("    ");
    lcd.setCursor(3, 0);
    lcd.print(UltraSensor1);
    delay(10);
  }
  else {
    UltraSensor1 = UltraSensor1 * 10;
    Blynk.virtualWrite(V0, UltraSensor1);
    Serial.println("Dustbin1=");
    Serial.print(UltraSensor1);
    lcd.setCursor(0, 0);
    lcd.print("D1=  ");
    lcd.print("    ");
    lcd.setCursor(3, 0);
    lcd.print(UltraSensor1);
    delay(10);
  }
}

void dustbin2_read() {
  SonarSensor2();
  if (UltraSensor2 < 3) {
    UltraSensor2 = 10;
    UltraSensor2 = UltraSensor2 * 10;
    Blynk.virtualWrite(V1, UltraSensor2);
    Serial.println("Dustbin2=");
    Serial.print(UltraSensor2);
    lcd.setCursor(7, 0);
    lcd.print("D2=");
    lcd.print("    ");
    lcd.setCursor(11, 0);
    lcd.print(UltraSensor2);
    delay(10);
  } else if (UltraSensor2 > 10) {
    UltraSensor2 = 0;
    Blynk.virtualWrite(V1, UltraSensor2);
    Serial.println("Dustbin2=");
    Serial.print(UltraSensor2);
    lcd.setCursor(7, 0);
    lcd.print("D2=  ");
    lcd.print("    ");
    lcd.setCursor(11, 0);
    lcd.print(UltraSensor2);
    delay(10);
  }
  else {
    UltraSensor2 = UltraSensor2 * 10;
    Blynk.virtualWrite(V1, UltraSensor2);
    Serial.println("Dustbin2=");
    Serial.print(UltraSensor2);
    lcd.setCursor(7, 0);
    lcd.print("D2=  ");
    lcd.print("    ");
    lcd.setCursor(11, 0);
    lcd.print(UltraSensor2);
    delay(10);
  }
}

void dustbin3_read() {
  SonarSensor3();
  if (UltraSensor3 < 3) {
    UltraSensor3 = 10;
    UltraSensor = UltraSensor * 10;
    Blynk.virtualWrite(V1, UltraSensor);
    Serial.println("Dustbin=");
    Serial.print(UltraSensor);
    lcd.setCursor(14, 0);
    lcd.print("D=");
    lcd.print("    ");
    lcd.setCursor(17, 0);
    lcd.print(UltraSensor);
    delay(10);
  } else if (UltraSensor > 10) {
    UltraSensor = 0;
    Blynk.virtualWrite(V1, UltraSensor);
    Serial.println("Dustbin=");
    Serial.print(UltraSensor);
    lcd.setCursor(14, 0);
    lcd.print("D=  ");
    lcd.print("    ");
    lcd.setCursor(17, 0);
    lcd.print(UltraSensor);
    delay(10);
  }
  else {
    UltraSensor = UltraSensor * 10;
    Blynk.virtualWrite(V1, UltraSensor);
    Serial.println("Dustbin=");
    Serial.print(UltraSensor);
    lcd.setCursor(14, 0);
    lcd.print("D=  ");
    lcd.print("    ");
    lcd.setCursor(17, 0);
    lcd.print(UltraSensor);
    delay(10);
  }
}
