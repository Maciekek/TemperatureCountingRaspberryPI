__author__ = 'Maciej'
import re
import time
import datetime

tempSensorPath = "../sys/bus/w1/devices/"

def readFromFile(fileName):
    file = open(fileName+"28-000006bf05f0/w1_slave");
    text = file.read();
    file.close();
    return text


def extractTemperature(temperatureSensor):
    return re.search('(?<=t=).*',temperatureSensor).group(0);


def getActualTemperature():
    temp = extractTemperature(readFromFile(tempSensorPath));
    return int(temp);


def countProcessType(cycle, lastTemp):
    print(lastTemp)
    print(getActualTemperature());
    print(cycle[1]);
    time.sleep(2)
    return lastTemp


def informationCycle(cycle):
    cycleTime = datetime.datetime.now() - cycle[0]
    cycleType = cycle[1];

    print("\n")
    print("CZAS CYKLU")
    print(cycleTime);
    print("\n")

    saveCycleTime(cycleTime, cycleType);
    pass


def saveCycleTime(cycleTime, cycleType):
    print(cycleTime)
    file = open('files/temp1.txt', "a")
    localtime   = time.localtime()
    timeString  = time.strftime("%Y:%m:%d %H-%M-%S", localtime)

    file.write(timeString +" Czas:  " + str(cycleTime) + " cykl: " + cycleType + "\n");
    file.close();

    pass


def watchTemperature():
    lastTemp = 0
    while True:
        cycle = []

        if lastTemp > getActualTemperature():
            cycle.append(datetime.datetime.now())
            cycle.append("chlodzenie")
            while lastTemp >= getActualTemperature():
                lastTemp = countProcessType(cycle, lastTemp)
                time.sleep(60);
            informationCycle(cycle)
            cycle = []

        if lastTemp < getActualTemperature():
            cycle.append(datetime.datetime.now())
            cycle.append("grzanie")
            while lastTemp <= getActualTemperature():
                lastTemp = countProcessType(cycle, lastTemp)
                time.sleep(60);
            informationCycle(cycle)

        time.sleep(2)

    pass


def main():

    temperatureSensor = readFromFile("../sys/bus/w1/devices/");
    print(temperatureSensor);

    #for i in range(10):
    watchTemperature();


    actualTemperature = extractTemperature(temperatureSensor);
    print("Aktualna temperatura: "+ actualTemperature);


    return 0;


main();
