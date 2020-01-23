void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
  pinMode(5, OUTPUT);

}

int distance = 0;
double buttonPress = 0;
double val1 = 1200 / 145;
double val2 = 1200 / 150;
double val3 = 1200 / 145;
double val4 = 1200 / 155;
double val5 = 1200 / 150;
double val6 = 1200 / 150;
double val7 = 1200 / 150;
double val8 = 1200 / 155;
double val9 = 1200 / 155;
double val10 = 1200 / 155;
double val11 = 1200 / 155;
int tap;
int count = 1;


void loop() 
{
  // put your main code here, to run repeatedly:

 
  if (Serial.available() > 0)
  { // only send data back if data has been sent
    distance = Serial.parseInt(); // read the incoming data
  }

    if (distance != 0)
    {
      delay(100); // delay for 1/10 of a second

      if(distance < 10)
        buttonPress = distance * val1;
      else if(distance < 20)
        buttonPress = distance * val2;
      else if(distance < 30)
        buttonPress = distance * val3;
      else if(distance < 40)
        buttonPress = distance * val4;
      else if(distance < 50)
        buttonPress = distance * val5;
      else if(distance < 60)
        buttonPress = distance * val6;
      else if(distance < 70)
        buttonPress = distance * val7;
      else if(distance < 80)
        buttonPress = distance * val8;
      else if(distance < 90)
        buttonPress = distance * val9;
      else if(distance < 100)
        buttonPress = distance * val10; 
      else
        buttonPress = distance * val11;        
      

      tap = (int) buttonPress;

      digitalWrite(5, HIGH);
      delay(tap);

      digitalWrite(5, LOW);
      delay(tap);

    }

  }
