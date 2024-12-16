import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../"))

from models.train import main
from models.emotion_classifier import LyricEmotionClassifier

if __name__ == '__main__':
    classifier = LyricEmotionClassifier()
    classifier.load_weights('C:/Users/Harvey/Desktop/Codes/Python/NLP/LyricToImage/bart_lyric.pt')
    main(classifier.model)