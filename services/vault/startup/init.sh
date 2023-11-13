#!/bin/bash

# Maximum number of retries
MAX_RETRIES=5

# Delay between retries in seconds
DELAY=1

# Function to check and retry vault status
waitforserver() {
    local retries=0
    local status=1

    while [ "$retries" -lt "$MAX_RETRIES" ] && [ "$status" -ne 0 ] && [ "$status" -ne 2 ]; do
        # Run vault status and capture the exit status
        echo "Checking vault status..."
        vault status > /dev/null 2>&1
        status=$?
        
        if [ "$retries" -gt "$MAX_RETRIES" ] && [ "$status" -ne 0 ] && [ "$status" -ne 2 ]; then
            echo "Max retries reached. Vault server still not up."
            exit 1
        fi

        sleep "$DELAY"
        ((retries++))

    done
}

# Call the function to check and retry
waitforserver

echo "Vault server up"
# Check if Vault is not initialized
vault_initialized=$(vault status -format=json 2>/dev/null | jq -r '.initialized')

vault_sealed=$(vault status -format=json 2>/dev/null | jq -r '.sealed')

if [ "$vault_initialized" != "true" ]; then
    ./startup/vault_init.sh

    vault_initialized=$(vault status -format=json 2>/dev/null | jq -r '.initialized')
    
    if [ "$vault_initialized" == "true" ]; then
        echo "Vault initialized"
    else
        echo "Vault initialisation failed"
        exit 1
    fi
else
    if [ "$vault_sealed" == "true" ]; then
        ./startup/unseal.sh
        
        vault_sealed=$(vault status -format=json 2>/dev/null | jq -r '.sealed')    
        
        if [ "$vault_sealed" == "false" ]; then
            echo "Vault unsealed"
        else
            echo "Vault unsealing failed"
            exit 1
        fi   
    else
        echo "Vault is already unsealed"
    fi
fi