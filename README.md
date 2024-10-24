# Herramienta de Notificación de Ofertas de Vuelos ✈️

Este proyecto utiliza la API de búsqueda de vuelos de **Amadeus** para obtener ofertas de vuelos y comparar los precios más bajos con una **hoja de cálculo de Google**. Si se encuentra un precio más bajo que el registrado, se envía una notificación al usuario a través de WhatsApp usando **Twilio**.

## Tabla de Contenidos

- [Objetivo](#objetivo)
- [Funcionalidades](#funcionalidades)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [APIs Requeridas](#apis-requeridas)
- [Requisitos del programa](#requisitos-del-programa)
- [Instalación](#instalación)
- [Uso](#uso)
- [API de Búsqueda de Vuelos](#api-de-búsqueda-de-vuelos)
- [Notas y Consideraciones](#notas-y-consideraciones)
- [Pruebas](#pruebas)
- [Excepciones Comunes](#excepciones-comunes)

## Objetivo

El objetivo del proyecto es permitir la búsqueda de vuelos utilizando la API de Amadeus y verificar si el precio de un vuelo ha bajado con respecto al precio almacenado en una hoja de Google. Si se detecta un precio más bajo, se notifica al usuario mediante Twilio.

## Funcionalidades

- Buscar vuelos utilizando la API de búsqueda de vuelos de Amadeus.
- Comparar los precios más bajos con los almacenados en una hoja de Google Sheets utilizando la API de Sheety.
- Enviar notificaciones de vuelos baratos vía WhatsApp utilizando la API de Twilio.
- Actualizar la hoja de Google Sheets con los precios más bajos obtenidos, siempre que el nuevo precio sea más bajo.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal del proyecto.
- **API de Google Sheets vía Sheety**: Para gestionar datos en una hoja de cálculo de Google.
- **API de Amadeus**: Para obtener ofertas de vuelos y códigos de aeropuertos.
- **API de Twilio**: Para enviar notificaciones vía SMS o WhatsApp.
- **dotenv**: Para gestionar las claves de API de manera segura.

## APIs Requeridas

- **API de Sheety** para integración con Google Sheets: https://sheety.co/
- **API de Ofertas de Vuelos de Amadeus** para obtener datos de vuelos: https://developers.amadeus.com/
- **API de Twilio** para enviar notificaciones: https://www.twilio.com/docs/messaging/quickstart/python

## Requisitos del programa

- **Buscar vuelos:** Utiliza la API de búsqueda de vuelos de Amadeus y la API de Sheety para llenar la hoja de Google con los códigos IATA de las ciudades y sus precios más bajos.
- **Notificación:** Si el precio de un vuelo es más bajo que el registrado en la hoja de Google, se enviará un mensaje a través de Twilio.
- **Datos en Google Sheets:** Los precios más bajos se almacenan y actualizan en la hoja de Google.

## Instalación

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tu_usuario/flight-deals-finder.git
    cd flight-deals-finder
    ```

2. **Haz una copia de la Hoja de Google**:
   - [Plantilla de Hoja de Google](https://docs.google.com/spreadsheets/d/1wvOQ5LC6tmxOfMJGZ3FPNkkZvG4A45YeIouduCgYy8Y/edit?gid=0)

3. **Configura las variables de entorno**:
   - Crea un archivo `.env` y agrega tus claves de API y otros datos sensibles.
   - Usa el archivo `.env.example` proporcionado como referencia.

4. **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Ejecuta el script**:
    ```bash
    python main.py
    ```

## Uso

- Actualizar los códigos IATA en Google Sheets: El programa verifica si los códigos IATA están vacíos en la hoja de Google y los actualiza utilizando la API de Amadeus. Si no se encuentra un código IATA para alguna ciudad, se imprime un mensaje.
- Buscar vuelos y enviar notificaciones: Para cada ciudad en la hoja de Google, el programa busca vuelos utilizando la API de Amadeus. Si encuentra un vuelo con un precio más bajo que el registrado, envía una notificación por WhatsApp con los detalles del vuelo.
- Actualizar los precios en Google Sheets: Si se encuentra un vuelo más barato, el programa actualiza la hoja de Google con el nuevo precio.

### Flujo de Datos

1. **Datos de Google Sheet**: Almacena nombres de ciudades, códigos IATA y los precios de vuelos actuales.
2. **API de Amadeus**: Se utiliza para obtener ofertas de vuelos y códigos IATA de ciudades y aeropuertos.
3. **API de Twilio**: Envía mensajes SMS o WhatsApp con detalles de vuelos (origen, destino, precio, fecha).

## API de Búsqueda de Vuelos

### Cómo Funciona

- La API de Amadeus devuelve una gran cantidad de vuelos en formato JSON. Este JSON se analiza para encontrar el vuelo más barato.
- La función `find_cheapest_flight()` se encarga de analizar los datos y devolver el vuelo más barato o "N/A" si no se encuentra ningún vuelo.
  - 📌 Puedes usar herramientas como [Json Pathfinder](https://jsonpathfinder.com/) para encontrar fácilmente las rutas dentro del JSON devuelto por la API y extraer los datos relevantes.
- **Formato de fecha:** La API de Amadeus requiere que las fechas se pasen en formato YYYY-MM-DD. Usa strftime() para asegurarte de que las fechas estén en el formato correcto.

### Parámetros de Búsqueda

- El proyecto usa `timedelta` para definir un período de 3 meses desde la fecha actual para buscar vuelos.
- Los resultados están limitados a vuelos directos y se muestran en **euros**.

## Notas y Consideraciones

### Límites de las APIs

- La API de Amadeus tiene un límite de 2000 solicitudes al mes. Si llegas a este límite, la API dejará de devolver datos, lo que puede causar que no se encuentren vuelos. En este caso, deberás esperar a que se renueve el límite o probar con otro entorno de desarrollo.
- La API de Sheety tiene un límite de 200 solicitudes al mes. Asegúrate de no sobrepasar este límite realizando demasiadas actualizaciones en tu hoja de Google.

### Códigos IATA y aeropuertos populares

- Si una ciudad no tiene un código IATA válido o no se encuentra un vuelo para esa ruta, el código "Not Found" no debería usarse para realizar búsquedas, ya que causará un error. Asegúrate de manejar correctamente estos casos.
- Es recomendable concentrarse en aeropuertos populares y rutas principales para maximizar los resultados de la API de Amadeus, ya que algunos aeropuertos o rutas menos concurridas pueden no devolver resultados.

### Formato de la hoja de Google

- Asegúrate de que las celdas de precios en Google Sheets están correctamente formateadas como números y no contienen fórmulas que interfieran con las actualizaciones automáticas.

### Manejo de errores y excepciones

- El proyecto maneja los casos donde no se encuentran vuelos o cuando se alcanza el límite de la API devolviendo un objeto FlightData con valores "N/A". Esto permite que el programa continúe ejecutándose sin fallos.
- Si la API de Amadeus devuelve un error, como el código 429 (límite de solicitudes alcanzado), o si el formato de los parámetros es incorrecto, el programa lo manejará adecuadamente y no se detendrá abruptamente.

### Depuración

- Si no obtienes resultados para ciertos destinos o fechas, puede ser útil cambiar la ciudad de origen a un gran aeropuerto internacional o ajustar las fechas. También puedes verificar manualmente la disponibilidad de vuelos en sitios web como Skyscanner o Kayak para confirmar que hay vuelos disponibles en esas rutas.

### Seguridad del archivo .env:

- Asegúrate de mantener tu archivo .env seguro y fuera de cualquier repositorio público, ya que contiene claves sensibles de API. Puedes agregar un archivo .gitignore para evitar que se suba accidentalmente a GitHub.

## Pruebas

El proyecto incluye pruebas unitarias básicas para las funciones clave del programa. Ejecuta las pruebas con:

```bash
python -m unittest discover -s tests
```

## Excepciones Comunes

- **Límite de solicitudes de API:** Si has alcanzado el límite de la API de Amadeus, recibirás un mensaje con el código de error 429. Puedes probar con diferentes parámetros de búsqueda o esperar hasta que se renueven las solicitudes permitidas.
- **Códigos IATA no válidos:** Si no se encuentra un código IATA, el programa evita realizar la búsqueda de vuelos para esa ciudad.

---

***¡Gracias por echarle un vistazo a este proyecto!*** Siéntete libre de contribuir o modificarlo para adaptarlo a tus propias necesidades. 😊
