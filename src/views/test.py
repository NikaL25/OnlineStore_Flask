from intasend import APIService

API_PUBLISHABLE_KEY = 'ISPubKey_test_813ac5a8-6ddc-48e9-bc7c-77a6c32baa9d'

API_TOKEN = 'ISSecretKey_test_845b83ed-b8e9-43bd-ae6e-c713611e7971'

phone_number = +254995551118

service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

create_order = service.collect.mpesa_stk_push(phone_number=phone_number, email='nikalomiashvili25@gmail.com', amount=100, narrative='Purchase of items')

print(create_order)