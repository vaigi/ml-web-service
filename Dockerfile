FROM python:3
COPY .  /root
WORKDIR /root
RUN pip install flask gunicorn numpy scikit-learn scipy flask_wtf pandas