#include <Servo.h>
#include <ArduinoJson.h>

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

Servo cupholder, pillcollector; //servo that holds the cuups
//Servo pillcollector //servo that collects the pills

#define USE_SERIAL Serial

ESP8266WiFiMulti WiFiMulti;

void setup() {

  USE_SERIAL.begin(115200);
  // USE_SERIAL.setDebugOutput(true);

  USE_SERIAL.println();
  USE_SERIAL.println();
  USE_SERIAL.println();

  for (uint8_t t = 4; t > 0; t--) {
    USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
    USE_SERIAL.flush();
    delay(1000);
  }

  WiFiMulti.addAP("Chinomnso's iPhone", "nubbin419");
  cupholder.attach(2);          //give pins to the servos
  pillcollector.attach(5);

  //initialise the positions
  cupholder.write(90);
  delay(1000);
  pillcollector.write(180);
  delay(1000);

}

//void getprescription(int paracetamol, int panadol) {
//  String person;
//
//    HTTPClient http;
//
//    http.begin("https://58y5ck6e:v7ocw75f729qazw5@box-6748659.us-east-1.bonsaisearch.net/try/try/dispensename", "82 FA D3 A3 14 24 24 F8 9E E9 DF 0E 8E 38 EC E9 E8 11 A7 BA"); //HTTPS
//
//    int httpCode = http.GET();
//
//    // httpCode will be negative on error
//    if (httpCode > 0) {
//      // HTTP header has been send and Server response header has been handled
//      USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);
//
//      // file found at server
//      if (httpCode == HTTP_CODE_OK) {
//        String payload = http.getString();
//        JsonObject& root = jsonBuffer2.parseObject(payload);
//        String personn = root["_source"]["dispensename"];
//        person = personn;
//      }
//    } else {
//      USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
//    }
//
//    http.end();
//
//    USE_SERIAL.print("[HTTP] begin...\n");
//    // configure traged server and url
//    http.begin("https://58y5ck6e:v7ocw75f729qazw5@box-6748659.us-east-1.bonsaisearch.net/try/try/" + person, "82 FA D3 A3 14 24 24 F8 9E E9 DF 0E 8E 38 EC E9 E8 11 A7 BA"); //HTTPS
//    //http.begin("http://192.168.1.12/test.html"); //HTTP
//
//    USE_SERIAL.print("[HTTP] GET...\n");
//    // start connection and send HTTP header
//    httpCode = http.GET();
//
//    // httpCode will be negative on error
//    if (httpCode > 0) {
//      // HTTP header has been send and Server response header has been handled
//      USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);
//
//      // file found at server
//      if (httpCode == HTTP_CODE_OK) {
//        String payload = http.getString();
//        JsonObject& root = jsonBuffer2.parseObject(payload);
//
//        const char* source = root["_source"];
//
//        paracetamol = root["_source"]["paracetamol"];
//        panadol = root["_source"]["panadol"];
//        USE_SERIAL.println(paracetamol);
//        USE_SERIAL.println(panadol);
//
//        USE_SERIAL.println(payload);
//
//      }
//      http.end();
//
//    } else {
//      USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
//      http.end();
//
//    }
//
//  delay(5000);
//}

void dispenseone (int n, String whatpill) {
  int ends = 0;
  if (whatpill == "green") {
    cupholder.write(0);
    delay(1000);
  }
  else {
    cupholder.write(165);
    delay(1000);
    ends = 30;
  }

  int pos;
  for (int i = 0; i < n; i++ ) {
    for (pos = 180; pos >= 0; pos -= 1) // goes from 180 degrees to 0 degrees
    {
      pillcollector.write(pos);              // tell servo to go to position in variable 'pos'
      delay(30);                       // waits 30ms for the servo to reach the position
    }
  }
  pillcollector.write(180);
  delay(100);
}

void dispenseall (int green, int orange) {
  //green on init is at opening
  //dispense green
  if (green > 0){
  dispenseone(green, "green");
  delay(500);
  }
  //dispense orange
  if (orange > 0){
  dispenseone(orange, "orange");
  delay(500);
  }
}

void loop() {
StaticJsonBuffer<400> jsonBuffer;
StaticJsonBuffer<400> jsonBuffer1;
StaticJsonBuffer<400> jsonBuffer2;

  int paracetamol = 0;
  int panadol = 0;

  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    HTTPClient http;

    USE_SERIAL.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin("https://58y5ck6e:v7ocw75f729qazw5@box-6748659.us-east-1.bonsaisearch.net/try/try/dispense", "82 FA D3 A3 14 24 24 F8 9E E9 DF 0E 8E 38 EC E9 E8 11 A7 BA"); //HTTPS

    int httpCode = http.GET();

    // httpCode will be negative on error


    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        String payload = http.getString();
        JsonObject& root = jsonBuffer.parseObject(payload);

        const char* source = root["_source"];

        int dispense = root["_source"]["dispense"];
        USE_SERIAL.println(payload);
        //http.end();

        if (dispense == 1) {
                  //reset dispense to 0
    http.begin("https://58y5ck6e:v7ocw75f729qazw5@box-6748659.us-east-1.bonsaisearch.net/try/try/dispense", "82 FA D3 A3 14 24 24 F8 9E E9 DF 0E 8E 38 EC E9 E8 11 A7 BA"); //HTTPS
http.addHeader("Content-Type", "application/x-www-form-urlencoded");
http.POST("{\"dispense\" : 0}");
http.writeToStream(&Serial);

          //           getprescription(paracetamol, panadol);
          USE_SERIAL.print("Im here now");

          ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

          String person;

          http.begin("https://58y5ck6e:v7ocw75f729qazw5@box-6748659.us-east-1.bonsaisearch.net/try/try/dispensename", "82 FA D3 A3 14 24 24 F8 9E E9 DF 0E 8E 38 EC E9 E8 11 A7 BA"); //HTTPS

          int httpCode1 = http.GET();
          USE_SERIAL.print("Im here now 2");

          // httpCode will be negative on error
          if (httpCode1 > 0) {
            // HTTP header has been send and Server response header has been handled
            USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode1);

            // file found at server
            if (httpCode1 == HTTP_CODE_OK) {
              String payload1 = http.getString();
              JsonObject& root1 = jsonBuffer1.parseObject(payload1);
              String personn = root1["_source"]["dispensename"];
              USE_SERIAL.print(personn);

              person = personn;
            }
          } else {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
          }

          //http.end();

          USE_SERIAL.print("[HTTP] begin...\n");
          // configure traged server and url
          http.begin("https://58y5ck6e:v7ocw75f729qazw5@box-6748659.us-east-1.bonsaisearch.net/try/try/" + person, "82 FA D3 A3 14 24 24 F8 9E E9 DF 0E 8E 38 EC E9 E8 11 A7 BA"); //HTTPS
          //http.begin("http://192.168.1.12/test.html"); //HTTP

          USE_SERIAL.print("[HTTP] GET...\n");
          // start connection and send HTTP header
          int httpCode2 = http.GET();

          // httpCode will be negative on error
          if (httpCode2 > 0) {
            // HTTP header has been send and Server response header has been handled
            USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode2);

            // file found at server
            if (httpCode2 == HTTP_CODE_OK) {
              String payload2 = http.getString();
              JsonObject& root2 = jsonBuffer2.parseObject(payload2);

              const char* source2 = root2["_source"];

              paracetamol = root2["_source"]["paracetamol"];
              panadol = root2["_source"]["panadol"];
              USE_SERIAL.println(paracetamol);
              USE_SERIAL.println(panadol);

              USE_SERIAL.println(payload2);

            }
            //http.end();

          } else {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode2).c_str());
            //http.end();

          }

        }

        delay(1000);
        /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


        dispenseall(paracetamol, panadol);


      }

    } else {
      USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  } else{
    USE_SERIAL.printf("no wifi");
  }
  USE_SERIAL.printf("done \n");
  
  delay(2000);
}
