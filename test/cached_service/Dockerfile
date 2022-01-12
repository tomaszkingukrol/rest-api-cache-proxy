FROM python
WORKDIR /usr/app
COPY . .
RUN pip install -r requirements.txt
CMD ["python",  "cached_service.py"]