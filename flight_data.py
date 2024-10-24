class FlightData:
    """
    Esta clase será responsable de manejar la información de los vuelos, es decir,
    buscar los precios de los vuelos, compararlos con los datos existentes en la
    hoja de cálculo, y determinar si se debe enviar una notificación.
    """
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        """
        Constructor para inicializar una nueva instancia de
        flight data con la información de un vuelo específico.

        Parámetros:
        - price: Precio del vuelo
        - origin_airport: Código IATA del aeropuerto de origen
        - destination_airport: Código IATA del aeropuerto de destino
        - out_date: Fecha del vuelo de ida
        - return_date: Fecha del vuelo de vuelta

        Este constructor asegura que cada vez que se cree un objeto de la clase FlightData,
        se rellenarán automáticamente estas propiedades con los detalles del vuelo.
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(data):
    """
    Analiza los datos de vuelos recibidos de la API de Amadeus
    y encuentra la opción de vuelo más barata.

    Argumentos:
        data (dict): Detalles de los vuelos en formato JSON, proveniente de la API

    Devuelve:
        FlightData: Instancia de la clase FlightData que representa el vuelvo más barato encontrado,
        o una instancia de FlightData donde todos los campos son 'NA' si no hay datos disponibles.

    Si data es None o si no contiene vuelos válidos (si la clave 'data' está vacía), se imprime un mensaje
    ("No flight data") y la función retorna un objeto FlightData con todos los campos establecidos en "N/A"
    para indicar que no hay datos disponibles. Esto podría ocurrir si la API no devuelve resultados o
    si has alcanzado el límite de solicitudes en la API de Amadeus.
    """

    # Comprobación de datos válidos
    if data is None or not data['data']:
        print("Sin datos de vuelo")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    # Información del primer vuelo del json, proveniente de la API
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    # Initialize FlightData with the first flight for comparison
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

    # Iterar sobre todos los vuelos para comparar el precio de cada uno con el precio más bajo almacenado
    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"El precio más bajo a {destination} es {lowest_price}€")

    return cheapest_flight