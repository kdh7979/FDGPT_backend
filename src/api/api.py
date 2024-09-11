import time
import json
import requests

def get_next_conversation(model_id, conversation):
    res = requests.post('http://10.30.0.35:5000/api/inference/conversation', json={"model_id": model_id, "conversation": conversation})

    # time.sleep(2)
    # res = {
    #     "content" : "chatGPT says ..." # ChatGPT 응답
    # }
    return res.json()


def get_fraud_detection(conversation):
    res = requests.post('http://10.30.0.35:5000/api/inference/fraud_detect', json={
        "conversation" : conversation
    })
    # time.sleep(0.5)
    # res = {
    #     "is_fraud" : True,
    #     "warning" : "이 글은 사기일수도 있습니다?" # 경고 메세지
    # }
    print("-------------------------", res.text)
    return res.json()