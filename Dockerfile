FROM python:3.6
ENV AM_I_IN_A_DOCKER_CONTAINER Yes
COPY /markcaptcha /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "markcaptcha.py"]
