# Start with an Airflow base image
FROM apache/airflow:2.10.2-python3.9

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Copy your DAGs and scripts into the image
COPY dags/ $AIRFLOW_HOME/dags/
WORKDIR $AIRFLOW_HOME/dags/
RUN mkdir logs
RUN mkdir config

# Install any additional requirements
COPY requirements.txt .
COPY docker-compose.yaml . 
RUN pip install -r requirements.txt

# Initialize the Airflow database
RUN airflow db init

# Set the entrypoint to start the Airflow scheduler and webserver
ENTRYPOINT ["airflow", "scheduler"]