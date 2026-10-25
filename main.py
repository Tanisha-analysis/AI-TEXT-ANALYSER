import gradio as gr
from transformers import pipeline

# Load pretrained Hugging Face models (downloaded automatically on first run)
sentiment = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
qa = pipeline("question-answering")


def analyze_sentiment(text):
    r = sentiment(text[:2000])[0]
    return f"{r['label']} (confidence: {r['score']:.2f})"


def summarize_text(text):
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]


def answer_question(text, question):
    return qa(question=question, context=text)["answer"]


with gr.Blocks() as app:
    gr.Markdown("# AI Text Analyzer")
    text = gr.Textbox(lines=8, label="Paste your text here")

    with gr.Tab("Sentiment"):
        out1 = gr.Textbox(label="Result")
        gr.Button("Analyze").click(analyze_sentiment, text, out1)

    with gr.Tab("Summarize"):
        out2 = gr.Textbox(label="Summary")
        gr.Button("Summarize").click(summarize_text, text, out2)

    with gr.Tab("Ask a Question"):
        q = gr.Textbox(label="Your question")
        out3 = gr.Textbox(label="Answer")
        gr.Button("Get Answer").click(answer_question, [text, q], out3)

if __name__ == "__main__":
    app.launch()