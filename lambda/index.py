import json
import os
import urllib.request

# Colab FastAPIエンドポイント（/generateが必須）
COLAB_API_URL = os.environ.get("COLAB_API_URL", "https://5f8f-34-19-58-208.ngrok-free.app/generate")

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']

        print("Processing message:", message)

        # FastAPIに送信するリクエスト
        request_payload = {
            "prompt": message
        }

        # HTTP POSTで送信
        req = urllib.request.Request(
            COLAB_API_URL,
            data=json.dumps(request_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req) as res:
            response_body = res.read()
            response_data = json.loads(response_body)

        # FastAPIからの応答
        assistant_response = response_data.get("generated_text", "")

        # 会話履歴をLambda側で維持（任意）
        conversation_history = [
            {"role": "user", "content": message},
            {"role": "assistant", "content": assistant_response}
        ]

        # 成功レスポンスを返す
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": conversation_history
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }