
from abc import ABC, abstractmethod
import math
import random
from widgets import thingspeak


DEBUG = False

'''
Abstract class for fetching temperature and humidity.
'''
class AbstractWeatherInterface(ABC):
    
    @abstractmethod
    def get_temperature(self) -> float:
        ''' Fetch the temperature '''
        raise NotImplementedError
        
    @abstractmethod
    def get_humidity(self) -> float:
        ''' Fetch the humidity '''
        raise NotImplementedError

    def convert_to_f(self, temp_c: float) -> float:
        temp_as_f = temp_c * 1.8 + 32
        return temp_as_f

    def calculate_heat_index(self, temperature: float, humidity: float, is_farenheit: bool) -> float:
        ''' Calculate the heat index based on temperature and humidity '''
        heat_index = 0
        if (not is_farenheit):
                temperature = self.convert_to_f(temperature)

                heat_index = 0.5 * (temperature + 61.0 + ((temperature - 68.0) * 1.2) +
                            (humidity * 0.094))

                if (heat_index > 79):
                    heat_index = (-42.379 + 2.04901523 * temperature + 10.14333127 * humidity
                    + -0.22475541 * temperature * humidity + -0.00683783 * pow(temperature, 2)
                    + -0.05481717 * pow(humidity, 2) + 0.00122874 * pow(temperature, 2)
                    * humidity + 0.00085282 * temperature * pow(humidity, 2) + -0.00000199
                    * pow(temperature, 2) * pow(humidity, 2))

                    if ((humidity < 13) and (temperature >= 80.0) and (temperature <= 112.0)):
                        heat_index -= ((13.0 - humidity) * 0.25) * math.sqrt((17.0 - abs(temperature - 95.0)) * 0.05882)

                    elif ((humidity > 85.0) and (temperature >= 80.0) and (temperature <= 87.0)):
                        heat_index += ((humidity - 85.0) * 0.1) * ((87.0 - temperature) * 0.2)
        return heat_index


'''
Dummy interface for testing module without connecting hardware, generates random temperature and humidity. Super class convert to Farenheit and calculates heat index
'''
class DummyWeather(AbstractWeatherInterface):

        def get_temperature(self) -> float:
            ''' Fetch the temperature, overrides interface method '''
            temperature = random.random() * random.randint(1, 40)
            return temperature
            
        def get_humidity(self) -> float:
            ''' Fetch the humidity, overrides interface method '''
            humidity = random.random()*100
            return humidity

        def convert_to_f(self, temp_c) -> float:
             return super().convert_to_f(temp_c)

        def calculate_heat_index(self, temperature: float, humidity: float, is_farenheit: bool) -> float:
             return super().calculate_heat_index(temperature, humidity, is_farenheit)


'''
Reads data from ThingSpeak channel, which is published by the Particle Argon reading 
'''
class ThingSpeakWeather(AbstractWeatherInterface):

        def get_temperature(self) -> float:
            ''' Fetch the temperature, overrides interface method '''
            temperature = float(thingspeak.read_feeds(1)[0]['field1'])  
            if DEBUG: print(temperature)      
            return temperature
            
        def get_humidity(self) -> float:
            ''' Fetch the humidity, overrides interface method '''
            humidity = float(thingspeak.read_feeds(1)[0]['field2'])
            ## believe it or not, humidity can go above 100%. It really shouldn't in this example though, other than due to sensor error
            # if humidity > 100: humidity = 100
            if DEBUG: print(humidity)    
            return humidity

        def convert_to_f(self, temp_c) -> float:
             return super().convert_to_f(temp_c)

        def calculate_heat_index(self, temperature: float, humidity: float, is_farenheit: bool) -> float:
             return super().calculate_heat_index(temperature, humidity, is_farenheit)
