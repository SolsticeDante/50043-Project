# Use an official Python runtime as an image
FROM python:3.7

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000
EXPOSE 43074
EXPOSE 27017

WORKDIR /app/backend

# Install any needed packages specified in requirements.txt
COPY installation_files/requirements.txt /app/backend
RUN pip install -r requirements.txt
RUN pip install PyMySQL[rsa]

COPY backend /app/backend
COPY data_analytics /app/data_analytics
COPY installation_files /app/installation_files



ADD ./sql-dump/amazon.sql /docker-entrypoint-initdb.d

# CMD mysql -u user -ppassword -e "SET autocommit=0;" AMAZON < amazon.sql
WORKDIR /app
#CMD ["/usr/bin/mongod", "-f", "/etc/mongod.conf"]
ADD ./mongo-seed/ /app/mongo-seed/
#CMD python ./mongo-seed/mongo-populate.py
#RUN /app/mongo-seed/import.sh
#ENTRYPOINT mongo

WORKDIR /app/backend/reviews

CMD export FLASK_APP=reviews