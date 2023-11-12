#!/bin/bash

echo "Vault is already initialized, but is sealed"

# Check if UNSEAL_KEY variables are set
if [ -z "$UNSEAL_KEY_1" ] || [ -z "$UNSEAL_KEY_2" ] || [ -z "$UNSEAL_KEY_3" ]; then
  echo "UNSEAL_KEY variables are not set."
else
  # Unseal Vault using the provided keys
  echo "Unsealing Vault..."

  # Unseal with the first key
  vault operator unseal "$UNSEAL_KEY_1" "$VAULT_ADDR" > /dev/null 2>&1

  # Unseal with the second key
  vault operator unseal "$UNSEAL_KEY_2" "$VAULT_ADDR" > /dev/null 2>&1

  # Unseal with the third key
  vault operator unseal "$UNSEAL_KEY_3" "$VAULT_ADDR" > /dev/null 2>&1

  echo "Vault successfully unsealed."
  if [ -n "$VAULT_TOKEN" ]; then
      vault login "$VAULT_TOKEN" > /dev/null 2>&1
      echo "Successfully authenticated."
  fi    
    
fi

