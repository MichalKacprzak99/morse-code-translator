/*
 Turns on and off a T010111 LED Module connected to O0,
 when pressing a T000180 Button Module attached to I0.
 http://www.tinkerkit.com/button/
 http://www.tinkerkit.com/led-green-10mm/

 This example code is in the public domain.

 created in Dec 2011
 by Federico Vanzati
 modified in Jun 2013
 by Matteo Loglio<http://matlo.me>

 based on  http://www.arduino.cc/en/Tutorial/Button
 */

// include the TinkerKit library
#include <TinkerKit.h>

TKButton button(I0);	// creating the object 'button' that belongs to the 'TKButton' class 
                        // and giving the value to the desired input pin


void setup() {
//nothing here
Serial.begin(9600);
}

void loop()
{
  // check the switchState of the button
                    

  if (button.readSwitch() == HIGH) {	  
    Serial.print(1); 
  } 
  else {			
    Serial.print(0); 
  }
  delay(100);   
}
