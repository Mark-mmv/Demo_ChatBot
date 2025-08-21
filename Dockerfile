FROM python:bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libgl1-mesa-dri \
    libglib2.0-0 \
    libx11-6 \
    libx11-xcb1 \
    libxrender1 \
    libxi6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libxtst6 \
    libnss3 \
    libxss1 \
    libasound2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libxcb1 \
    libxcb-glx0 \
    libxcb-keysyms1 \
    libxcb-image0 \
    libxcb-shm0 \
    libxcb-icccm4 \
    libxcb-randr0 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-sync1 \
    fonts-dejavu \
    xauth \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install openai
RUN pip install pyqt5

COPY . .

ENV QT_DEBUG_PLUGINS=1

CMD ["python", "src/chatbot.py"]