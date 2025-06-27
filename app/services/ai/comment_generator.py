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
                        f"{text}가 비어있거나 문장을 요약할 수 없을 경우 바빠서 일기를 쓰지 못했던 상황을 가정하고 응원하는 말을 작성해주세요.\
                        {text}가 한 문장일 경우 요약하지 않고 {text}와 {emotion}에 맞추어 응원하고 공감하는 말을 150자 이내로 작성합니다.\
                        {text}에 요약할 문장이 있는 경우 {text}를 읽고 {text}를 간략하게 1문장 이내로 요약해주세요.\
                        요약한 문장은 ~하셨군요 로 끝맺어야합니다.\
                        {emotion}의 감정에 맞추어 사용자를 응원하는 말을 150자 이내로 작성해주세요.\
                        답변에는 줄넘김이 없어야합니다."
                }
            ],
            max_tokens = 150
        )
        return reponse.choices[0].message.content


comment_generator = GptApi()