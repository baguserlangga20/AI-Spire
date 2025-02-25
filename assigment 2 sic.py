import machine
from machine import Pin, ADC
import ujson
import network
import utime as time
import dht
import urequests as requests


DEVICE_ID = "esp-32"
WIFI_SSID = "" #nama wifi sendiri
WIFI_PASSWORD = "" #password juga
TOKEN = "BBUS-GkUQCVA0n5dqBSfeLaukJ5maWH1yLM"
DHT_PIN = Pin(15)

# Constants for ADC setup
ADC_PIN = 32  # Use GPIO34 or another ADC pin on ESP32
NO_OF_SAMPLES = 100  # Number of samples for averaging (similar to C code)
VALUE_MAX = 4095  # Maximum ADC value for 12-bit resolution (ESP32)

# Set up the ADC pin
adc = machine.ADC(ADC_PIN)
adc.atten(machine.ADC.ATTN_11DB)  # Set input attenuation to 11dB for 0-3.6V range
adc.width(machine.ADC.WIDTH_12BIT)  # Set ADC resolution to 12-bit


def create_json_data(temperature, humidity, light):
    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "temp": temperature,
        "humidity": humidity,
        "type": "sensor"
    })
    return data

def create_json_data(kelembapan):
    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "mosit": kelembapan,
        "type": "sensor"
    })
    return data

def send_data_to_ubidots(temperature, humidity, moist):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "moist" : moist
    }
    response = requests.post(url, json=data, headers=headers)
    print("Response:", response.text)
    print("Done Sending Data to ubidots!")

def send_data_to_server(temperature, humidity, moist):
    url = "https://postman-echo.com/post"  # Ganti dengan URL yang benar untuk menerima POST
    headers = {"Content-Type": "application/json"}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "moist" : moist,
        "timestamp": "24-02-2025 16:09:30"
    }
    response = requests.post(url, json=data, headers=headers)
    

wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting device to WiFi")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi_client.isconnected():
    print("Sabar lekkk")
    time.sleep(0.1)
print("MANTAAPP!")
print(wifi_client.ifconfig())

dht_sensor = dht.DHT11(DHT_PIN)

# Function to read the ADC and average multiple samples
def yl69_read():
    adc_reading = 0
    # Multisampling
    for i in range(NO_OF_SAMPLES):
        adc_reading += adc.read()
    adc_reading //= NO_OF_SAMPLES  # Average the readings
    return adc_reading

# Function to normalize the ADC reading to a percentage (inverted)
def yl69_normalization(adc_value):
    return (VALUE_MAX - adc_value) * 100 // VALUE_MAX


while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        mentahanmoist = yl69_read()
        moisture = yl69_normalization(mentahanmoist)
        
        
        if temperature is not None and humidity is not None:
            print("Temperature:", temperature, "°C")
            print("Humidity:", humidity, "%")
            print("Moisture:", moisture, '%')
            
            send_data_to_ubidots(temperature, humidity, moisture)
            send_data_to_server(temperature, humidity, moisture)
        else:
            print("Failed to read from DHT sensor.")
        
    except Exception as e:
        print("Error:", e)

    time.sleep(2)
