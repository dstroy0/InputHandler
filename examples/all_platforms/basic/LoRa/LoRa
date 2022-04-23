/*
    https://github.com/sandeepmistry/arduino-LoRa/blob/master/examples/LoRaSenderNonBlockingCallback/LoRaSenderNonBlockingCallback.ino

    sender sketch
*/

#include <SPI.h>
#include <LoRa.h>

char payload[32]{};
char payload_index = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Sender, non blocking");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  LoRa.onTxDone(onTxDone);
}

void loop() {
    while (Serial.available() && payload_index < 32) // get user input, and place it in the payload buffer
    {
      char rc = Serial.read(); // Serial (Stream) read() can only read one byte (char) at a time
      payload[payload_index] = rc; // put the received char into the payload buffer
      payload_index++; // increment payload_index, this means the same as payload_index = payload_index + 1;
    }
    if (payload_index > 0)
    {
        // send in async / non-blocking mode
        LoRa.beginPacket();
        LoRa.print(payload);
        LoRa.endPacket(true); // true = async / non-blocking mode
        payload_index = 0;
    }
}

void onTxDone() {
  Serial.println("TxDone");
}