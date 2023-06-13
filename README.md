# ETL_Application

# Initial steps:
* Download and install Python 3 from https://www.python.org/downloads/. Please skip this step if Python 3 is already installed.
* Download and install PostgreSQL from https://www.postgresql.org/download/. Please skip this step if PostgreSQL is already installed.
* Download and install Docker from https://www.docker.com/products/docker-desktop/. Please skip this step if Docker is already installed.
* Download all the project files to the system.
* Start the docker engine.

# Running the application manually:
* Open a command prompt in the project directory or set the working directory of the command prompt to the project directory.
* Build the Docker image using the command: “docker build --tag etl_image .”
* Run the Docker image in a container using the command: “docker run --publish 5000:5000 --env POSTGRES_USER={username} --env POSTGRES_PASSWORD={password} --env POSTGRES_DB={database_name} etl_image”. Please replace values for username, password, and database name. The values should be case-sensitive. Provide the values without enclosing them in quotes.
* Run the ETL process. You can use the command “curl http://localhost:5000/” in a different command prompt or load http://localhost:5000/ in a browser.
* You should see the message “{"message":"ETL process started"}”
* Now in a different command prompt log into PostgreSQL using the command: “psql -U {username} -W -d {database_name}”. Please provide your username and database name same as the one provided previously. The system will prompt for a password.
* Now query the database to view the table created by the ETL process using the query: “select * from users;”
* Now you should see the final table with users' data and derived features.

# Running the application using scripts:
* Open a command prompt in the project directory or set the working directory of the command prompt to the project directory.
* Execute the command "python docker_build_and_run.py".
* Open a command prompt in the project directory and execute "python run_ETL.py".
* Execute the command "python run_postgresql_commands.py". Please provide the same credentials and database name provided in second step.
* Now you should see the final table with users' data and derived features.
