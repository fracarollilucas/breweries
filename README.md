# breweries
This repository is the result of my attempt at a Data Engineering pipeline architecture that consumes data from an API, transforms it and persists it to a data lake.

# Preamble
This tutorial assumes you have Docker and Airflow and have basic familiarity with them, as well as with git. Furthermore, this `README` file is merely an instruction manual on how to run the code. For design considerations I have made and other aspects of documenting the process, refer to `DESIGNPROCESS.md`. 

# How to run 
1. Clone this repository into your `dags/` folder, or wherever you run your DAGs.
2. `cd` into the `breweries/` folder and run `pip install -r requirements.txt`
3. Make sure you have Airflow running. For most Windows users, this means entering the directory where you have your `docker-compose.yaml` and running `docker-compose up airflow-init` on the Command Prompt, but you can [read the documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) for mor details.
4. Enter Airflow (usually, this means typing `localhost:8080` on your browser and hitting `Enter`). If you're asked to provide credentials, they most likely are `airflow` both for the username and the password.
5. Upon landing on the home page, you should see a list of DAG names, among which you should find `breweries_pipeline`. Click on it.

![image](https://github.com/user-attachments/assets/c26b37f5-9e35-492c-bc4d-db940b9f6ecf)



5. Unpause the DAG by toggling the button on the upper-left corner and trigger it by clicking on the play button on the upper-right corner.

![image](https://github.com/user-attachments/assets/a2548503-7130-433d-87ef-7f90dadcac39)


6. The DAG should now start running. You can follow the progression of each task by clicking on `Graph`.

![image](https://github.com/user-attachments/assets/76936410-fe32-48b6-9e3c-75d05fb14e70)


7. When the DAG finishes running and you wish to see the files saved, you can open `Docker Desktop`, select `Containers`, then `airflow` and select the Airflow worker. In the `Files` tab, the data will be stored inside `/opt/airflow/data`. The folder structure should follow the Medallion architecture. You can import the `data` directory to your computer by right-clicking on it and selecting `Save`. Alternatively, you can mount a volume inside your `docker-compose.yaml` file by adding the following lines to your `airflow-worker` tag. Just make sure to indent them correctly. This will create a mapping between the `data` folder in your host machine and the container, so that the files that are saved inside the container can be visible to your computer.

```
volumes:
  - ./dags/breweries/data:/opt/airflow/data
```

   

![image](https://github.com/user-attachments/assets/fb6edd80-9c0d-4630-8098-1897d735bc95) ![image](https://github.com/user-attachments/assets/63c56796-aa3f-4185-b4d8-c9f7dece1c7d)
