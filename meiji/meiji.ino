/*
    Name:       button.ino
    Created:    2018/9/21 14:06:15
    Author:     sakabin
*/

#include <M5Stack.h>
int PIN3  = 2; //To Asist Hand
int PIN4  = 5;//To 脳波計

// The setup() function runs once each time the micro-controller starts
void setup() {
  
  // init lcd, serial, but don't init sd card
  M5.begin(true, false, true);
  
  /*
    Power chip connected to gpio21, gpio22, I2C device
    Set battery charging voltage and current
    If used battery, please call this function in your project
  */
  M5.Power.begin();
  pinMode(PIN3, OUTPUT);
  pinMode(PIN4, OUTPUT);
 

  M5.Lcd.clear(BLACK);
  M5.Lcd.setTextColor(YELLOW);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(65, 10);
  M5.Lcd.println("Button example");
  M5.Lcd.setCursor(3, 35);
  M5.Lcd.println("Press button B for 700ms");
  M5.Lcd.println("to clear screen.");
  M5.Lcd.clear(BLACK);
  M5.Lcd.setTextSize(10);
  M5.Lcd.setCursor(0, 0);
 
}

// Add the main program code into the continuous loop() function
void loop() {
  // update button state
  M5.update();
  
  // if you want to use Releasefor("was released for"), use .wasReleasefor(int time) below
  if (M5.BtnA.wasReleased()) {
    M5.Lcd.setCursor(50, 80);
    M5.Lcd.clear(BLACK);
    digitalWrite(PIN3, HIGH);
    delay(3000);
    digitalWrite(PIN3, LOW);
    delay(100);
    digitalWrite(PIN3, HIGH);
    delay(100);
    digitalWrite(PIN3, LOW);  

    
  } else if (M5.BtnB.wasReleased()) {
    M5.Lcd.setCursor(50, 80);
    M5.Lcd.clear(BLACK);
    M5.Lcd.print('B');
  } else if (M5.BtnC.wasReleased()) {
    M5.Lcd.setCursor(50, 80);
    M5.Lcd.clear(BLACK);
    M5.Lcd.print('C');
  }
  if (Serial.available()) {
    String text = Serial.readStringUntil(0x0a);
    if (text.length() > 0 && text.startsWith("*")) {
      text.trim();
      text.replace("*",""); 
    }
    String input = text;
    if(input=="a") {
        digitalWrite(PIN4, HIGH);
        M5.Lcd.clear(BLACK);
        M5.Lcd.print('a');
    }
    if (input == "0") {
      digitalWrite(PIN4, LOW);//(動画再生中)   
    }
     if (input == "1") { //アシストハンド動かす
    digitalWrite(PIN3, HIGH);
     delay(3000);
     digitalWrite(PIN3, LOW);
     delay(100);
     digitalWrite(PIN3, HIGH);
     delay(100);
     digitalWrite(PIN3, LOW);   
    }
    if (input == "9") { //リセット
     digitalWrite(PIN3, HIGH);
     delay(3000);
     digitalWrite(PIN3, LOW);
     delay(100);
     digitalWrite(PIN3, HIGH);
     delay(100);
     digitalWrite(PIN3, LOW);   
     }
    
  }  

}
