import json

import paho.mqtt.client as mqtt
import requests
from matplotlib import pyplot as plt

import FlightPlan as FP
import calculateParameters as CP

global_broker_address = 'localhost' # '10.10.10.1'  # "broker.hivemq.com"
# global_broker_address = '10.10.10.1'
global_broker_port = 8000


# API_URL = "http://localhost:8080/"


def on_message_function(cli, userdata, message):
    global client

    splited = message.topic.split("/")
    origin = splited[0]
    destination = splited[1]
    command = splited[2]

    if command == 'Connect':
        print('Connection and subscription.')
        client.subscribe('webApplication/server/createFlightPlan')
        # client.subscribe('webApplication/server/getValue')
        client.subscribe('webApplication/server/calculateParameters')
        # client.subscribe('webApplication/server/StartVideoStream')
        client.subscribe('webApplication/server/createPerimeterFlightPlan')
        print('Connected.')

    if command == "calculateParameters":
        print('Calculate distances between photos.')
        msg = json.loads(message.payload.decode("utf-8"))

        hfov = msg['hfov']
        vfov = msg['vfov']
        h_overlap = msg['h_overlap']
        v_overlap = msg['v_overlap']
        height = msg['height']

        d_length, d_width = CP.calculate_distance_between_photos(height, h_overlap, v_overlap, hfov, vfov)

        result = {'d_length': d_length, 'd_width': d_width}

        client.publish("server/" + origin + '/calculatedParameters', json.dumps(result))
        print('Distances between photos calculated.')

    if command == "createFlightPlan":
        print('Flight plan creation.')
        msg = json.loads(message.payload.decode("utf-8"))  # print('msg =\n', msg)

        list_pts = []
        points = msg['points']  # print('points =\n', points)

        for point in points:
            new_point = point['lat'], point['lng']
            list_pts.append(new_point)  # print('list_created :\n', list_pts)

        if len(list_pts) == 2:
            # flight_points = list_pts
            flight_points, stops = FP.rectangle_flight_plan(list_pts[0], list_pts[1], float(msg['d_length']), float(msg['d_width']))

        else:
            flight_points, stops = FP.create_flight_plan(list_pts, float(msg['d_length']), float(msg['d_width']))

        result = {'flight_points': flight_points, 'stops_points': stops}

        client.publish("server/" + origin + '/createdFlightPlan', json.dumps(result))
        print('Flight plan created and sent !')

        """Plots, not necessary.
        # print('axis')
        plt.axis()
        # print('first_plot')
        FP.plot_pts(list_pts, style='-', color='y', wait=True)
        sorted_pts = FP.sorted_points(list_pts)
        # print('second_plot')
        FP.plot_pts(sorted_pts, style=':', color='b', wait=True)
        # print('last_plot')
        FP.plot_pts(flight_points, style='-', color='r', wait=True)
        FP.plot_pts(stops, style='--', color='g', wait=False)
        """

    if command == "createPerimeterFlightPlan":
        print('Perimeter Flight plan creation.')
        msg = json.loads(message.payload.decode("utf-8"))  # print('msg =\n', msg)

        list_pts = []
        points = msg['points']  # print('points =\n', points)
        d = float(msg['d'])

        for point in points:
            new_point = point['lat'], point['lng']
            list_pts.append(new_point)  # print('list_created :\n', list_pts)

        flight_points = list_pts
        stops = [list_pts[0]]

        for i in range(0, len(list_pts) - 1):
            next_stops = FP.stops_on_a_line(list_pts[i], list_pts[i + 1], d)
            stops = stops + next_stops[1:]

        print("Stops : ", stops)

        result = {'flight_points': flight_points, 'stops_points': stops}
        client.publish("server/" + origin + '/createdPerimeterFlightPlan', json.dumps(result))

        print('Perimeter flight plan created and sent !')


if __name__ == '__main__':
    client = mqtt.Client(transport="websockets")

    client.on_message = on_message_function

    client.connect(global_broker_address, global_broker_port)
    client.subscribe('webApplication/server/Connect')
    print("Waiting commands")

    client.loop_forever()



    # client = mqtt.Client("ComputeService")
    # By the moment, the data service only can store positions (sent by the autopilot service)
    # and provide the stored positions
    # client.subscribe("autopilotService/dataService/storePosition")
    # client.subscribe("+/dataService/getStoredPositions")
    # client.subscribe("+/ComputeService/createFlightPlan")

