import openai

from app.core.config import settings


class GptApi:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    #LLM 호출해서 답변 받기
    def requestAdvice(self, emotion, text):
        reponse = openai.chat.completions.create(
            model = "gpt-4o",
            messages= [
                {
                    "role":"system",
                    "content":
                        "당신은 친절한 심리상담전문가입니다. 사용자의 감정에 공감해야합니다."
                },
                {
                    "role":"user",
                    "content":
                        f"{text}를 읽고 {text}를 간략하게 1문장 이내로 요약해주세요.\
                        요약한 문장은 ~하셨군요 로 끝맺어야합니다.\
                        {emotion}의 감정에 맞추어 사용자를 응원하는 말을 150자 이내로 작성해주세요."
                }
            ],
            max_tokens = 150
        )
        return reponse.choices[0].message.content


comment_generator = GptApi()