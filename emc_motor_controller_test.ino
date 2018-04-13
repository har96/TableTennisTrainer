#include <Servo.h>//Using servo library to control ESC


struct tabel_tennis
{
    int x;
    int y;
    int motor1_speed;
    int motor2_speed;
    int rotate;
    int piston;
    char spin;
   
}info;

Servo motor1; //Creating a servo class with name as esc
Servo motor2;
Servo rot;
void setup()
{
motor1.attach(9); //Specify the esc signal pin,Here as D8
motor2.attach(10);
rot.attach(11);


enable_motors();
delay(2000);

Serial.begin(9600);
Serial.flush();
}


int speed1,speed2, angle, x, y; 


char spintype;
bool modecheck = false;
char gamemode;

void enable_motors()
{
  motor1.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  
  //delay(2000); dont need these anymore
  
  //motor1.writeMicroseconds(2000); //initialize the signal to 1000
  //motor2.writeMicroseconds(2000);
  
  delay(1000);
  
  speed1= map(0, 0, 1023,1000,2000);
  motor1.writeMicroseconds(speed1);
  motor2.writeMicroseconds(speed1);
  
  
}
void loop()
{
//get play style : easy, medium, hard
while(modecheck != true)
{
difficulty();
}

if(Serial.available() == 4 )
{
speed1= Serial.parseInt();//analogRead(A0); //Read input from analog pin a0 and store in val 

speed2= Serial.parseInt();

angle= Serial.parseInt();// the rotation servo
info.rotate = angle;

spintype = Serial.parseInt(); // character

info.spin = spintype;


switch(spintype)
{
  case 'b': case 'B':
  {
    backspin();
    break;
  }

  case 't': case 'T':
  {
    topspin();
    break;
  }

  case 'l': case 'L':
  {
    sidespin(spintype);
    break;
  }

  case 'r': case 'R':
  {
    sidespin(spintype);
    break;
  }
}


Serial.print(speed1);
speed1 = map(speed1, 0, 1023,1000,2000);
Serial.print(' ');
Serial.println(speed1);
info.motor1_speed = speed1;

;//analogRead(A0); //Read input from analog pin a0 and store in val 
Serial.print(speed2);
speed2 = map(speed2, 0, 1023,1000,2000);
Serial.print(' ');
Serial.println(speed2);
info.motor2_speed = speed2;

Serial.print(angle);
Serial.print(' ');
Serial.println(angle);
Serial.println(spintype);
Serial.println();


set_motor1();
set_motor2();

set_rotation();
set_x();
set_y();
set_motor1();
set_motor2();
//set_piston();
delay(1500); // to set the servos: will give them enogh time to change position
}
} 




void difficulty()
{
  char dif;
  if(Serial.available()==1)
  {
    dif = Serial.read(); // e for easy i for intermediate and h for hard
  
    if(dif == 'e' || dif == 'E')
    {
      Serial.println("Easy");
      gamemode = 'e';
      modecheck = true;
    }

    else if( dif == 'i' || dif == 'I')
    { 
      Serial.println("Intermediate");
      gamemode = 'i';
      modecheck = true;
    }

    else if ( dif == 'h' || dif == 'H')
    {
      Serial.println("Hard");
      gamemode = 'h';
      modecheck = true;
    }
  }
}

void set_rotation()
{
  rot.write(info.rotate);
}

void set_x()
{
  
}

void set_y()
{
  
}

void set_motor1()
{
  motor1.writeMicroseconds(info.motor1_speed);
}

void set_motor2()
{
  motor2.writeMicroseconds(info.motor2_speed);
}

void topspin()
{
  Serial.println("topspin");
}

void backspin()
{
  Serial.println("backspin");
}

void sidespin(char type)
{
  if(type == 'r' || type == 'R')
  {
    Serial.println("rightspin");
  }

  else if ( type == 'l' || type == 'L')
  {
    Serial.println("leftspin");
  }
}

