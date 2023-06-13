# ETL_Application
* Download and install Python 3 from https://www.python.org/downloads/. Please skip this step if Python 3 is already installed.
* Download and install PostgreSQL from https://www.postgresql.org/download/. Please skip this step if PostgreSQL is already installed.
* Download and install Docker from https://www.docker.com/products/docker-desktop/. Please skip this step if Docker is already installed.
* Download all the project files to the system.
* Start the docker engine.
* Open a command prompt in the project directory or set the working directory of the command prompt to the project directory.
* Build the Docker image using the command: “docker build --tag etl_image .”
* Run the Docker image in a container using the command: “docker run --publish 5000:5000 --env POSTGRES_USER=username --env POSTGRES_PASSWORD=password --env POSTGRES_DB=database etl_image”. Please replace values for username, password, and database name. The values should be case-sensitive. Provide the values without enclosing them in quotes.
* Run the ETL process. You can use the command “curl http://localhost:5000/” in a different command prompt or load http://localhost:5000/ in a browser.
* You should see the message “{"message":"ETL process started"}”
* Now in a command prompt log into PostgreSQL using the command: “psql -U username”. Please provide your username same as the one provided previously.
* Now connect to the database using the command “\c database_name”. Please provide the database name same as the one provided previously.
* Now query the database to view the table created by the ETL process using the query: “select * from users;”
* Now you should see the final table with users' data and derived features.
