#include <SPI.h>
#include <mcp2515.h>
#include <stdlib.h>

#define potPin A0
int potvalue=0;
int new_potvalue=0;
int LED = 3;
int LED1 = 4;

struct can_frame canMsg;
struct can_frame canMsg1;

MCP2515 mcp2515(10);


void setup() {
  canMsg1.can_id  = 0x0F6;
  canMsg1.can_dlc = 2;
  //canMsg1.data[0] = 0x8E;
  canMsg1.data[1] = 0x87;
  
  while (!Serial);
  Serial.begin(115200);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS);
  mcp2515.setNormalMode();
  
  //Serial.println("Example: Write to CAN");
  //Serial.println("------- CAN Read ----------");
  //Serial.println("ID  DLC   DATA");
}

void loop() {

  potvalue = analogRead(potPin);
  potvalue = map(potvalue,0,2047,0,511);
  analogWrite (LED, potvalue);
  //Serial.println(potvalue);
  canMsg1.data[0] = potvalue;

  //Serial.println("Messages sent");
  mcp2515.sendMessage(&canMsg1);
  delay(100);

  if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
    //Serial.print(canMsg.can_id, HEX); // print ID
    //Serial.print(" "); 
    //Serial.print(canMsg.can_dlc, HEX); // print DLC
    //Serial.print(" ");
    if(canMsg.can_id==0x0F6){
      int x = canMsg.data[0];
      //Serial.print(x);
      analogWrite (LED1, x);
      
      }      
  }
}
