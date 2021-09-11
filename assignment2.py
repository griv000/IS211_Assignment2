import argparse
import datetime
import urllib.request
import logging


def downloadData(myURL):
    url = myURL
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    return data


def processData(data):
    myDict = dict()
    myTemp = data
    myWorking = myTemp.split("\n")
    linenum = 1
    for row in myWorking:
        myList = row.split(",")
        try:
            myDate = datetime.datetime.strptime(myList[2],'%d/%m/%Y')
            myTuple = (myList[1], myDate)
            myDict[myList[0]] = myTuple
        except:
            myLog.error("Error processing line #" + str(linenum) + " for ID #" + str(myList[0]))
            pass
        linenum += 1
    return myDict


def displayPerson(id, personData):
    if id in personData:
        myList = personData.get(id)
        print("Person #" + id , "is" , myList[0] , "with a birthday of", myList[1].strftime("%Y%m%d"))
    else:
        print("No user found with that id")


def main(url):
    print(f"Running main with URL = {url}...")
    myCSV = downloadData(url)
    newDict = dict()
    newDict = processData(myCSV)
    def InputFunct():
        myInput = input("Please enter an ID to lookup: ")
        try:
            int(myInput)
            if int(myInput) > 0:
                displayPerson(myInput,newDict)
                InputFunct()
            else:
                print("Exit")
                quit()
        except ValueError:
            print("Not a valid ID number")
            InputFunct()
    InputFunct()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    logging.basicConfig(filename="errors.log",filemode="w",level=logging.ERROR)
    myLog = logging.getLogger("assignment2")
    main(args.url)