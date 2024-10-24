import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

URL = 'https://test.api.amadeus.com'
ENDPOINT_TOKEN = f'{URL}/v1/security/oauth2/token'
ENDPOINT_FLIGHT = f'{URL}/v2/shopping/flight-offers'
ENDPOINT_CITIES = f'{URL}/v1/reference-data/locations/cities'

class FlightSearch:

   def __init__(self):
      """
      Inicializar una instancia de la clase FlightSearch.

      Este constructor realiza las siguientes tareas:
      1. Recupera API key y API secret de las variables de entorno 'API_KEY_AMADEUS' y 'API_SECRET_AMADEUS', respectivamente.

      Variables de instancia:
         _api_key (str): La clave de la API para autenticarse con Amadeus, obtenida del archivo .env.
         _api_secret (str): El secreto de la API para autenticarse con Amadeus, obtenido del archivo .env.
         _token (str): El token de autenticación obtenido al llamar al método _get_new_token().
      """
      self._api_key = os.environ["API_KEY_AMADEUS"]
      self._api_secret = os.environ["API_SECRET_AMADEUS"]
      self._token = self._get_new_token()

   def _get_new_token(self):
      """
      Genera el token de autenticación que se utiliza para acceder a la API de Amadeus y lo devuelve.

      Esta función realiza una solicitud POST a la endpoint de tokens de Amadeus con las credenciales necesarias
      (clave de API y secreto de API) para obtener un nuevo token de credenciales del cliente.
      Al recibir una respuesta, la función actualiza el token de la instancia de FlightSearch.

      Returns:
         str: El nuevo token de acceso obtenido de la respuesta de la API.
      """
      try:
         header = {
            'Content-Type': 'application/x-www-form-urlencoded'
         }
         body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
         }
         response = requests.post(url=ENDPOINT_TOKEN, headers=header, data=body)
         response.raise_for_status()  # Verifica si hay algún error en la respuesta
         # Nuevo token de acceso. Normalmente expira en 1799 segundos (30 min)
         token_data = response.json()
         print(f"Tu token es {token_data['access_token']}")
         print(f"Tu token expira en {token_data['expires_in']} segundos")
         return token_data['access_token']
      except requests.exceptions.RequestException as e:
         print(f"Error obteniendo el token: {e}")
         return None

   def get_destination_code(self, city_name):
      """
      Recupera el código IATA para una ciudad especificada usando el API de Ubicación de Amadeus.

      Parámetros:
         city_name (str): El nombre de la ciudad para la cual encontrar el código IATA.
      Return:
         str: El código IATA de la primera ciudad coincidente si se encuentra; "N/A"
          si no se encuentra ninguna coincidencia debido a un IndexError,
          o "No encontrado" si no se encuentra ninguna coincidencia debido a un KeyError.

      La función envía una solicitud GET al IATA_ENDPOINT con una consulta que
      especifica el nombre de la ciudad y otros parámetros para afinar la búsqueda.
      Luego intenta extraer el código IATA de la respuesta JSON.

      - Si la ciudad no se encuentra en los datos de la respuesta (es decir, si el array de datos
      está vacío, lo que lleva a un IndexError), registra un mensaje indicando que no se encontró
      ningún código de aeropuerto para la ciudad y devuelve "N/A".

      - Si la clave esperada no se encuentra en la respuesta (es decir, si falta la clave 'iataCode',
      lo que lleva a un KeyError), registra un mensaje indicando que no se encontró ningún código
      de aeropuerto para la ciudad y devuelve "No encontrado".
      """
      header = {"Authorization": f"Bearer {self._token}"}
      query = {
         'keyword': city_name,
         'max': 2,
         'include': 'AIRPORTS',
      }
      response = requests.get(url=ENDPOINT_CITIES, headers=header, params=query)
      print(f"Status code {response.status_code}. Airport IATA: {response.text}")
      try:
         code = response.json()["data"][0]['iataCode']
      except IndexError:
         print(f"IndexError: No se ha encontrado el código del aeropuerto de {city_name}.")
         return "N/A"
      except KeyError:
         print(f"KeyError: No se ha encontrado el código del aeropuerto de {city_name}.")
         return "Not Found"

      return code

   def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
      """
      Searches for flight options between two cities on specified departure and return dates
      using the Amadeus API.
      Parameters:
          origin_city_code (str): The IATA code of the departure city.
          destination_city_code (str): The IATA code of the destination city.
          from_time (datetime): The departure date.
          to_time (datetime): The return date.
      Returns:
          dict or None: A dictionary containing flight offer data if the query is successful; None
          if there is an error.
      The function constructs a query with the flight search parameters and sends a GET request to
      the API. It handles the response, checking the status code and parsing the JSON data if the
      request is successful. If the response status code is not 200, it logs an error message and
      provides a link to the API documentation for status code details.
      """

      headers = {"Authorization": f"Bearer {self._token}"}
      query = {
         "originLocationCode": origin_city_code,
         "destinationLocationCode": destination_city_code,
         "departureDate": from_time.strftime("%Y-%m-%d"),
         "returnDate": to_time.strftime("%Y-%m-%d"),
         "adults": 1,
         "nonStop": "true",
         "currencyCode": "EUR",
         "max": "10",
      }

      response = requests.get(url=ENDPOINT_FLIGHT, headers=headers, params=query)

      if response.status_code != 200:
         print(f"check_flights() response code: {response.status_code}")
         print("Hubo un problema con la búsqueda de vuelos.\n"
               "Para detalles sobre status codes, revisa la documentación de la API:\n"
               "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
               "-reference")
         print("Response body:", response.text)
         return None

      return response.json()