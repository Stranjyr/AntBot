/*
  RFID Eval 13.56MHz Shield example sketch v10
  2/26/14
  Based on code by Aaron Weiss, aaron at sparkfun dot com
  OSHW license: http://freedomdefined.org/OSHW
  Last updated by William Hampton
  University of Alabama
  5-04-14
  
  
  works with 13.56MHz MiFare 1k tags

  Based on hardware v13:
  D7 -> RFID RX
  D8 -> RFID TX
  D9 -> XBee TX
  D10 -> XBee RX

  Note: RFID Reset attached to D13 (aka status LED)

  Note: be sure include the SoftwareSerial lib, http://arduiniana.org/libraries/newsoftserial/

  Usage: Sketch prints "Start, and then either reads a tag or writes a string to a tag (See loop)

*/
//TODO - checksum not working. Cant read or write!
//Update - 5-04-14  possbly fixed checksum. replaced mod 0x100 with a cast to 8 bit. Cannot test until this fall.
#include <SoftwareSerial.h>

SoftwareSerial rfid(7, 8);
SoftwareSerial xbee(10, 9);

//Prototypes
void check_for_notag(void);
void halt(void);
void parse(void);
void print_serial(void);
void read_serial(void);
void seek(void);
void set_flag(void);

//Global var
int flag = 0;
int Str1[50];
char IN[16];
int act = -1;
int b = 1;
//INIT
void setup()
{
  Serial.begin(9600);
  Serial.println("Start");
  Serial.println("Type 'R' to read, or 'W' to write");

  // set the data rate for the SoftwareSerial ports
  xbee.begin(9600);
  rfid.begin(19200);
  delay(10);
  halt();
}

//MAIN
//type 'w' to write to tag, or 'r' to read. will continue to read or write until either 'w' or 'r is typed again.
void loop()
{
  if(Serial.available() > 0)
  {
      Serial.flush();
      char funct = Serial.read();
      
      //Serial.println(act);
      switch(funct)
      {
        case('R'):
        case('r'): Serial.println("Enter which block to read:  ");
                   Serial.flush();
                   while(!Serial.available());//hangs program till intput is recieved
                   b = Serial.parseInt();
                   Serial.println(b);
                   //Serial.println("READ DONE");
                   act = 1;//tells the function is read
                   funct = NULL;
                   break;
        case('W'):
        case('w'): Serial.println("Enter your message to write:  ");
                   {
                   String temp = "";
                   char c;
                   int l = 0;//size of entered string
                   Serial.flush();
                   //builds a string to send to the block
                   while(!Serial.available());//hangs program till intput is recieved
                   while(Serial.available()) {
                        c = Serial.read();
                        temp.concat(c);
                        l++;
                        delay(10);
                    }
                   
                   Serial.println(temp);
                   //reads either first 16 or all chars in temp, whichever is less
                   int cnt = 0;
                  
                   for(cnt = 0; cnt<16 && cnt<l; cnt++)
                   {
                     IN[cnt] = temp[cnt];
                   }
                   //pads IN as needed
                   for(; cnt<16; cnt++)
                   {
                    IN[cnt] = NULL;
                   }
                   
                   Serial.println("Enter a number:  ");
                   Serial.flush();
                   while(!Serial.available());//hangs program till intput is recieved
                   b = Serial.parseInt();
                   Serial.println(b);
                   act = 2; //tells the action is write
                   funct = NULL;
                   }
                   break;
                   
          default: break;
      }
      Serial.flush();
  }
      switch(act)
      {
        case(1): read_Main(b);
                 break;
        case(2): write_Main(IN, b);
                 break;
        default: break;
      }
  
        
}
//not used
void check_for_notag()
{
  seek();
  delay(10);
  parse();
  set_flag();

  if(flag = 1){
    seek();
    delay(10);
    parse(11);
    
    
  }
}
//not used
void halt()
{
 //Halt tag
  rfid.write((uint8_t)255);
  rfid.write((uint8_t)0);
  rfid.write((uint8_t)1);
  rfid.write((uint8_t)147);
  rfid.write((uint8_t)148);
}
//saves return value of RFID to Str1[]. len is the expected number of return bytes
void parse(int len)
{
  while(rfid.available()){
    if(rfid.read() == 255){
      for(int i=1;i<len;i++){
        Str1[i]= rfid.read();
        //Serial.print(Str1[i]);
        
      }
    }
    
  }
  //Serial.print("\n");
}
//prints return of seek. used to verify seek worked
void print_serial()
{
  if(flag == 1){
    Serial.println("SEEK OUT");
    //print to serial port
    Serial.print(Str1[8], HEX);
    Serial.print(Str1[7], HEX);
    Serial.print(Str1[6], HEX);
    Serial.print(Str1[5], HEX);
    Serial.println();
    //print to XBee module
    xbee.print(Str1[8], HEX);
    xbee.print(Str1[7], HEX);
    xbee.print(Str1[6], HEX);
    xbee.print(Str1[5], HEX);
    xbee.println();
    delay(100);
    //check_for_notag();
  }
}
//prints return value of auth. Used to verify auth worked
void print_Auth()
{
  if(flag == 1){
    //print to serial port
    Serial.println("Auth OUT");
   
    Serial.print(Str1[1], HEX);
    Serial.print(Str1[2], HEX);
    Serial.print(Str1[3], HEX);
    Serial.print(Str1[4], HEX);
    Serial.print(Str1[5], HEX);
    Serial.println();
    //print to XBee module
    xbee.print(Str1[8], HEX);
    xbee.print(Str1[7], HEX);
    xbee.print(Str1[6], HEX);
    xbee.print(Str1[5], HEX);
    xbee.println();
    delay(100);
    //check_for_notag();
  }
}
//Prints out return from read_BLock. Used for Verifiing block worked. 
//currently prints char values
void print_Block()
{
  if(flag == 1){
    Serial.println("Read OUT");
    if(Str1[2] == 2)
    {
      Serial.print(Str1[3], HEX);
      Serial.print(Str1[4], HEX);
    }
    else
    {
      for(int y = 5; y<20; y++)
      {
        Serial.print((char)Str1[y]);
        
      }
    }
    Serial.println();
  
    //print to serial port
    
    
    
    delay(100);
    //check_for_notag();
  }
}
//prints out return from write_Block. Used for verifing write_Block worked
void print_Write()
{
  if(flag == 1){
    Serial.println("Write OUT");
    if(Str1[2] == 2)
    {
      Serial.print(Str1[3], HEX);
      Serial.print(Str1[4], HEX);
    }
    else
    {
      for(int y = 3; y<20; y++)
      {
        Serial.print(Str1[y], HEX);
        Serial.print(":");
        
      }
    }
    Serial.println();
  
    //print to serial port
    
    
    
    delay(100);
    //check_for_notag();
  }
}
//reads in block b.
void read_Main(uint8_t b)
{
  
  seek();
  delay(10);
  parse(11);
  set_flag();
  //print_serial();
  
  authenticate(b);
  delay(10);
  parse(6);
  //print_Auth();
  
  
  
  
  
  read_Block(b);
  delay(10);
  parse(20);
  print_Block();
  delay(500);
}
//Input a char array len 16. Writes key to block b
//Padding handled in LOOP
void write_Main(char key[], uint8_t b)
{
  
  seek();
  delay(10);
  parse(11);
  set_flag();
  //print_serial();
  
  authenticate(b);
  delay(10);
  parse(6);
  //print_Auth();
  
  
  write_Block(key, b);
  delay(10);
  parse(20);
  print_Write();
  
  
  
  
}
void seek()
{
  //search for RFID tag
  rfid.write((uint8_t)255);
  rfid.write((uint8_t)0);
  rfid.write((uint8_t)1);
  rfid.write((uint8_t)130);
  rfid.write((uint8_t)131);
  delay(10);
}
//authentiates block b for read/write
void authenticate(uint8_t b)
{
  //search for RFID tag
  uint8_t cksm = 0;
  cksm+=0x85;
  cksm+=b;
  cksm+=0xFF;
  cksm+=0x03;
  
  //Serial.println(cksm);
  rfid.write((uint8_t)255);
  rfid.write((uint8_t)0);
  rfid.write((uint8_t)0x03);
  rfid.write((uint8_t)0x85);
  rfid.write((uint8_t)b);
  rfid.write((uint8_t)0xFF);
  rfid.write((uint8_t)cksm);
  delay(10);
  
}
//reads in authenticated block b
void read_Block(uint8_t b)
{
  //search for RFID tag
  uint8_t cksm = 0;
  cksm+=0x86;
  cksm+=0x02;
  cksm+=b;
  
  rfid.write((uint8_t)255);
  rfid.write((uint8_t)0);
  rfid.write((uint8_t)0x02);
  rfid.write((uint8_t)0x86);
  rfid.write((uint8_t)b);
  rfid.write((uint8_t)cksm);
  delay(10);
  
}

//writes AAAAAAAAAAAAAAA to block b. Used for testing
void write_Block(uint8_t b)
{
  //search for RFID tag
  
  rfid.write((uint8_t)255);
  rfid.write((uint8_t)0);
  rfid.write((uint8_t)0x12);
  rfid.write((uint8_t)0x89);
  rfid.write((uint8_t)b);
  rfid.write((uint8_t)0x01);//1
  rfid.write((uint8_t)0x01);//2
  rfid.write((uint8_t)0x01);//3
  rfid.write((uint8_t)0x01);//4
  rfid.write((uint8_t)0x01);//5
  rfid.write((uint8_t)0x01);//6
  rfid.write((uint8_t)0x01);//7
  rfid.write((uint8_t)0x01);//8
  rfid.write((uint8_t)0x01);//9
  rfid.write((uint8_t)0x01);//10
  rfid.write((uint8_t)0x01);//11
  rfid.write((uint8_t)0x01);//12
  rfid.write((uint8_t)0x01);//13
  rfid.write((uint8_t)0x01);//14
  rfid.write((uint8_t)0x01);//15
  rfid.write((uint8_t)0x01);//16
  rfid.write((uint8_t)0xAD);//checksum
  delay(10);
  
}
//write a 16 bit char array to block b
void write_Block(char key[], uint8_t b)
{
  //search for RFID tag
  uint8_t chk = 0;//checksum
  rfid.write((uint8_t)255);
  rfid.write((uint8_t)0);
  rfid.write((uint8_t)0x12);
  rfid.write((uint8_t)0x89);
  rfid.write((uint8_t)b);
  chk+=(uint8_t)0x89;
  chk+=(uint8_t)0x12;
  chk+=b;
  for(int a = 0; a<16; a++)
  {
    rfid.write((uint8_t)key[a]);
    chk+=(uint8_t)key[a];
  }
  
  
  //Serial.println(chk);
  rfid.write((uint8_t)chk);//checksum
  delay(10);
  
}

void set_flag()
{
  if(Str1[2] == 6){
    flag++;
  }
  if(Str1[2] == 2){
    flag = 0;
  }
}
