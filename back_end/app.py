from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.mongoDB_function import insert_ticket_info
from utils.request_official_website import get_ticket_info, get_data
from datetime import datetime
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})




# @app.route('/submit', methods=['POST'])
# def submit():
#     data = request.get_json()
#     print(data)
#     insert_ticket_info(data)
#     return jsonify({"message": "Data received and printed."}), 200


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    insert_ticket_info(data)
    if request.method == 'POST':
        departurePort = data.get('departurePort')
        arrivalPort = data.get('arrivalPort')
        departureDate = data.get('departureDate')
        departure_datetime = datetime.fromisoformat(departureDate[:-1])
        departure_date = departure_datetime.date()
        departure_date_str = departure_date.strftime('%Y-%m-%d')
    
        flightDate = data.get('flightDate')
        if flightDate is not None:
            flight_datetime = datetime.fromisoformat(flightDate[:-1])
            flight_date = flight_datetime.date()
            flight_hour = flight_datetime.hour
            flight_minute = flight_datetime.minute
            flight_date_str = flight_date.strftime('%Y-%m-%d')
            airlines = data.get('airlines')
            flightNumber = data.get('flightnumber')
        else:
            flight_date_str = None
            flight_hour = None
            flight_minute = None
            flight_date_str = None
            flightNumber = None
        email = data.get('email')

    ticket_tmp = {
        'arrivalPort': arrivalPort,
        'departureDate': departure_date_str,
        'flightNumber': flightNumber,
        'flight_hour': flight_hour,
        'flight_minute': flight_minute,
        'email': email,
        'flightDate': flight_date_str,
        'airlines': airlines
    }
    print(ticket_tmp)
    get_ticket_info(ticket_tmp)
    return jsonify({"message": "Data received and printed."}), 200
if __name__ == '__main__':
    app.run(port=8000, debug=True)
