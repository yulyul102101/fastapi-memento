from enum import Enum


class GenderEnum(str, Enum):
    male    = "male"
    female  = "female"
    other   = "other"


class AgeGroupEnum(str, Enum):
    teen            = "10대"
    twenties        = "20대"
    thirties        = "30대"
    forties         = "40대"
    fifties         = "50대"
    sixties_plus    = "60대 이상"


class EmotionEnum(str, Enum):
    joy         = "기쁨"
    sadness     = "슬픔"
    anger       = "화남"
    neutral     = "중립"
    tired       = "지침"