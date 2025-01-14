import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date, datetime, timedelta

class Db_Client:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate('setting/discord-crystal-firebase-adminsdk-pwger-2dbef7c56b.json')
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    def get_all_subscriber_user(self):
        """查詢所有訂閱者資料"""
        try:
            result = []
            ref = self.db.collection("subscriber_users")
            docs = ref.stream()
            for doc in docs:
                result.append(doc.id)
            return result
        except Exception as e:
            print(f"查詢所有訂閱者時發生錯誤: {e}")
            return False
        
    def get_all_detail_lists(self):
        """查詢所有訂閱購買資料"""
        try:
            result = []
            ref = self.db.collection("detail_lists")
            docs = ref.stream()
            for doc in docs:
                result.append(doc.id)
            return result
        except Exception as e:
            print(f"查詢所有訂閱購買資料時發生錯誤: {e}")
            return False

    def add_subscriber_user(self, userId, userName):
        """新增訂閱者資料"""
        try:
            ref = self.db.collection("subscriber_users").document(str(userId))
            ref.set({
                "userId": str(userId),
                "userName": str(userName)
            })
            return True
        except Exception as e:
            print(f"新增訂閱者時發生錯誤: {e}")
            return False
    
    def del_subscriber_user(self, userId):
        """刪除指定訂閱者資料"""
        try:
            ref = self.db.collection("subscriber_users").document(str(userId))
            data = ref.get().to_dict()
            if data == None: return None
            ref.delete()
            return True
        except Exception as e:
            print(f"刪除訂閱者時發生錯誤: {e}")
            return False
        
    def add_subscriber_detail(self, userId, userName, purchaseDate, quantity, payment, amount):
        """新增訂閱資料"""
        try:
            # 確認是否註冊過
            user_doc = self.db.collection("subscriber_users").document(str(userId)).get()
            if not user_doc.exists:
                self.add_subscriber_user(userId, userName)

            dataId = int(datetime.now().timestamp())
            data = {
                "dataId": str(dataId),
                "userId": str(userId),
                "userName": userName,
                "purchaseDate": purchaseDate,
                "quantity": quantity,
                "payment": payment,
                "amount": amount
            }
            ref = self.db.collection("subscriber_users").document(str(userId)).collection("Details").document(str(dataId))
            ref.set(data)
            ref_2 = self.db.collection("detail_lists").document(str(dataId))
            ref_2.set(data)
            return True, dataId
        except Exception as e:
            print(f"新增訂閱資料時發生錯誤: {e}")
            return False, ""

    def del_subscriber_detail(self, dataId):
        """刪除訂閱資料"""
        try:
            ref = self.db.collection("detail_lists").document(str(dataId))
            data = ref.get().to_dict()
            if data == None: return None
            userId = data.get("userId")
            ref.delete()
            ref_2 = self.db.collection("subscriber_users").document(str(userId)).collection("Details").document(str(dataId))
            data = ref_2.get().to_dict()
            if data == None: return False
            ref_2.delete()
            return True
        except Exception as e:
            print(f"刪除訂閱資料時發生錯誤: {e}")
            return False

    def list_subscriber_details(self, userId):
        """列出個人購買明細"""
        try:
            # 確認是否註冊過
            user_doc = self.db.collection("subscriber_users").document(str(userId)).get()
            if not user_doc.exists:
                return None
            
            ref = self.db.collection("subscriber_users").document(str(userId)).collection("Details")
            docs = ref.stream()
            result = []
            for doc in docs:
                result.append(doc.to_dict())
            return result if result != [] else None
        except Exception as e:
            print(f"列出個人購買明細時發生錯誤: {e}")
            return False
    
    def get_detail(self, dataId):
        """查詢特定購買明細"""
        try:
            ref = self.db.collection("detail_lists").document(str(dataId))
            data = ref.get().to_dict()
            return data
        except Exception as e:
            print(f"查詢特定購買明細時發生錯誤: {e}")
            return False
        
if __name__ == "__main__":
    pass