/*
    https://github.com/sandeepmistry/arduino-LoRa/blob/master/examples/LoRaReceiverCallback/LoRaReceiverCallback.ino
*/

#include <InputHandler.h>
#include <LoRa.h>
#include <SPI.h>
using namespace ih;
#ifdef ARDUINO_SAMD_MKRWAN1300
    #error "This example is not compatible with the Arduino MKR WAN 1300 board!"
#endif

char payload[32] {}; // zero-initialized buffer
                     // https://en.cppreference.com/w/cpp/language/zero_initialization
uint8_t payload_index = 0;

// Input default constructor with output
char output_buffer[64] {}; // zero-initialized class output buffer
const InputParameters* defaultConstructor = NULL;
Input inputHandler(defaultConstructor, output_buffer, buffsz(output_buffer));

// default function, called if nothing matches or if there is an error
void unrecognized(Input* inputProcess)
{
    // error output
    inputProcess->outputToStream(Serial);
}

// function that will be called on the RX device
void remote_device(Input* inputProcess) { Serial.println(F("Reached 'remote_device' function")); }

/**
   @brief Parameters struct for help_

*/
const PROGMEM Parameters receiver_param[1] = {
    remote_device, // this is allowed to be NULL, if this is NULL and the terminating subcommand
                   // function ptr is also NULL nothing will launch (error)
    no_wildcards,  // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "remote",      // command string
    6,             // command string characters
    root,          // parent id
    root,          // this command id
    root,          // command depth
    0,             // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
Command remote_(receiver_param); // remote command

void setup()
{
    Serial.begin(115200);
    while (!Serial)
        ;

    Serial.println("LoRa Receiver Callback");

    if (!LoRa.begin(915E6))
    {
        Serial.println("Starting LoRa failed!");
        while (1)
            ;
    }

    // Uncomment the next line to disable the default AGC and set LNA gain, values between 1 - 6 are
    // supported LoRa.setGain(6);

    // register the receive callback
    LoRa.onReceive(onReceive);

    // put the radio into receive mode
    LoRa.receive();

    inputHandler.defaultFunction(unrecognized); // default callback function
    inputHandler.addCommand(remote_);           // remote device, perform runtime calcs
    inputHandler.begin();                       // allocate memory for inputHandler
}

void loop()
{
    // do nothing
}

void onReceive(int packetSize)
{
    // received a packet

    // read packet
    for (int i = 0; i < packetSize; i++)
    {
        payload[i] = LoRa.read();
    }

    // print RSSI of packet
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());

    inputHandler.readCommandFromBuffer((uint8_t*)payload, packetSize);
}