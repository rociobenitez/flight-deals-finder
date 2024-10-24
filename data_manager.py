import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

SHEET_APP_KEY = os.getenv('SHEET_APP_KEY')
ENDPOINT_SHEET = f'https://api.sheety.co/{SHEET_APP_KEY}/ofertaDeVuelos/prices'

class DataManager:
   def __init__(self):
      self._user = os.getenv('SHEET_USERNAME')
      self._password = os.getenv('SHEET_PASSWORD')
      self._authorization = HTTPBasicAuth(self._user, self._password)
      self.destination_data = {}

   def get_destination_data(self):
      # Uso de la API de Sheety para OBTENER (GET) todos los datos de esa hoja e imprimirlos
      try:
         response = requests.get(ENDPOINT_SHEET, auth=self._authorization)
         response.raise_for_status()  # Levanta una excepción para códigos de estado 4xx/5xx
         data = response.json()

         if "prices" in data:
            self.destination_data = data["prices"]
            return self.destination_data
         else:
            print("Formato inesperado en la respuesta de Sheety.")
            return None
      except requests.exceptions.RequestException as e:
         print(f"Error al obtener los datos: {e}")
         return None

   # En la clase DataManager, hacer una solicitud PUT y utilizar el id de la fila de sheet_data
   # para actualizar la hoja de Google con los códigos IATA.
   def update_destination_codes(self):
      for city in self.destination_data:
         new_data = {
            "price": {
               "iataCode": city["iataCode"],
               "lowestPrice": float(city["lowestPrice"])
            }
         }
         try:
            response = requests.put(
               url=f"{ENDPOINT_SHEET}/{city['id']}",
               json=new_data
            )
            response.raise_for_status()  # Levanta una excepción si la respuesta no es 2xx
            print(f"Actualización exitosa para {city['city']} con ID {city['id']}.")
         except requests.exceptions.RequestException as e:
            print(f"Error al actualizar los datos de {city['city']} (ID: {city['id']}): {e}")
