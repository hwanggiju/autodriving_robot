// 모터 사이즈/엔코더/감속비
// 28파이/2채널 6펄스/ 1/139
// 모터는 한바퀴당 44펄스인데, 감속기를 통하면 모터가 139바퀴를 더 돌아야 1바퀴이므로 감속기를 통한 최종 출력은 1바퀴에 6116펄스이며,
// 각도로 치면 1펄스에 0.059도까지 감지 가능

#define encoderPinA         2
#define encoderPinB         3
#define encoderPinC         18
#define encoderPinD         19

#define led                 13

#define Gear_ratio          139   // 감속비
#define encoderPPR          6     // 2채널 6펄스
#define MotorRPM            44    // 모터 한바퀴 펄스

const float ratio = 360. / 139. / 6.;    // 1펄스 각도

char SerialData[256] = "";        // 시리얼 입력값

// P control
float Kp = 30;
float targetDeg = 360;  // 목표값

int driverPwmL  = 6;    // 왼쪽 enable PWM
int driverIn1   = 7;
int driverIn2   = 8;
int driverIn3   = 9;
int driverIn4   = 10;
int driverPwmR  = 11;   // 오른쪽 enable PWM


float speedL = 100, speedR = 100; // 바퀴 속도

long encoderPosL = 0;   // 왼쪽 엔코더 시작위치
long encoderPosR = 0;   // 오른쪽 엔코더 시작위치

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
  Serial.begin(115200);

  pinMode(encoderPinA, INPUT_PULLUP);
  attachInterrupt(0, doEncoderA, CHANGE);

  pinMode(encoderPinB, INPUT_PULLUP);
  attachInterrupt(1, doEncoderB, CHANGE);

  pinMode(encoderPinC, INPUT_PULLUP);
  attachInterrupt(4, doEncoderC, CHANGE);

  pinMode(encoderPinD, INPUT_PULLUP);
  attachInterrupt(5, doEncoderD, CHANGE);
}

void loop() {
  float motorDegL = float(encoderPosL) * ratio;   // 현재 왼쪽 모터 각도
  float motorDegR = float(encoderPosR) * ratio;   // 현재 오른쪽 모터 각도
  float errorL = targetDeg - motorDegL;           // 목표각도와 현재 각도의 오차
  float errorR = targetDeg - motorDegR;
  float controlL = Kp * errorL;
  float controlR = Kp * errorR;

  if (Serial.available()) {
    int i = 0;
    while (Serial.available()) {
      SerialData[i] = Serial.read();
      delay(1);
      i++;
    }
    if (strcmp(SerialData, "stop") == 0) {
      digitalWrite(led, LOW);
      driverSet(speedL, 0, 0, 0, 0, speedR);
    }
    else if (strcmp(SerialData, "front") == 0) {
      digitalWrite(led, HIGH);
      driverSet(speedL, 1, 0, 1, 0, speedR);
    }
    else if (strcmp(SerialData, "left") == 0) {
      driverSet(speedL / 2, 0, 1, 1, 0, speedR / 2);
    }
    else if (strcmp(SerialData, "right") == 0) {
      driverSet(speedL / 2, 1, 0, 0, 1, speedR / 2);
    }
    else if (strcmp(SerialData, "back") == 0) {
      driverSet(speedL, 0, 1, 0, 1, speedR);
    }
    /*
      else if (strcmp(SerialData, "reset") == 0) {
      driverSet(speedL, 0, 0, 0, 0, speedR);
      robot_R = 0;
      robot_X = 0;
      robot_Y = 0;
      Serial.print("OK");
      }

      else if (strcmp(SerialData, "Pos") == 0) {
      Serial.print("Pos/");
      Serial.print(int(robot_X / unitScale));
      Serial.print("/");
      Serial.print(int(robot_Y / unitScale));
      Serial.print("/");
      Serial.print(float(robot_R));
      }
    */
    Serial.print("encoderPosL : ");
    Serial.print(encoderPosL);
    Serial.print("  encoderPosR : ");
    Serial.println(encoderPosR);
    Serial.print("motorDegL : ");
    Serial.print(float(encoderPosL)*ratio);
    Serial.print("  motorDegR : ");
    Serial.println(float(encoderPosR)*ratio);
    Serial.print("errorL : ");
    Serial.print(errorL);
    Serial.print("  errorR : ");
    Serial.println(errorR);
    Serial.print("controlL : ");
    Serial.print(controlL);
    Serial.print("  controlR : ");
    Serial.println(controlR);
    Serial.print("motorVelL : ");
    Serial.print(min(abs(controlL), 255));
    Serial.print("    motorVelR : ");
    Serial.println(min(abs(controlR), 255));
    Serial.println();
    for (int j = 0; j < 256; j++)
      SerialData[j] = '\0';
  }
}
