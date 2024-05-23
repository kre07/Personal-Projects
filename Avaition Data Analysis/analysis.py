'''  
Kritagya Sharma
This code analyzes flight data to determine the most used aircraft, the price of tickets, and the duration of each flight.

'''

def parse_flight_data(file_path):
    try:
        with open(file_path,"r") as file:
            
            next (file)  # skips header
            all_flights= {}
            for line in file: # Converts every line into a list
                if line.strip() == "": # Skips empty lines
                    continue
                file_turned_into_list = line.strip().split(",") # creates a list            
                flight_duration = file_turned_into_list[6].split(":")
                flight_duration = int(flight_duration[0]) * 60 + int(flight_duration[1])



                flight_info = {
                    'Aircraft': file_turned_into_list[8],
                    'Airline': file_turned_into_list[5],
                    'ArrivalAirport': file_turned_into_list[2],
                    'ArrivalTime': file_turned_into_list[4],
                    'AvgTicketPrice': int(file_turned_into_list[7]),
                    'DepartureAirport': file_turned_into_list[1],
                    'DepartureTime': file_turned_into_list[3],
                    'FlightDuration': (flight_duration),
                    'PassengerCount': int(file_turned_into_list[9])
                }   
                all_flights[file_turned_into_list[0].lower()] = flight_info # 0th index is flight number

            return all_flights
            

    except IOError:
        return -1                
                  
def calculate_average_ticket_price(all_flights, airline):
    total_price = 0
    flights_count = 0
    for info in all_flights: 
        new_info = all_flights[info]  # Get the value instead of the keys
        if new_info['Airline'].lower() == airline.lower():
            total_price +=new_info['AvgTicketPrice']
            flights_count += 1

    if flights_count == 0:
        return 0
    else: 
        avg_ticket_price = total_price / flights_count
        return avg_ticket_price

    

def get_total_passengers_by_airline(all_flights):
    total_passengers_by_airline = {}

    for flight_number in all_flights:
        flight_value = all_flights[flight_number] 
        airline = flight_value['Airline']  # Get the airline name
        passenger_count = flight_value['PassengerCount']  # Get passenger number

        if airline in total_passengers_by_airline: # If that airline is already in the dictionary, then add onto it
            total_passengers_by_airline[airline] += passenger_count
        else:  # If its not in the dictionary, make a new key and value for it
            total_passengers_by_airline[airline] = passenger_count

    return total_passengers_by_airline


def get_overnight_flights(all_flights):
    overnight_flights = []

    for flight_number, flight_info in all_flights.items():
        departure = str(flight_info['DepartureTime'])# converting into a list so it is in [2023-11-25, 06:25:00] and it can access the first index which is the hours.
        departure_split = int(departure.split(" ")[1][:2]) 
        arrival = str(flight_info['ArrivalTime'])
        arrival_split = int(arrival.split(" ")[1][:2])

        if departure_split > arrival_split: 
            overnight_flights.append(flight_number)

    return overnight_flights


def get_top_n_aircraft(all_flights, n=3):
    aircraft_count = {}
    
    # Count the occurrences of each aircraft
    for flight_info in all_flights.values():
        aircraft = flight_info['Aircraft'].lower()  
        if aircraft in aircraft_count:
            aircraft_count[aircraft] += 1 
        else:
            aircraft_count[aircraft] = 1
    

    sorted_aircraft = sorted(aircraft_count.items(), key=lambda x: x[1], reverse=True) # Sort the aircraft 

    top_5_aircraft = []
    count = 0  # Initialize  to keep track of how many aircraft models we have added to the list
    for aircraft in sorted_aircraft:
        if count < n:  # Check if we have added enough aircraft models
            top_5_aircraft.append(aircraft[0])  # Add the aircraft model 
            count += 1  # keep track of aircrafts
        else:
            break  # Exit the loop if enough aircrafts are reached

    if n > len(sorted_aircraft):
        raise ValueError("Invalid n value!")
    
    return top_5_aircraft



def get_total_duration(all_flights, airports): #  calculates the total flight duration for each airline in the dataset
    airline_durations = {}  
  
    airport_code_lowercase = []
    for airport_code in airports: # Convert Airport codes to lower case
        airport_code_lowercase.append(airport_code.lower()) 

    for key_id in all_flights:
        flight_info = all_flights[key_id]
        airline_durations[flight_info['Airline']] = 0

    for flight_number, flight_info in all_flights.items():
        airport_departure = flight_info['DepartureAirport'].lower() # Initialize departure times
        airport_arrival = flight_info['ArrivalAirport'].lower() # Initialize arrival times

        if airport_departure in airport_code_lowercase and airport_arrival in airport_code_lowercase: # Check if departure and arrival dates are in the lowercase list
            airline = flight_info['Airline']
            duration = flight_info['FlightDuration']

            if airline in airline_durations: 
                airline_durations[airline] += duration 
            else:               
                airline_durations[airline] = duration

    return airline_durations







