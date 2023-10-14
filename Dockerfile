FROM python:3.11.3

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
# CMD ["flet", "run", "main.py", "-vv", "-w", "-p", "45000"]