import whisper
import torch


class VoiceToText:
    def __init__(self, device=torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        self.whisper_model = whisper.load_model("small").to(device)

    def transcribe_audio(self, file_path):
        print(f"[INFO] '{file_path}' 파일을 텍스트로 변환 중...")
        result = self.whisper_model.transcribe(file_path)
        content = result["text"].strip()
        print(f"[TEXT] 인식된 문장: {content}")
        return content


stt = VoiceToText()