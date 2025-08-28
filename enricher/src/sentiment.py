from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self._analyzer = SentimentIntensityAnalyzer()

    def sentiment_analyzer(self, text: str) -> str:
        sentiment_score = self._analyzer.polarity_scores(text)
        compound_score = sentiment_score['compound']
        if compound_score > 0.5:
            return "positive"
        elif compound_score > -0.5:
            return "neutral"
        return "negative"