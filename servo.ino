#include <Servo.h>
 
#define X_SERVO_PIN 9
#define Y_SERVO_PIN 10


Servo xservo;
Servo yservo;
int incomingByte = 0;
int state = 0;
 
void setup() {
	Serial.begin(9600); // устанавливаем последовательное соединение
	xservo.attach(X_SERVO_PIN);
	xservo.write(90);  // Поворачивает сервопривод на среднее положение
	yservo.attach(Y_SERVO_PIN);
	yservo.write(90);  // Поворачивает сервопривод на среднее положение
}
 
void loop() {
	if (Serial.available() > 0) {  //если есть доступные данные
		// считываем байт
		incomingByte = Serial.read();
		switch(state){
			case 0: //preamble input
				if( incomingByte == 0x55 )
					state=1;
			break;
			case 1: //xservo go
				xservo.write(incomingByte);
				state=2;
			break;
			case 2: //yservo go
				yservo.write(incomingByte);
				state=0;
			break;
		}
	}
}
