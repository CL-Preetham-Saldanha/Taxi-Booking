# login credentials
from cmath import cos
import json
from turtle import distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class drive:
    OTP = 12

    def confirmRide(self):
        OTPin = input("Enter the OTP\n")
        while True:
            if OTPin == self.OTP:
                print("Your ride has started\n")
                end = input("Enter anything if ride has ended")
                break
            else:
                OTPin = int(input("Re Enter OTP\n"))
                break


class user:

    username = "Preetham"
    password = "12345"
    distance = 0
    amount = 0
    OTP = 12

    def checkCredentials(self):
        name = input("enter your username\n")
        password = input("enter your password\n")

        if name == self.username and password == self.password:
            print("Succesfull login\n")
            return True
        else:
            print(
                "Either username or password entered is incorrect, please try again\n"
            )
            return False

    def createAccount(self):
        name = input("enter your username\n")
        npassword = input("enter your password\n")
        cpassword = input("enter your password again to confirm\n")

        if npassword == cpassword:
            self.username = name
            self.password = npassword
        else:
            print("passwords are not matching please create account again\n")
            self.createAccount()

    def findDistance(self):
        pickupPoint = input("Enter place you want to be picked from\n")
        destination = input("Enter your destination\n")
        geolocator = Nominatim(user_agent="Booking_app")

        locationP = geolocator.geocode(pickupPoint)
        print(locationP.address)
        locationD = geolocator.geocode(destination)
        print(locationD.address)

        locationPCordinates = (locationP.latitude, locationP.longitude)
        locationDCordinates = (locationD.latitude, locationD.longitude)

        # newport_ri = (41.49008, -71.312796)
        # cleveland_oh = (41.499498, -81.695391)

        self.distance = (
            geodesic(locationDCordinates, locationPCordinates).miles / 1.609344
        )
        print("your distance is ", str(self.distance))
        # self.distance = geodesic(cleveland_oh, newport_ri).miles / 1.609344

    def selectCab(self):
        f = open("data.json")
        Data = json.load(f)
        f.close()
        taxiData = Data["data"]
        while True:
            print("select the cab from below\n")
            for i in range(1, min(len(taxiData), 10)):
                print(
                    str(i) + "Car type: ",
                    taxiData[i]["Type"],
                    "\n",
                    "CostPerKM: ",
                    taxiData[i]["costPerKM"],
                    "\n",
                    "Rating: ",
                    taxiData[i]["rating"],
                    "\n",
                )
            index = int(input("Enter the number representing cab\n"))
            cindex = int(input("Confirm your car by entering number again\n"))
            if cindex == index:
                if index > 0 and index <= min(len(taxiData), 10):
                    self.amount = round(
                        self.distance * float(taxiData[index]["costPerKM"]), 1
                    )
                    print("your distance is ", str(self.distance))

                    print("This cab will cost \u20B9" + str(self.amount))
                    print("OTP is ", str(self.OTP))
                    break
                else:
                    print("Enter valid number")


def main():

    f = open("data.json")
    Data = json.load(f)
    f.close()
    taxiData = Data["data"]
    countOfTaxi = Data["countOfTaxi"]

    print(
        "Do you want to register and add taxi details?\n Enter 'Y' for yes and any key for no \n"
    )
    yesOrNo = input()
    if yesOrNo.lower() == "y":
        while True:
            numberPlate = input("enter Number plate\n")
            type = input("enter the car model\n")
            cost = input("enter cost per Kilo meter\n")

            print(".\n")
            print(".\n")
            print(".\n")
            taxiDetail = {
                "numberPlate": numberPlate,
                "Type": type,
                "costPerKM": cost,
                "rating": "NA",
            }
            taxiData.append(taxiDetail)

            dataDictionary = {"data": taxiData}
            countDictionary = {"countOfTaxi": countOfTaxi + 1}
            modifiedData = dict()
            modifiedData.update(dataDictionary)
            modifiedData.update(countDictionary)
            f = open("data.json", "w")
            json.dump(modifiedData, f)
            f.close()

            print("enter 1.To add another taxi to list 2.Done\n")
            option = int(input())
            if option == 1:
                continue
            elif option == 2:
                print("Thank you")
                break
            else:
                print("wrong input,Enter again")

    myUser = user()
    myDrive = drive()

    while True:
        option = int(input("1.Log in \n2.sign up\n"))
        if option == 1:
            if myUser.checkCredentials():
                myUser.findDistance()
                myUser.selectCab()
                myDrive.confirmRide()
                print("Thank you for travelling with us!")
                #

                break
        elif option == 2:
            myUser.createAccount()
            break
        else:
            print("Invalid input, try again")


if __name__ == "__main__":
    main()
