FROM python:3

LABEL maintainer="stirfliedlice"

RUN apt-get update && apt-get install -y ipmitool

WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]
CMD [ "./test_script.py" ]
