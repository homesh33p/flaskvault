#!/bin/bash

echo "Vault is already initialized, but is sealed"

#!/bin/bash

# Check if the .env file exists
if [ -f /vault/config/vault.env ]; then
  # Load environment variables from .env file
  export $(cat /vault/config/vault.env | xargs)

  # Optionally, print loaded variables
  echo "Environment variables loaded from .env file:"
else
  echo ".env not found"
  exit 1
fi

for ((i=1; i<=5; i++)); do
  var_name="UNSEAL_KEY_$i"
  if [ -z "${!var_name}" ]; then
    echo "$var_name is not set."
  else      
    vault_sealed=$(vault status -format=json 2>/dev/null | jq -r '.sealed')
    
    if [ "$vault_sealed" = "true" ]; then
      echo "Unsealing with $var_name"    
    
      echo "Unsealing with $var_name"
      vault operator unseal "${!var_name}"
    else
      echo "Vault is unsealed."
      break        
    fi    
  fi
done

vault_sealed=$(vault status -format=json 2>/dev/null | jq -r '.sealed')

if [ "$vault_sealed" = "true" ]; then
  echo "Unsealing failed, exiting"
  exit 1
fi

if [ -n "$VAULT_TOKEN" ]; then
    vault login "$VAULT_TOKEN"
    echo "Successfully authenticated."
fi 

