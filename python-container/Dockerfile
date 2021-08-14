FROM python:3

LABEL maintainer="stirfliedlice"

RUN apt-get update && apt-get install -y ipmitool

WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENTRYPOINT [ "sh", "-c", "export IDRACPASSWORD=`cat /var/run/secrets/idrac_password` ; python3 test_script.py ${IDRACIP} ${IDRACUSER} ${IDRACPASSWORD}" ]

# ENTRYPOINT [ "sh", "./entrypoint.sh" ]
# CMD [ "python3", "./test_script.py" ]

ENTRYPOINT [ "python3" ]
CMD [ "./test_script.py" ]
