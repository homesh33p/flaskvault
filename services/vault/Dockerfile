# base image
FROM alpine:3.14

# set vault version
ENV VAULT_VERSION 1.8.2

# create a new directory
RUN mkdir /vault
RUN mkdir /startup

COPY ./startup /startup

RUN chmod +x /startup

# download dependencies
RUN apk --no-cache add \
      bash \
      ca-certificates \
      wget \
      jq \
      supervisor

# download and set up vault
RUN wget --quiet --output-document=/tmp/vault.zip https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip && \
    unzip /tmp/vault.zip -d /vault && \
    rm -f /tmp/vault.zip && \
    chmod +x /vault

# update PATH
ENV PATH="PATH=$PATH:$PWD/vault"

# add the config file
COPY ./config/vault-config.json /vault/config/vault-config.json

# COPY ./vault_unseal.sh /vault/vault_unseal.sh
# RUN chmod +x /vault/vault_unseal.sh
# RUN ln -s /vault/vault_unseal.sh /usr/local/bin/unseal

# expose port 8200
EXPOSE 8200

# ENTRYPOINT [ "./startup/init.sh" ]
COPY ./config/supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]