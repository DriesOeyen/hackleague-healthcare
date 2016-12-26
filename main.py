#!/usr/bin/python

import requests

serverDomain = 'http://192.168.1.10:3000'
lastGuess = ""


def average(array):
    return float(sum(array)) / len(array)


def handleResponse(response):
    if response.status_code == 200:
        body_json = response.json()

        if 'error' in body_json:
            print(body_json['error'])
        else:
            if body_json['gameOver']:
                print("Game over. Here are the results :")
                body_json['results']['nbCuredPatients'] = len(body_json['results']['curedPatients'])
                print(body_json['results'])
            else:
                play(body_json['gameId'], body_json['state'])
    else:
        print("Error : server returned status code " + response.status_code)


def play(gameId, curState):
    move = turn(curState)
    if move is not None:
        payload = {'gameId': gameId, 'action': move}
        r = requests.post(serverDomain + '/api/play', json=payload)
        handleResponse(r)


def start(patientId):
    r = requests.post(serverDomain + '/api/start', json={'patientId': patientId})
    handleResponse(r)

# createResponseHandler(playCB));


def evaluate(teamName):
    r = requests.post(serverDomain + '/api/evaluate', json={'teamName': teamName})
    handleResponse(r)


# createResponseHandler(playCB));


def turn(curstate):
    if curstate['visitCount'] == 0:
        lastGuess = ""

        # Test for sepsis
        if curstate['metrics']['temperature'][-1] > 40 and curstate['metrics']['heartRate'][-1] > 120 and curstate['metrics']['bloodPressure'][-1] < 70:
            lastGuess = "sepsis"
            return {'type': 'TREATMENT', 'treatment': 'Antibio3'}

        # Test for gastro
        tempLength = len(curstate['metrics']['temperature'])
        tempLengthHalf = int(tempLength / 2)
        tempHalf1 = curstate['metrics']['temperature'][0:tempLengthHalf - 20]
        tempHalf2 = curstate['metrics']['temperature'][tempLengthHalf + 20:tempLength]
        if average(tempHalf1) > 37 and average(tempHalf1) < 38 and average(tempHalf2) > 38 and curstate['health'] < 79:
            lastGuess = "gastro"
            return {'type': 'TREATMENT', 'treatment': 'Antibio1'}

        # Test for intoxication
        hrLength = len(curstate['metrics']['heartRate'])
        hrLengthHalf = int(hrLength / 2)
        hrHalf2 = curstate['metrics']['heartRate'][hrLengthHalf:hrLength]
        if average(hrHalf2) > 88:
            lastGuess = "intoxication"
            return {'type': 'TREATMENT', 'treatment': 'Detoxifier'}

        # Test for cold
        if curstate['health'] < 91 and curstate['health'] > 90:
            lastGuess = "cold"
            return {'type': 'WAIT'}

        # Best-guess: assume flu or pneunomia
        lastGuess = "other"
        return {'type': 'TREATMENT', 'treatment': 'Antiviral1'}
    else:
        if curstate['visitCount'] == 1:
            print(lastGuess)  # Surfaces previous guesses that didn't cure the patient

        # Gastro might require multiple rounds of antibiotics
        if lastGuess == "gastro":
            return {'type': 'TREATMENT', 'treatment': 'Antibio1'}

        # Fall-back strategy - don't try this at home!
        return {'type': 'TREATMENT', 'treatment': 'Antiviral1'}

# To run your code with only one patient, use this function. The integer is the id of the patient
# start(1)

# To test your code and evaluate your score, use this function. Your code will run for all the patients available
evaluate("; DROP TABLE users")  # This is our team name :)
