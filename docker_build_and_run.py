import os


POSTGRES_USER = input("Enter the PostgreSQL username: ")
POSTGRES_PASSWORD = input("Enter the PostgreSQL password: ")
POSTGRES_DB = input("Enter the PostgreSQL database name: ")


os.system("docker build --tag etl_image .")


os.system(f"docker run --publish 5000:5000 --env POSTGRES_USER={POSTGRES_USER} --env POSTGRES_PASSWORD={POSTGRES_PASSWORD} --env POSTGRES_DB={POSTGRES_DB} etl_image")
