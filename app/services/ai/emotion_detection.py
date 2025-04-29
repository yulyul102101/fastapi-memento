from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

from app.models.enums import EmotionEnum


class SentiAnalysis:
    def __init__(self, device=torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        self.model_name = "nlp04/korean_sentiment_analysis_kcelectra"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(device)  # ➤ GPU로 이동
        self.model.eval()
        self.selected_labels = {
            0: EmotionEnum.joy,     # 기쁨(행복한)
            5: EmotionEnum.neutral, # 일상적인
            7: EmotionEnum.sadness, # 슬픔(우울한)
            8: EmotionEnum.tired,   # 힘듦(지침)
            9: EmotionEnum.anger    # 짜증남
        }

    def analyze_emotion(self, content):
        inputs = self.tokenizer(content, return_tensors="pt", truncation=True, padding=True).to(
            torch.device("cuda" if torch.cuda.is_available() else "cpu"))  # ➤ 입력도 GPU로
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)

        filtered_probs = {i: probs[0][i].item() for i in self.selected_labels}
        pred_label = max(filtered_probs, key=filtered_probs.get)

        print(f"[EMOTION] 예측 감정: {self.selected_labels[pred_label]} (score: {filtered_probs[pred_label]:.2f})")
        return self.selected_labels[pred_label], filtered_probs[pred_label]


sa = SentiAnalysis()