/*
   See documentation at https://nRF24.github.io/RF24 & https://dstroy0.github.io/InputHandler/html/index.html
   See License information at root directory of this library, and RF24's license at https://github.com/nRF24/RF24/blob/master/LICENSE
   Authors: Brendan Doherty (2bndy5), Douglas Quigg (dstroy0)
*/

/**
   A simple example of sending data from 1 nRF24L01 transceiver to another, and
   using InputHandler's framework to construct a very basic remote cli
*/
#include <SPI.h>
#include "printf.h"
#include "RF24.h"
#include <InputHandler.h>

// instantiate an object for the nRF24L01 transceiver
RF24 radio(7, 8); // using pin 7 for the CE pin, and pin 8 for the CSN pin

// Let these addresses be used for the pair
uint8_t address[][6] = {"1Node", "2Node"};
// It is very helpful to think of an address as a path instead of as
// an identifying device destination

// to use different addresses on a pair of radios, we need a variable to
// uniquely identify which address this radio will use to transmit
bool radioNumber = 1; // 0 uses address[0] to transmit, 1 uses address[1] to transmit

// Used to control whether this node is sending or receiving
bool role = false;  // true = TX role, false = RX role

// For this example, we'll be using a payload that is
// a char buffer the maximum size of the radio's hardware buffer
char payload[32] {}; // zero-initialized buffer https://en.cppreference.com/w/cpp/language/zero_initialization
uint8_t payload_index = 0;

// UserInput default constructor with output
char output_buffer[64] {}; // zero-initialized class output buffer
UserInput inputHandler(output_buffer, buffsz(output_buffer));

// default function, called if nothing matches or if there is an error
void unrecognized(UserInput* inputProcess) {
  // error output
  inputProcess->outputToStream(Serial);
}

// function that will be called on the RX device
void remote_device(UserInput* inputProcess) {
  Serial.println(F("Reached 'remote_device' function"));
}

/**
   @brief CommandParameters struct for help_

*/
const PROGMEM CommandParameters receiver_param[1] = {
  remote_device,            // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
  no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "remote",                 // command string
  6,                        // command string characters
  root,                     // parent id
  root,                     // this command id
  root,                     // command depth
  0,                        // subcommands
  UI_ARG_HANDLING::no_args, // argument handling
  0,                        // minimum expected number of arguments
  0,                        // maximum expected number of arguments
  /* UITYPE arguments */
  {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
CommandConstructor remote_(receiver_param); // remote command

void setup() {

  Serial.begin(115200);
  while (!Serial) {
    // some boards need to wait to ensure access to serial over USB
  }

  // initialize the transceiver on the SPI bus
  if (!radio.begin()) {
    Serial.println(F("RF24 radio hardware is not responding!!"));
    while (1) {} // hold in infinite loop
  }

  // print example's introductory prompt
  Serial.println(F("RF24+InputHandler"));

  // To set the radioNumber via the Serial monitor on startup
  Serial.println(F("Which radio is this? Enter '0' or '1'. Defaults to '0'"));
  while (!Serial.available()) {
    // wait for user input
  }
  char input = Serial.parseInt();
  radioNumber = input == 1;
  Serial.print(F("radioNumber = "));
  Serial.println((int)radioNumber);

  // role variable is hardcoded to RX behavior, inform the user of this
  Serial.println(F("If the TX node, limit input to 32 char or less!"));

  // Set the PA Level low to try preventing power supply related problems
  // because these examples are likely run with nodes in close proximity to
  // each other.
  radio.setPALevel(RF24_PA_LOW);  // RF24_PA_MAX is default.

  // save on transmission time by setting the radio to only transmit the
  // number of bytes we need to transmit a float
  radio.setPayloadSize(sizeof(payload)); // float datatype occupies 4 bytes

  // set the TX address of the RX node into the TX pipe
  radio.openWritingPipe(address[radioNumber]);     // always uses pipe 0

  // set the RX address of the TX node into a RX pipe
  radio.openReadingPipe(1, address[!radioNumber]); // using pipe 1

  // additional setup specific to the node's role
  if (role) {
    radio.stopListening();  // put radio in TX mode
  } else {
    radio.startListening(); // put radio in RX mode
    inputHandler.defaultFunction(unrecognized); // default callback function
    inputHandler.addCommand(remote_); // remote device, perform runtime calcs
    inputHandler.begin(); // allocate memory for inputHandler
  }

  // For debugging info
  // printf_begin();             // needed only once for printing details
  // radio.printDetails();       // (smaller) function that prints raw register values
  // radio.printPrettyDetails(); // (larger) function that prints human readable data

} // setup

void loop() {

  if (role) {
    // This device is a TX node

    while (Serial.available() && payload_index < 32) // get user input, and place it in the payload buffer
    {
      char rc = Serial.read(); // Serial (Stream) read() can only read one byte (char) at a time
      payload[payload_index] = rc; // put the received char into the payload buffer
      payload_index++; // increment payload_index, this means the same as payload_index = payload_index + 1;
    }
    if (payload_index > 0) {
      unsigned long start_timer = micros();                    // start the timer
      bool report = radio.write(&payload, payload_index);      // transmit & save the report
      unsigned long end_timer = micros();                      // end the timer
      payload_index = 0;
      if (report) {
        Serial.print(F("Transmission successful! "));          // payload was delivered
        Serial.print(F("Time to transmit = "));
        Serial.print(end_timer - start_timer);                 // print the timer result
        Serial.print(F(" us. Sent: "));
        Serial.println(payload);                               // print payload sent
      } else {
        Serial.println(F("Transmission failed or timed out")); // payload was not delivered
      }
    }
  } else {
    // This device is a RX node

    uint8_t pipe;
    if (radio.available(&pipe)) {             // is there a payload? get the pipe number that recieved it
      uint8_t bytes = radio.getPayloadSize(); // get the size of the payload
      radio.read(&payload, bytes);            // fetch payload from FIFO
      Serial.print(F("Received "));
      Serial.print(bytes);                    // print the size of the payload
      Serial.print(F(" bytes on pipe "));
      Serial.print(pipe);                     // print the pipe number
      Serial.print(F(": "));
      Serial.println(payload);                // print the payload's value
      inputHandler.readCommandFromBuffer((uint8_t*)payload, bytes);
      inputHandler.outputToStream(Serial); // print inputHandler's output buffer
    }
  } // role
} // loop

// end of file
