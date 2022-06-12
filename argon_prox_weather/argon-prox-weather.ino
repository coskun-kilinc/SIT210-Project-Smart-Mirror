// This #include statement was automatically added by the Particle IDE.
#include <ThingSpeak.h>

// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_DHT.h>

#define DHTPIN D2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)


SYSTEM_THREAD(ENABLED);

TCPClient client;

// starting values
unsigned long startTime = 60000; // set to 1 minute to give an extra minute to get a starting value
float maxTemp = 0.0;
float maxHum = 0.0;

unsigned long myChannelNumber = 1765217;    // change this to your channel number
const char * myWriteAPIKey = "BT01Z7HKQ47RFYKB"; // change this to your channels write API key

// create DHT object
DHT dht(DHTPIN, DHTTYPE);

// setup() runs once, when the device is first turned on.
void setup() {
  ThingSpeak.begin(client);
  Serial.begin(9600);
  dht.begin();

}

// loop() runs over and over again, as quickly as it can execute.
void loop() {
    // read every 15 seconds, but report the max every minute.
    delay(15000);
    // DHT sometimes returns a NaN result. If we're only updating the mirror every minute, this could lead to
    // an minute of no information. If we take the maximum reading over a minute, we reduce the chance of this happening
    // and smooth out noice from the sensor.

    unsigned long elapsedTime = millis() - startTime;
    
    // read temp and humidity
    float temperature = dht.getTempCelcius();
    float humidity = dht.getHumidity();
    // print to serial monitor, just for debugging 
    Serial.println(String::format("Temperature: %f°c", temperature)); 
    Serial.println(String::format("Humidity: %f%%", humidity)); 
    
    if ( temperature > maxTemp) { maxTemp = temperature; }
    if ( humidity > maxHum) { maxHum = humidity; }
    // Write maximum value over previous minute to ThingSpeak
    
    // after 1 minute has elapsed
    if ( elapsedTime >= 60000 ){
        // assign readings to thingspeak fields
        ThingSpeak.setField(1, maxTemp);
        ThingSpeak.setField(2, maxHum);
        // reset maximums
        maxTemp = 0;
        maxHum = 0;
        // write data to thingspeak channel
        ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
        startTime = millis();
    }
}