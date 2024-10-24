import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "MAD"

# ==================== Update the Airport Codes in Google Sheet ====================

#  Verificar si sheet_data contiene algún valor para la clave "iataCode".
#  Si no, entonces la columna de Códigos IATA está vacía en la hoja de Google.
#  En este caso, pasamos el nombre de cada ciudad en sheet_data uno por uno
#  a la clase FlightSearch para obtener el código IATA correspondiente
#  para esa ciudad utilizando la API de Búsqueda de Vuelos.
#  Usar el código que recibimos para actualizar el diccionario sheet_data.

for row in sheet_data:
   if row["iataCode"] == "":
      row["iataCode"] = flight_search.get_destination_code(row["city"])
      # desacelerando las solicitudes para evitar el límite de tasa
      time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Search for Flights and Send Notifications ====================
tomorrow = datetime.now() + timedelta(days=1)
three_month_from_today = datetime.now() + timedelta(days=(3 * 30))

for destination in sheet_data:
   print(f"Consiguiendo vuelos para {destination}")
   flights = flight_search.check_flights(
     ORIGIN_CITY_IATA,
     destination["iataCode"],
     from_time=tomorrow,
     to_time=three_month_from_today
   )

   if flights is None:
      print("No se encontraron datos de vuelos")
      continue

   cheapest_flight = find_cheapest_flight(flights)

   if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
      print(f"Se ha encontrado un precio más bajo para ir a {destination['city']}!")
      notification_manager.send_whatsapp(
         message_body=f"Alerta de bajo precio! Solo {cheapest_flight.price}€ para volar "
                     f"desde {cheapest_flight.origin_airport} a {cheapest_flight.destination_airport}, "
                     f"del {cheapest_flight.out_date} al {cheapest_flight.return_date}."
      )
   else:
      print(f"El precio actual para {destination['city']} es {cheapest_flight.price}€, no es más barato.")

   time.sleep(2)  # Pausa para evitar sobrecargar la API