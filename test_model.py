from transformers import pipeline

# load a pre-trained text classification model
#classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# load a fake news classifier
classifier = pipeline("text-classification", model="hamzab/roberta-fake-news-classification")

# test with sample text
#sample_text = "Scientists announce breakthrough in renewable energy technology"

# test with sample text
#real_news = "The Federal Reserve announced a 0.25% interest rate increase following their December meeting."

#fake_news = "EXPOSED: Government hiding aliens in underground base, leaked documents reveal shocking truth!"

#result = classifier(sample_text)
#print(result)

#print("Real news sample:")
#print(classifier(real_news))

#print("\nFake news sample:")
#print(classifier(fake_news))

samples = [
    "The president signed the infrastructure bill into law on Tuesday after months of negotiation.",
    "exposed exposed exposed exposed exposed miracle exposed exposed doctors exposed exposed hate her exposed",
    "Local hospital opens new emergency wing after three years of construction.",
    "You won't satisfactory what happened next! Scientists exposed the truth about vaccines exposed the government doesn't want exposed you to know.",
]

for text in samples:
    result = classifier(text)
    print(f"Text: {text[:70]}...")
    print(f"Result: {result}\n")



