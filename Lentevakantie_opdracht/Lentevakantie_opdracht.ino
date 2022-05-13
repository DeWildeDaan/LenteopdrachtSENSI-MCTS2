int D1 = 13;
int A = 11;
int F = 12;
int D2 = 10;
int D3 = 9;
int B = 8;
int D4 = 7;
int G = 6;
int C = 5;
int DP = 4;
int D = 3;
int E = 2;

int getal = 0;
String message = "10";

int i1;
String uur1;
int intuur1;
int i2;
String uur2;
int intuur2;
int i3;
String minuut1;
int intminuut1;
int i4;
String minuut2;
int intminuut2;


void setup() {
  Serial.begin(9600);
  pinMode(D1, OUTPUT);
  pinMode(A, OUTPUT);
  pinMode(F, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(D4, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(C, OUTPUT);
  pinMode(DP, OUTPUT);
  pinMode(D, OUTPUT);
  pinMode(E, OUTPUT);

  digitalWrite(D1, HIGH);
  digitalWrite(D2, HIGH);
  digitalWrite(D3, HIGH);
  digitalWrite(D4, HIGH);
}

void loop() {
  if (Serial.available()) {
    message = Serial.readString();
    Serial.println("OK");
  }
  send_message(message);
  
}

void send_message (String message) {
  i1 = message.indexOf(':');
  uur1 = message.substring(0, i1);
  intuur1 = uur1.toInt();
  
  i2 = message.indexOf(':', i1+1 );
  uur2 = message.substring(i1+1, i2);
  intuur2 = uur2.toInt();
  
  i3 = message.indexOf(':', i2+1 );
  minuut1 = message.substring(i2+1, i3);
  intminuut1 = minuut1.toInt();
  
  i4 = message.indexOf(':', i3+1 );
  minuut2 = message.substring(i3+1);
  intminuut2 = minuut2.toInt();
 
  display_getal(intuur1);
  digitalWrite(D1, LOW);
  digitalWrite(D1, HIGH);

  display_getal(intuur2);
  digitalWrite(D2, LOW);
  digitalWrite(D2, HIGH);

  display_getal(intminuut1);
  digitalWrite(D3, LOW);
  digitalWrite(D3, HIGH);
  
  display_getal(intminuut2);
  digitalWrite(D4, LOW);
  digitalWrite(D4, HIGH);
   
  }


void display_getal (int getal) {
  if (getal == 1) {
    digitalWrite(A, LOW);
    digitalWrite(B, HIGH);
    digitalWrite(C, HIGH);
    digitalWrite(D, LOW);
    digitalWrite(E, LOW);
    digitalWrite(F, LOW);
    digitalWrite(G, LOW);
  }
  if (getal == 2) {
    digitalWrite(A, HIGH);
    digitalWrite(B, HIGH);
    digitalWrite(C, LOW);
    digitalWrite(D, HIGH);
    digitalWrite(E, HIGH);
    digitalWrite(F, LOW);
    digitalWrite(G, HIGH);
  }
  if (getal == 3) {
    digitalWrite(A, HIGH);
    digitalWrite(B, HIGH);
    digitalWrite(C, HIGH);
    digitalWrite(D, HIGH);
    digitalWrite(E, LOW);
    digitalWrite(F, LOW);
    digitalWrite(G, HIGH);
  }
  if (getal == 4) {
    digitalWrite(A, LOW);
    digitalWrite(B, HIGH);
    digitalWrite(C, HIGH);
    digitalWrite(D, LOW);
    digitalWrite(E, LOW);
    digitalWrite(F, HIGH);
    digitalWrite(G, HIGH);
  }
  if (getal == 5) {
    digitalWrite(A, HIGH);
    digitalWrite(B, LOW);
    digitalWrite(C, HIGH);
    digitalWrite(D, HIGH);
    digitalWrite(E, LOW);
    digitalWrite(F, HIGH);
    digitalWrite(G, HIGH);
  }
  if (getal == 6) {
    digitalWrite(A, HIGH);
    digitalWrite(B, LOW);
    digitalWrite(C, HIGH);
    digitalWrite(D, HIGH);
    digitalWrite(E, HIGH);
    digitalWrite(F, HIGH);
    digitalWrite(G, HIGH);
  }
  if (getal == 7) {
    digitalWrite(A, HIGH);
    digitalWrite(B, HIGH);
    digitalWrite(C, HIGH);
    digitalWrite(D, LOW);
    digitalWrite(E, LOW);
    digitalWrite(F, LOW);
    digitalWrite(G, LOW);
  }
  if (getal == 8) {
    digitalWrite(A, HIGH);
    digitalWrite(B, HIGH);
    digitalWrite(C, HIGH);
    digitalWrite(D, HIGH);
    digitalWrite(E, HIGH);
    digitalWrite(F, HIGH);
    digitalWrite(G, HIGH);
  }
  if (getal == 9) {
    digitalWrite(A, HIGH);
    digitalWrite(B, HIGH);
    digitalWrite(C, HIGH);
    digitalWrite(D, LOW);
    digitalWrite(E, LOW);
    digitalWrite(F, HIGH);
    digitalWrite(G, HIGH);
  }
  if (getal == 0) {
    digitalWrite(A, HIGH);
    digitalWrite(B, HIGH);
    digitalWrite(C, HIGH);
    digitalWrite(D, HIGH);
    digitalWrite(E, HIGH);
    digitalWrite(F, HIGH);
    digitalWrite(G, LOW);
  }
  if (getal == 10) {
    digitalWrite(A, LOW);
    digitalWrite(B, LOW);
    digitalWrite(C, LOW);
    digitalWrite(D, LOW);
    digitalWrite(E, LOW);
    digitalWrite(F, LOW);
    digitalWrite(G, LOW);
  }
}
