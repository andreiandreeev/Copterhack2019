#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
//////////////////////CONFIGURATION///////////////////////////////
#define CHANNEL_NUMBER 6  //set the number of chanels
#define CHANNEL_DEFAULT_VALUE 1500  //set the default servo value
#define FRAME_LENGTH 22500  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PULSE_LENGTH 300  //set the pulse length
#define onState 1  //set polarity of the pulses: 1 is positive, 0 is negative
#define sigPin 10  //set PPM signal output pin on the arduino

/*this array holds the servo values for the ppm signal
 change theese values in your code (usually servo values move between 1000 and 2000)*/
int ppm[CHANNEL_NUMBER];
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";


void setup(){  
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  Serial.println("Setup");
  
  //initiallize default ppm values
  for(int i=0; i<CHANNEL_NUMBER; i++){
      ppm[i]= CHANNEL_DEFAULT_VALUE;
  }
  pinMode(7, INPUT);
  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, !onState);  //set the PPM signal pin to the default state (off)
 // Serial.print("SETUP");
  //delay(2000);
  
  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;
  
  OCR1A = 100;  // compare match register, change this
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();

}

  int throttle = 1500;
  int yaw      = 1500;
  int pitch    = 1500;
  int roll     = 1500;
  int aux1     = 1500;
  int aux2     = 1500;
  int camroll  = 1500;
  int campitch = 1500;

void loop(){
   
   if(radio.available())
   {
     char message[24] = "";
     radio.read(&message, sizeof(message));
     Serial.println(message);
     
     String throttlestr = String(message[0])  + String(message[1]) + String(message[2])   + String(message[3]);
     String yawstr      = String(message[4])  + String(message[5]) + String(message[6])   + String(message[7]);
     String pitchstr    = String(message[8])  + String(message[9]) + String(message[10])  + String(message[11]);
     String rollstr     = String(message[12]) + String(message[13]) + String(message[14]) + String(message[15]);
     String armstr      = String(message[16]) + String(message[17]) + String(message[18]) + String(message[19]);
     String camstr      = String(message[20]) + String(message[21]) + String(message[22]) + String(message[23]);
     //Serial.println(throttlestr + " " + yawstr + " " + pitchstr + " " + rollstr + " " + armstr);
     throttle = throttlestr.toInt();
     yaw      = yawstr.toInt();
     pitch    = pitchstr.toInt();
     roll     = rollstr.toInt();
     aux1     = armstr.toInt();
     camroll  = camstr.toInt();
     
   }

   ppm[0] = roll;
   ppm[1] = pitch;
   ppm[3] = yaw;
   ppm[2] = throttle;
   ppm[4] = aux1;
   ppm[5] = camroll;
}

ISR(TIMER1_COMPA_vect){  //leave this alone
  static boolean state = true;
  
  TCNT1 = 0;
  
  if (state) {  //start pulse
    digitalWrite(sigPin, onState);
    OCR1A = PULSE_LENGTH * 2;
    state = false;
  } else{  //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;
  
    digitalWrite(sigPin, !onState);
    state = true;

    if(cur_chan_numb >= CHANNEL_NUMBER){
      cur_chan_numb = 0;
      calc_rest = calc_rest + PULSE_LENGTH;// 
      OCR1A = (FRAME_LENGTH - calc_rest) * 2;
      calc_rest = 0;
    }
    else{
      OCR1A = (ppm[cur_chan_numb] - PULSE_LENGTH) * 2;
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
}

