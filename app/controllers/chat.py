from flask import session
from openai import OpenAI

class ChatController:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    
    @classmethod
    def get_response(self, message):
        print(f"Start get response: {message}")
        completion = self.client.chat.completions.create(
            extra_body={},
            model="alibaba/tongyi-deepresearch-30b-a3b:free",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là giáo viên tiếng Nhật dạy học sinh với trình độ N5. Hãy trò chuyện với học sinh bằng tiếng Nhật một cách thân thiện, dễ hiểu và ngắn gọn trong 1-2 câu."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    

