from flask import Flask, render_template, request
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# Initialize the Flask app
app = Flask(__name__)

# Function to predict sentiment from text input
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=-1).item()
    
    sentiment_labels = ["negative", "neutral", "positive"]
    return sentiment_labels[predicted_class]

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment = ""
    text = ""  # Store the user's input text here
    if request.method == 'POST':
        text = request.form['text']  # Capture the text input
        sentiment = predict_sentiment(text)  # Get the sentiment prediction
    return render_template('index.html', sentiment=sentiment, text=text)  # Pass both text and sentiment to the template

# Main block to initialize everything
if __name__ == '__main__':
    # Load the tokenizer and model inside the main guard
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = RobertaTokenizer.from_pretrained(model_name)
    model = RobertaForSequenceClassification.from_pretrained(model_name)

    # Start Flask app
    app.run(debug=True)
