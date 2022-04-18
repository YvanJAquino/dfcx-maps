from google.cloud import firestore

# fs = firestore.Client(project='basic-strata-326019')
# collection = fs.collection('sessions')
# doc_id = '081G3Ku3cLZRhCuCUwafiExMQ'
# document = collection.document(doc_id).get()
# print(document.to_dict())

def text_nearest_template(phone_number) -> str:
    phone_number = f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
    text = f"No problem, we've sent a text to {phone_number}"
    return text

sample = '7862511624'
print(text_nearest_template(sample))