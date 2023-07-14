FROM python:3.8-slim

# copy file
COPY . /
COPY run.sh /

# Install requirements for add-on
RUN pip install -r requirements.txt
# RUN /bin/bash -c "source /venv/Scripts/activate"

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]