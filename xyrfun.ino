#include<Servo.h>


#define MOTOR_PULSE_ZERO 1000
#define MOTOR_PULSE_180 1940
#define SERVO_PULSE_ZERO 544
#define SERVO_PULSE_180 2300

int valx,valy,valr,speed1,speed2;
Servo rot,x,y,piston,motor1,motor2;
void setup() {
  // put your setup code here, to run once:
rot.attach(10);
x.attach(11);
y.attach(9);
piston.attach(6);
Serial.begin(9600);
startup();
motor1.attach(5);
motor2.attach(3);
servo_test();
enable_motors();
delay(2000);
Serial.flush();
}

void servo_test()
{
  y.write(0);
  delay(1000);
  x.write(125);
  delay(1000);
  x.write(63);
  delay(1000);
  x.write(0);
  delay(1000);
  x.write(63);
  delay(1000);
  rot.write(0);
  y.write(60);
  delay(1000);
  x.write(125);
  y.write(100);
  rot.write(180);
  delay(1000);
  x.write(63);
  y.write(180);
  rot.write(90);
  delay(2000);
}
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

void startup()
{
  rot.write(90);
  x.write(0);
  y.write(180);
  piston.write(180);
  delay(1500);
}
void loop() {
  // put your main code here, to run repeatedly:

  if(Serial.available() == 5)
  { 
   speed1= Serial.parseInt();//analogRead(A0); //Read input from analog pin a0 and store in val
   speed2 = Serial.parseInt();
   speed1 = map(speed1, 0, 1023,1000,2000);
   speed2 = map(speed2, 0, 1023,1000,2000);
    motor1.writeMicroseconds(speed1);
    motor2.writeMicroseconds(speed2);
    valy = Serial.parseInt();
    valy = (valy/9.0)*60+60;
    Serial.print(valy);
    Serial.print(" ");
    valx = Serial.parseInt();
    valx = (valx/12.0)*(-125)+125;
    Serial.println(valx);
    valr = Serial.parseInt();
    
//speed2= Serial.parseInt();
    piston_up();
    y.write(valy);//writeMicroseconds( map(valy,9,0,SERVO_PULSE_ZERO,SERVO_PULSE_180) );//write(valy);
    x.write(valx);//writeMicroseconds( map(valx,0,12,SERVO_PULSE_ZERO,SERVO_PULSE_180) );//write(valx);
    rot.writeMicroseconds( map(valr,0,180,SERVO_PULSE_ZERO,SERVO_PULSE_180) );
   piston_down();
  }
}

void piston_up()
{
  piston.writeMicroseconds( map(5,0,180,SERVO_PULSE_ZERO,SERVO_PULSE_180) );
}

void piston_down()
{
  delay(600);
  piston.writeMicroseconds( map(140,0,180,SERVO_PULSE_ZERO,SERVO_PULSE_180) );
}

