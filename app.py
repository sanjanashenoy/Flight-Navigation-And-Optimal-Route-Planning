from flask import Flask, request, jsonify, render_template
import requests
import heapq
import psycopg2

app = Flask(__name__)

# Define your API key and URL
WEATHER_API_KEY = '4073a6f015e2f0e8472f4e0876d4f495'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather_conditions(airport_code):
    airport_to_city = {
        'IND': 'Indianapolis',
        'ISP': 'Islip',
        'JAN': 'Jackson',
        'JAX': 'Jacksonville',
        'LAS': 'Las Vegas',
        'LAX': 'Los Angeles',
        'LBB': 'Lubbock',
        'LIT': 'Little Rock',
        'MAF': 'Midland',
        'MCI': 'Kansas City',
        'MCO': 'Orlando',
        'MDW': 'Chicago',
        'MHT': 'Manchester',
        'MSY': 'New Orleans',
        'OAK': 'Oakland',
        'OKC': 'Oklahoma City',
        'OMA': 'Omaha',
        'ONT': 'Ontario',
        'ORF': 'Norfolk',
        'PBI': 'West Palm Beach',
        'PDX': 'Portland',
        'PHL': 'Philadelphia',
        'PHX': 'Phoenix',
        'PIT': 'Pittsburgh',
        'PVD': 'Providence',
        'RDU': 'Raleigh-Durham',
        'RNO': 'Reno',
        'RSW': 'Fort Myers',
        'SAN': 'San Diego',
        'SAT': 'San Antonio',
        'SDF': 'Louisville',
        'SEA': 'Seattle',
        'SFO': 'San Francisco',
        'SJC': 'San Jose',
        'SLC': 'Salt Lake City',
        'SMF': 'Sacramento',
        'SNA': 'Santa Ana',
        'STL': 'St. Louis',
        'TPA': 'Tampa',
        'TUL': 'Tulsa',
        'TUS': 'Tucson',
        'ABQ': 'Albuquerque',
        'AMA': 'Amarillo',
        'AUS': 'Austin',
        'BHM': 'Birmingham',
        'BNA': 'Nashville',
        'BOI': 'Boise',
        'BUF': 'Buffalo',
        'BUR': 'Burbank',
        'BWI': 'Baltimore',
        'CMH': 'Columbus',
        'CRP': 'Corpus Christi',
        'DAL': 'Dallas',
        'DEN': 'Denver',
        'ELP': 'El Paso',
        'FLL': 'Fort Lauderdale',
        'GEG': 'Spokane',
        'HOU': 'Houston',
        'HRL': 'Harlingen',
        'IAD': 'Washington',
        'ALB': 'Albany',
        'BDL': 'Hartford',
        'DTW': 'Detroit',
        'CLE': 'Cleveland',
        'ORD': 'Chicago',
        'ATL': 'Atlanta',
        'CVG': 'Cincinnati',
        'MKE': 'Milwaukee',
        'MSP': 'Minneapolis',
        'EWR': 'Newark',
        'SUN': 'Hailey',
        'SGU': 'St. George',
        'MSO': 'Missoula',
        'BZN': 'Bozeman',
        'GTF': 'Great Falls',
        'BIL': 'Billings',
        'PSP': 'Palm Springs',
        'HDN': 'Hayden',
        'IAH': 'Houston',
        'DFW': 'Dallas',
        'ASE': 'Aspen',
        'JAC': 'Jackson Hole',
        'SBP': 'San Luis Obispo',
        'FAT': 'Fresno',
        'EUG': 'Eugene',
        'MOD': 'Modesto',
        'LEX': 'Lexington',
        'FSD': 'Sioux Falls',
        'BTV': 'Burlington',
        'ROA': 'Roanoke',
        'MEM': 'Memphis',
        'FAR': 'Fargo',
        'XNA': 'Bentonville',
        'COS': 'Colorado Springs',
        'GUC': 'Gunnison',
        'AZO': 'Kalamazoo',
        'TVC': 'Traverse City',
        'CRW': 'Charleston',
        'TYS': 'Knoxville',
        'SAV': 'Savannah',
        'ICT': 'Wichita',
        'GJT': 'Grand Junction',
        'PIA': 'Peoria',
        'SGF': 'Springfield',
        'MSN': 'Madison',
        'CID': 'Cedar Rapids',
        'MLI': 'Moline',
        'DRO': 'Durango',
        'CHS': 'Charleston',
        'DSM': 'Des Moines',
        'ATW': 'Appleton',
        'GRB': 'Green Bay',
        'FWA': 'Fort Wayne',
        'DAY': 'Dayton',
        'LNK': 'Lincoln',
        'FCA': 'Kalispell',
        'IDA': 'Idaho Falls',
        'HSV': 'Huntsville',
        'CWA': 'Wausau',
        'MFR': 'Medford',
        'PSC': 'Pasco',
        'SYR': 'Syracuse',
        'SBA': 'Santa Barbara',
        'RAP': 'Rapid City',
        'YUM': 'Yuma',
        'RDM': 'Redmond',
        'LGB': 'Long Beach',
        'MTJ': 'Montrose',
        'RDD': 'Redding',
        'CLD': 'Carlsbad',
        'SBN': 'South Bend',
        'HPN': 'White Plains',
        'SPI': 'Springfield',
        'MBS': 'Saginaw',
        'LAN': 'Lansing',
        'TWF': 'Twin Falls',
        'MRY': 'Monterey',
        'SMX': 'Santa Maria',
        'ACV': 'Arcata',
        'BFL': 'Bakersfield',
        'CEC': 'Crescent City',
        'CIC': 'Chico',
        'PMD': 'Palmdale',
        'EKO': 'Elko',
        'IYK': 'Inyokern',
        'OXR': 'Oxnard',
        'IPL': 'Imperial',
        'PIH': 'Pocatello',
        'CPR': 'Casper',
        'BTM': 'Butte',
        'HLN': 'Helena',
        'BLI': 'Bellingham',
        'CAK': 'Akron',
        'RFD': 'Rockford',
        'COD': 'Cody',
        'SLE': 'Salem',
        'LWS': 'Lewiston',
        'GRR': 'Grand Rapids',
        'AVP': 'Wilkes-Barre',
        'ABE': 'Allentown',
        'BIS': 'Bismarck',
        'GSP': 'Greenville',
        'CDC': 'Cedar City',
        'BMI': 'Bloomington',
        'YKM': 'Yakima',
        'CLT': 'Charlotte',
        'HNL': 'Honolulu',
        'KOA': 'Kona',
        'OGG': 'Kahului',
        'JFK': 'New York',
        'LIH': 'Lihue',
        'MDT': 'Harrisburg',
        'LGA': 'New York',
        'RIC': 'Richmond',
        'BOS': 'Boston',
        'EGE': 'Eagle',
        'ROC': 'Rochester',
        'GSO': 'Greensboro',
        'DCA': 'Washington',
        'SJU': 'San Juan',
        'STT': 'Charlotte Amalie',
        'MIA': 'Miami',
        'ANC': 'Anchorage',
        'MYR': 'Myrtle Beach',
        'STX': 'Christiansted',
        'ILM': 'Wilmington',
        'VPS': 'Valparaiso',
        'SRQ': 'Sarasota',
        'PNS': 'Pensacola',
        'DAB': 'Daytona Beach',
        'CAE': 'Columbia',
        'GPT': 'Gulfport',
        'MLB': 'Melbourne',
        'PHF': 'Newport News',
        'MFE': 'McAllen',
        'SHV': 'Shreveport',
        'MGM': 'Montgomery',
        'PFN': 'Panama City',
        'CHA': 'Chattanooga',
        'FAY': 'Fayetteville',
        'AGS': 'Augusta',
        'MOB': 'Mobile',
        'BTR': 'Baton Rouge',
        'BGR': 'Bangor',
        'GNV': 'Gainesville',
        'ABY': 'Albany',
        'DHN': 'Dothan',
        'AVL': 'Asheville',
        'EVV': 'Evansville',
        'FNT': 'Flint',
        'TRI': 'Bristol',
        'OAJ': 'Jacksonville',
        'AEX': 'Alexandria',
        'SWF': 'Newburgh',
        'EWN': 'New Bern',
        'MEI': 'Meridian',
        'PWM': 'Portland',
        'GRK': 'Killeen',
        'GTR': 'Golden Triangle',
        'LFT': 'Lafayette',
        'LYH': 'Lynchburg',
        'HHH': 'Hilton Head',
        'EYW': 'Key West',
        'VLD': 'Valdosta',
        'CSG': 'Columbus',
        'MLU': 'Monroe',
        'TLH': 'Tallahassee',
        'ACY': 'Atlantic City',
        'FSM': 'Fort Smith',
        'MCN': 'Macon',
        'CHO': 'Charlottesville',
        'TOL': 'Toledo',
        'FLO': 'Florence',
        'BQK': 'Brunswick',
        'SCE': 'State College',
        'ITO': 'Hilo',
        'LAW': 'Lawton',
        'SPS': 'Wichita Falls',
        'ABI': 'Abilene',
        'CLL': 'College Station',
        'TYR': 'Tyler',
        'GGG': 'Longview',
        'ACT': 'Waco',
        'SJT': 'San Angelo',
        'TXK': 'Texarkana',
        'LRD': 'Laredo',
        'CMI': 'Champaign',
        'ROW': 'Roswell',
        'RST': 'Rochester',
        'MQT': 'Marquette',
        'LSE': 'La Crosse',
        'DBQ': 'Dubuque',
        'KTN': 'Ketchikan',
        'JNU': 'Juneau',
        'SIT': 'Sitka',
        'PSG': 'Petersburg',
        'CDV': 'Cordova',
        'YAK': 'Yakutat',
        'BET': 'Bethel',
        'BRW': 'Barrow',
        'SCC': 'Prudhoe Bay',
        'FAI': 'Fairbanks',
        'ADQ': 'Kodiak',
        'WRG': 'Wrangell',
        'OME': 'Nome',
        'OTZ': 'Kotzebue',
        'ADK': 'Adak',
        'PSE': 'Ponce',
        'BQN': 'Aguadilla',
        'MKG': 'Muskegon',
        'DLG': 'Dillingham',
        'AKN': 'King Salmon',
        'LWB': 'Lewisburg',
        'WYS': 'West Yellowstone'
    }
    
    city = airport_to_city.get(airport_code)
    if not city:
        print(f"No city mapping found for airport code: {airport_code}")
        return "Unknown", {'temp': 0, 'feels_like': 0, 'temp_min': 0, 'temp_max': 0, 'pressure': 0, 'humidity': 0}

    try:
        url = WEATHER_API_URL
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        weather_desc = data['weather'][0]['description']
        weather_main = data['main']

        return weather_desc, weather_main
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        # Return default values when an error occurs
        return "Unknown", {'temp': 0, 'feels_like': 0, 'temp_min': 0, 'temp_max': 0, 'pressure': 0, 'humidity': 0}


def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    seen = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in seen:
            continue

        path = path + [node]
        seen.add(node)

        if node == end:
            return (cost, path)

        for (next_node, distance) in graph.get(node, []):
            if next_node not in seen:
                heapq.heappush(queue, (cost + distance, next_node, path))

    return float("inf"), []

def build_graph():
    try:
        conn = psycopg2.connect(
            dbname="route_opti",
            user="postgres",
            password="sanj123",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("SELECT origin_airport, destination_airport, distance FROM routes")
        rows = cur.fetchall()
        
        graph = {}
        for origin, destination, distance in rows:
            if origin not in graph:
                graph[origin] = []
            graph[origin].append((destination, distance))
        
        cur.close()
        conn.close()
        
        return graph
    except Exception as e:
        return {}

graph = build_graph()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def get_route():
    data = request.json
    origin = data['origin']
    destination = data['destination']
    print(f"Received route request from {origin} to {destination}")

    # Check weather at origin and destination
    weather_origin_desc, weather_origin_main = get_weather_conditions(origin)
    weather_dest_desc, weather_dest_main = get_weather_conditions(destination)
    print(f"Weather at {origin}: {weather_origin_desc}, Temp: {weather_origin_main['temp']}°C")
    print(f"Weather at {destination}: {weather_dest_desc}, Temp: {weather_dest_main['temp']}°C")

    if "thunderstorm" in weather_origin_desc.lower() or "thunderstorm" in weather_dest_desc.lower():
        return jsonify({'error': 'Rerouting due to thunderstorm'}), 503

    # Predict delays based on weather conditions (simple example)
    delay_prediction = {
        'thunderstorm': 30,
        'rain': 15,
        'snow': 20,
        'clear': 0
    }

    # Assume delay due to weather is the max of origin and destination weather conditions
    delay_origin = delay_prediction.get(weather_origin_desc.lower(), 0)
    delay_destination = delay_prediction.get(weather_dest_desc.lower(), 0)
    total_delay = max(delay_origin, delay_destination)

    # Calculate total cost and optimal path
    cost, path = dijkstra(graph, origin, destination)
    if cost == float("inf"):
        return jsonify({'error': 'No route found'}), 404

    # Print optimal path and return response with delay information
    print(f"Optimal path from {origin} to {destination} with total cost {cost}: {path}")

    # Assume predicted delay is sum of origin and destination delays
    predicted_delay = delay_origin + delay_destination

    # Assuming you calculate the predicted delay and include it in the response
    return jsonify({
        'cost': cost,
        'path': path,
        'weather_origin': {
            'description': weather_origin_desc,
            'main': weather_origin_main
        },
        'weather_destination': {
            'description': weather_dest_desc,
            'main': weather_dest_main
        },
        'total_delay': total_delay,
        'predicted_delay': predicted_delay  # Include the predicted delay here
    })




if __name__ == '__main__':
    app.run(debug=True)
