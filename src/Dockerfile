FROM python:bullseye

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install openai
RUN pip install pyqt5

COPY . .

CMD ["python", "chatbot.py"]