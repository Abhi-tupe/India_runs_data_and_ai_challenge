# Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container first (to leverage Docker caching)
COPY requirements.txt .

# Install all production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the ports for both Streamlit (8501) and FastAPI (8000)
EXPOSE 8501 8000

# Provide a default instruction (this runs the unit tests first to guarantee integrity, then runs the ranker)
CMD python -m unittest test_pipeline.py && python rank.py