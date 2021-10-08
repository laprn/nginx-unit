FROM nginx/unit:1.25.0-python3.9

WORKDIR  /usr/local/nginx/app

COPY config.json /docker-entrypoint.d/

COPY wsgi.py /usr/local/nginx/app/
COPY requirements.txt /usr/local/nginx/app

# python3.9 install
RUN apt update
RUN apt -y upgrade
RUN apt install -y python3.9
RUN apt install -y python3-pip

# create venv
RUN python -m venv venv
RUN . venv/bin/activate

# pip istall
RUN pip install -r requirements.txt
RUN python dbinit.py