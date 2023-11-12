# Use Python 3.11.4
FROM baseimage_secretstore

# Set the working directory in the container
RUN mkdir /secretstore
WORKDIR /secretstore
COPY ./secretstore .
RUN chmod +x entrypoint_app.sh
RUN chmod +x entrypoint_worker.sh

ENTRYPOINT ["./entrypoint_worker.sh"]