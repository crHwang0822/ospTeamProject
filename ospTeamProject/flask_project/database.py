import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    
    # 식당 데이터 등록 ============================================================================================

    def insert_restaurantUpload(self, name, data, image_path):
        restaurant_info = {
            "Rname":name,
            "address":data['address'],
            "tel1":data['tel1'],
            "tel2":data['tel2'],
            "tel3":data['tel3'],
            "foodchoice":data['foodchoice'],
            "moodchoice":data['moodchoice'],
            "pricechoice":data['pricechoice'],
            "parking":data['parking'],
            "openhour":data['openhour'],
            "openmin":data['openmin'],
            "closehour":data['closehour'],
            "closemin":data['closemin'],
            "site":data['site'],
            "image_path":image_path
        }
        
        
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").push(restaurant_info)
            print(data,image_path)
            return True
        else:
            return False

    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            value=res.val()

            if value['Rname'] == name:
                return False
        return True


    # 리뷰 데이터 등록 ============================================================================================

    def insert_review(self, name, data, image_path):
        review_content = {
            "restaurant_name":data['Rname'],
            "nickname": name,
            "mood": data['moodchoice'],
            "taste": data['taste'],
            "star": data['star'],
            "text": data['text'],
            "image_path": image_path
        }
        self.db.child("review").push(review_content)
        print(data, image_path)
        return True
    


    # 메뉴 데이터 등록 ============================================================================================

    def insert_menuUpload(self,name,data,image_path):
        menu_info={
            "restaurant_name" : data['Rname'],
            "menuname" : data['menuname'],
            "menuprice" : data['menuprice'],
            "menudetail" : data['menudetail'],
            "vegan" : data['vegan'],
            "allergy" : data['allergy'],
            "allergylist" : data['allergylist'],
            "image_path" : image_path
        }

    
        if self.menu_duplicate_check(name,data['Rname']):
                # self.db.child("menu").child(name).set(menu_info)
                self.db.child("menu").push(menu_info)
                print(data,image_path)
                return True
        else:
                return False

    def menu_duplicate_check(self, name, res_name):
        menus = self.db.child("menu").get()
        for m in menus.each():
            value = m.val()
            
            if (value['restaurant_name'] == res_name) and (value['menuname']==name):
                return False
        return True

    # 맛집 이름으로 restaurant 테이블에서 정보 가져오기 =====================================================================================

    def get_restaurant_byname(self,name):
        restaurants=self.db.child("restaurant").get()
        target_value=""
        for res in restaurants.each():
            value=res.val()

            if value['Rname']==name:
                target_value=value
        return target_value


    # 맛집 이름으로 review 테이블에서 평점 가져와서 평균 계산하기 ===========================================================================

    def get_avgrate_byname(self,name):
        reviews=self.db.child("review").get()
        rates=[]

        for res in reviews.each():
            value=res.val()
            if value['restaurant_name']==name:
                rates.append(float(value['star']))

        if len(rates)==0:
            return 0
        else:
            return round(sum(rates)/len(rates), 2)
    
    # 맛집 이름으로 review 테이블에서 별점 가져와서 리뷰 개수 구하기 ======================================================================
    
    def get_reviewnum_byname(self,name):
        reviews=self.db.child("review").get()
        rates=[]

        for res in reviews.each():
            value=res.val()
            if value['restaurant_name']==name:
                rates.append(float(value['star']))
            
        return len(rates)

    # 맛집 이름으로 review 테이블에서 정보 가져오기 ======================================================================

    def get_review_byname(self, name):
        reviews=self.db.child("review").get()
        target_value=[]

        for res in reviews.each():
            value=res.val()

            if value['restaurant_name']==name:
                target_value.append(value)
        return target_value


    # 맛집등록 테이블에서 데이터 가져오기 ======================================================================

    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants

    # review 테이블에서 데이터 가져오기 ======================================================================

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    # 음식 카테고리(foodchoice)와 분위기(moodchoice)로 레스토랑 가져오기 ======================================================================

    def get_restaurants_byfoodchoice(self, foodchoice, moodchoice):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['foodchoice'] == foodchoice:
                if value['moodchoice']==moodchoice:
                    target_value.append(value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict



    # 음식 종류로 레스토랑 가져오기 ======================================================================

    def get_restaurants_byfoodchoice(self, foodchoice):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['foodchoice'] == foodchoice:
                target_value.append(value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict
    
    # 식당의 value 중 Rname만 리턴해주는 함수 ======================================================================

    def get_restaurantsName(self):
        restaurants = self.db.child("restaurant").get()
        names=[]

        for res in restaurants.each():
            value=res.val()
            names.append(value['Rname'])

        return names

    # 식당이름기반으로 등록 메뉴 검색하여 가져오기 ======================================================================

    def get_food_byname(self, name):
        menu = self.db.child("menu").get()
        target_value={}

        for res in menu.each():
            value = res.val()
            key=res.key()
            if value['restaurant_name'] == name:
                target_value[key]=value
        return target_value
    

    # 분위기(moodchoice)와 category로 데이터 가져오기 ======================================================================

    def get_restaurants_bymoodchoice(self,foodchoice,cate):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['foodchoice'] == foodchoice:
                if value['moodchoice'] == cate:
                    target_value.append(value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict

     # 분위기(moodchoice)로 데이터 가져오기 ======================================================================

    def get_restaurants_byOnlymoodchoice(self,cate):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['moodchoice'] == cate:
                target_value.append(value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict