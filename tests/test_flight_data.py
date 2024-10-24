import unittest
from flight_data import find_cheapest_flight, FlightData

class TestFlightData(unittest.TestCase):

   def test_find_cheapest_flight_with_valid_data(self):
      # Datos simulados de la API para probar la función
      fake_data = {
         "data": [
            {
               "price": {"grandTotal": "100"},
               "itineraries": [
                  {"segments": [
                     {"departure": {"iataCode": "MAD", "at": "2024-10-30T12:00"},
                      "arrival": {"iataCode": "LON"}}]},
                  {"segments": [
                     {"departure": {"iataCode": "LON", "at": "2024-11-05T12:00"}}]}
               ]
            }
         ]
      }
      cheapest_flight = find_cheapest_flight(fake_data)

      # Verifica que los datos del vuelo más barato sean correctos
      self.assertEqual(cheapest_flight.price, 100)
      self.assertEqual(cheapest_flight.origin_airport, "MAD")
      self.assertEqual(cheapest_flight.destination_airport, "LON")
      self.assertEqual(cheapest_flight.out_date, "2024-10-30")
      self.assertEqual(cheapest_flight.return_date, "2024-11-05")

   def test_find_cheapest_flight_no_data(self):
      # Caso en que no hay datos de vuelo
      fake_data = None
      cheapest_flight = find_cheapest_flight(fake_data)

      # Verifica que los datos estén marcados como N/A
      self.assertEqual(cheapest_flight.price, "N/A")
      self.assertEqual(cheapest_flight.origin_airport, "N/A")

if __name__ == '__main__':
   unittest.main()
