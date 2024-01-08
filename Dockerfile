FROM python@latest

ADD requirements.txt /requirements.txt
ADD main.py /main.py
RUN pip install -r requirements.txt

CMD ["python", "/main.py"]
