FROM python:3.14-alpine

WORKDIR app/
COPY . .
RUN pip install  -r req.txt
CMD ["uvicorn", "apps.views.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]