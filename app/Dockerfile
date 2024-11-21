FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Define the command to run your application
CMD ["python", "spending_analysis.py"]