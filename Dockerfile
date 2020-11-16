# Base image for docker
FROM python:3.7.6

WORKDIR /submission

# copying submission files over
COPY common.py .
COPY test_common.py .
COPY sample_input.json .
COPY sample_output.json .

# Runing unit tests
RUN python test_common.py

RUN pip install pyInstaller
RUN pyinstaller -F common.py 

RUN mv /submission/dist/common ./sde-test-solution



# ENTRYPOINT [ "/submission/sde-test-solution" ]
# ENTRYPOINT [ "/bin/bash" ]