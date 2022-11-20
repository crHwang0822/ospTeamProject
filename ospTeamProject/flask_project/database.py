import pyrebase
import json

class DBhandler:
    def _init_(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_restaurantUpload(self, name, data, img_path):
        restaurant_info = {
            "Rname":data['Rname'],
            "address":data['adress'],
            "tel1":data['tel1'],
            "tel2":data['tel2'],
            "tel3":data['tel3'],
            "foodchoice":data['foodchoice'],
            "moodchoice":data['moodchoice'],
            "pircechoice":data['pircechoice'],
            "parking":data['parking'],
            "openhour":data['openhour'],
            "openmin":data['openmin'],
            "closehour":data['closehour'],
            "closemin":data['closemin'],
            "img_path":img_path
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").child(name).set(restaurant_info)
            print(data,img_path)
            return True
        else:
            return False

    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            if res.key() == name:
                return False
            return True