import unittest
from unittest.mock import patch
from flight_search import FlightSearch

class TestFlightSearch(unittest.TestCase):
   """
   Esta prueba simula las respuestas de la API de Amadeus para
   verificar si el método get_destination_code funciona
   correctamente sin tener que hacer llamadas reales a la API.
   """
   @patch('flight_search.requests.get')
   def test_get_destination_code(self, mock_get):
      # Simula una respuesta exitosa de la API
      mock_get.return_value.status_code = 200
      mock_get.return_value.json.return_value = {
         "data": [{"iataCode": "LON"}]
      }

      flight_search = FlightSearch()
      code = flight_search.get_destination_code("Londres")
      self.assertEqual(code, "LON")

   @patch('flight_search.requests.get')
   def test_get_destination_code_not_found(self, mock_get):
      # Simula una respuesta en la que no se encuentra el código IATA
      mock_get.return_value.status_code = 200
      mock_get.return_value.json.return_value = {
         "data": []
      }

      flight_search = FlightSearch()
      code = flight_search.get_destination_code("Ciudad Desconocida")
      self.assertEqual(code, "N/A")

if __name__ == '__main__':
   unittest.main()
