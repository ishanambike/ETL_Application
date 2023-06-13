import subprocess

# Prompt for username and database name
username = input("Enter the PostgreSQL username: ")
database_name = input("Enter the PostgreSQL database name: ")


# Define the PostgreSQL commands
commands = [
    f'psql -U {username} -W -d {database_name} -c "select * from users;"'
]

# Execute the commands
for command in commands:
    subprocess.run(command, shell=True)
