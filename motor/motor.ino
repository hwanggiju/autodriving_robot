#include <math.h>

#define encoderPinA         2
#define encoderPinB         3
#define encoderPinC         18
#define encoderPinD         19

#define led                 13

#define wheel_radius        6 //반지름
#define robot_wheel_pitch   40 //로봇 바퀴 간격
#define encoder_PPR         26
#define Gear_ratio          139
#define Quadrature          2

#define gear                0.2
#define volume              0.2
#define diameter            12      // 무슨 값인지
#define pulse               7238

const float right_error     =   0;
const float left_error      =   0;
const float one_angle       =   2.73 * 41; //바퀴가 한바퀴 돌 때(양 쪽 모터 방향 반대) 각도

long nowTime = millis();
long preTime = nowTime;

char SerialData[1];

int unitScale = 5;

bool testMode = false;

// 모터 드라이버 핀 번호
int driverPwmL  = 6;
int driverIn1   = 7;
int driverIn2   = 8;
int driverIn3   = 9;
int driverIn4   = 10;
int driverPwmR  = 11;

int a, b, c, d;

float speedL = 100, speedR = 100; //바퀴 속도

long encoderPosL = 0;
long encoderPosR = 0;

float newpositionX, newpositionY;

float vel_robot, d_robot;
float dot_seta;
float robot_seta = PI / 2;
float robot_X = 0, robot_Y = 0, robot_R = 0;
float robot_seta_radian = 0, origin_setha;

float del_t = 0;
float newposition1, newposition1_old, vel_motor1;
float newposition2, newposition2_old, vel_motor2;

float calcultor(float newposition1, float newposition2, float del_t);

float angleCalculator(float newpositionX, float newpositionY);

float distanceCalculator(float newpositionX, float newpositionY);

float x = 0, y = 0, z = 0, originL = 0, originR = 0, setha = 0, disL = 0, disR = 0, angleL = 0, angleR = 0, distance = 0;

float sumx = 0; // 총 x의 값
float sumy = 0; // 총 y의 값
float sumz = 0; // 총 z의 값

void boardInitial() {
  pinMode(driverPwmL, OUTPUT);
  pinMode(driverPwmR, OUTPUT);
  pinMode(driverIn1, OUTPUT);
  pinMode(driverIn2, OUTPUT);
  pinMode(driverIn3, OUTPUT);
  pinMode(driverIn4, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP);
  pinMode(encoderPinC, INPUT_PULLUP);
  pinMode(encoderPinD, INPUT_PULLUP);

  digitalWrite(driverIn1, LOW);
  digitalWrite(driverIn2, LOW);
  digitalWrite(driverIn3, LOW);
  digitalWrite(driverIn4, LOW);
  analogWrite(driverPwmL, 0);
  analogWrite(driverPwmR, 0);
}

void driverSet(int Lpwm, int in1, int in2, int in3, int in4, int Rpwm) {
  digitalWrite(driverIn1, LOW);
  digitalWrite(driverIn2, LOW);
  digitalWrite(driverIn3, LOW);
  digitalWrite(driverIn4, LOW);
  in1 = (in1 > 1) ? 1 : in1;
  in2 = (in2 > 1) ? 1 : in2;
  in3 = (in3 > 1) ? 1 : in3;
  in4 = (in4 > 1) ? 1 : in4;
  in1 = (in1 < 0) ? 0 : in1;
  in2 = (in2 < 0) ? 0 : in2;
  in3 = (in3 < 0) ? 0 : in3;
  in4 = (in4 < 0) ? 0 : in4;
  Lpwm = (Lpwm > 255) ? 255 : Lpwm;
  Rpwm = (Rpwm > 255) ? 255 : Rpwm;
  Lpwm = (Lpwm < 0) ? 0 : Lpwm;
  Rpwm = (Rpwm < 0) ? 0 : Rpwm;
  delay(10);
  digitalWrite(driverIn1, in1);
  digitalWrite(driverIn2, in2);
  digitalWrite(driverIn3, in3);
  digitalWrite(driverIn4, in4);
  analogWrite(driverPwmL, Lpwm);
  analogWrite(driverPwmR, Rpwm);
}

void doEncoderA() {
  encoderPosL += (digitalRead(encoderPinA) == digitalRead(encoderPinB)) ? 1 : -1;
}
void doEncoderB() {
  encoderPosL += (digitalRead(encoderPinA) == digitalRead(encoderPinB)) ? -1 : 1;
}
void doEncoderC() {
  encoderPosR += (digitalRead(encoderPinC) == digitalRead(encoderPinD)) ? 1 : -1;
}
void doEncoderD() {
  encoderPosR += (digitalRead(encoderPinC) == digitalRead(encoderPinD)) ? -1 : 1;
}

void setup() {
  Serial.begin(9600);

  pinMode(encoderPinA, INPUT_PULLUP);
  attachInterrupt(0, doEncoderA, CHANGE);

  pinMode(encoderPinB, INPUT_PULLUP);
  attachInterrupt(1, doEncoderB, CHANGE);

  pinMode(encoderPinC, INPUT_PULLUP);
  attachInterrupt(4, doEncoderC, CHANGE);

  pinMode(encoderPinD, INPUT_PULLUP);
  attachInterrupt(5, doEncoderD, CHANGE);

}

long oldPositionL = -9999999999;
long oldPositionR = -9999999999;

void loop() {
  nowTime = millis();

  newposition1 = encoderPosL;
  newposition2 = encoderPosR;

  calculator(newposition1, newposition2);


  if (Serial.available()) {
    SerialData[0] = Serial.read();  // 시리얼 값 저장
    if (SerialData[0] == 's') {  // stop
      digitalWrite(led, LOW);
      driverSet(speedL, 0, 0, 0, 0, speedR);
      Serial.print("OK");
    }
    else if (SerialData[0] == 'f') { // front
      digitalWrite(led, HIGH);
      driverSet(speedL, 1, 0, 1, 0, speedR);
      Serial.print("OK");
    }
    else if (SerialData[0] == 'l') { // left
      driverSet(speedL / 2, 0, 1, 1, 0, speedR / 2);
      Serial.print("OK");
    }
    else if (SerialData[0] == 'r') { // right
      driverSet(speedL / 2, 1, 0, 0, 1, speedR / 2);
      Serial.print("OK");
    }
    else if (SerialData[0] == 'b') { // back
      driverSet(speedL, 0, 1, 0, 1, speedR);
      Serial.print("OK");
    }
    else if (SerialData[0] == 'R') { // reset
      driverSet(speedL, 0, 0, 0, 0, speedR);
      robot_R = 0;
      robot_X = 0;
      robot_Y = 0;
      Serial.print("OK");
    }
    else if (SerialData[0] == 'P') { // Pos
      Serial.print("Pos/");
      Serial.print(int(robot_X / unitScale));
      Serial.print("/");
      Serial.print(int(robot_Y / unitScale));
      Serial.print("/");
      Serial.print(float(robot_R));
    }
    else {
      if (testMode) {
        //Serial.println("OK");
      }
    }

    //for (int j = 0; j < 256; j++)
    //  SerialData[j] = '\0';
  }


}


float angleCalculator(float newpositionX, float newpositionY) {
  if (newpositionX >= 0 && newpositionY >= 0)
    return (-atan(newpositionX / newpositionY)) * 180 / PI;
  else if (newpositionX >= 0 && newpositionY < 0)
    return (-PI / 2 - atan(-newpositionY / newpositionX)) * 180 / PI;
  else if (newpositionX < 0 && newpositionY < 0)
    return (PI / 2 + atan(newpositionY / newpositionX)) * 180 / PI;
  else if (newpositionX < 0 && newpositionY >= 0)
    return (atan(-newpositionX / newpositionY)) * 180 / PI;
  else
    return 0;
}

float distanceCalculator(float newpositionX, float newpositionY) {
  return sqrt(pow(newpositionX, 2) + pow(newpositionY, 2));
}

float calculator(float newposition1, float newposition2) {
  double distanceL = diameter * M_PI / pulse * (newposition1 - newposition1_old);
  double distanceR = diameter * M_PI / pulse * (newposition2 - newposition2_old);

  newposition1_old = newposition1;
  newposition2_old = newposition2;
  //이동각도 계산
  double c = (distanceL - distanceR) / 2;
  //double angle = asin(2*sin(c/robot_wheel_pitch)*cos(c/robot_wheel_pitch))*(PI/180);
  double angle = 2 * asin(c / robot_wheel_pitch) * (180.0 / M_PI);
  Serial.print(distanceL);
  Serial.print(distanceR);
  //x, y 계산
  robot_X += sin(((angle / 2 + robot_R)) * (M_PI / 180.0)) * (distanceL + distanceR) / 2;
  robot_Y += cos(((angle / 2 + robot_R)) * (M_PI / 180.0)) * (distanceL + distanceR) / 2;
  robot_R += angle;
  if (robot_R > 180)
    robot_R = robot_R - 360;
  else if (robot_R < -180)
    robot_R = robot_R + 360;

  Serial.print("\t\tX: ");
  Serial.print(robot_X);
  Serial.print("\t\tY: ");
  Serial.print(robot_Y);
  Serial.print("\t\tR: ");
  Serial.print(robot_R);
  Serial.println();
  delay(100);
}
