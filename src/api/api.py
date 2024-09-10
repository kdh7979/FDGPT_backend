import time
import json

def get_next_conversation(model_id, conversation):
    # res = requests.post('/api/inference/conversation', json={"model_id": room_id, "conversation": conversation})

    time.sleep(2)
    res = {
        "content" : "chatGPT says ..." # ChatGPT 응답
    }
    return res


def get_fraud_detection(conversation):
    # requests.post('/api/inference/fraud_detect', json={
    #     "conversation" : conversation
    # })
    time.sleep(0.5)
    res = {
        "is_fraud" : True,
        "warning" : "이 글은 사기일수도 있습니다?" # 경고 메세지
    }
    return res