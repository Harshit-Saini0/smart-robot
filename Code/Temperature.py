import board
import adafruit_dht
import time

class TemperatureSensor:
    def __init__(self):
        self.sensor = adafruit_dht.DHT22(board.D7)

    def fetch(self):
        try:
            temperature = self.sensor.temperature * 9/5 + 32
            humidity = self.sensor.humidity
            return temperature, humidity
        except Exception as e:
            print("Read error:", e)
            return None, None

    def cleanup(self):
        self.sensor.exit()
        
if __name__ == "__main__":
    temp_sensor = TemperatureSensor()
    try:
        while True:
            temp, hum = temp_sensor.fetch()
            if temp is not None and hum is not None:
                print(f"Temp: {temp:.1f}°F, Humidity: {hum:.1f}%")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        temp_sensor.cleanup()
