#-alpine，-slim 简易版包不匹配，所以用python3.7
FROM python:3.7
ADD . /api
WORKDIR /api
# Install any needed packages specified in requirements.txt，-i https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
# Make port 7001 available to the world outside this container
EXPOSE 7001
# Run app.py when the container launches
CMD ["python", "/api/app/main.py"]


