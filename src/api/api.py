import time
import json

def get_next_conversation(model_id, conversation):
    # res = requests.post('/api/inference/conversation', json={"model_id": room_id, "conversation": conversation})

    time.sleep(0.3)
    res = {
        "content" : "awdkjahwkduhawduagwdjagwd" # ChatGPT 응답
    }
    return res


def get_fraud_detection(conversation):
    # requests.post('/api/inference/fraud_detect', json={
    #     "conversation" : conversation
    # })
    time.sleep(0.3)
    res = {
        "is_fraud" : "true",
        "warning" : "awdkjahwkduhawduagwdjagwd" # 경고 메세지
    }
    return res