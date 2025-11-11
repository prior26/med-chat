#!/bin/bash
INIT_FILE="init.json"

# Check if the file exists
if [ ! -f "$INIT_FILE" ]; then
    echo "Error: $INIT_FILE not found!"
    exit 1
fi

# Use jq to extract the hf-token value
if ! command -v jq &> /dev/null; then
    echo "Error: 'jq' is required to parse JSON. Please install it."
    exit 1
fi

HF_TOKEN=$(jq -r '.["hf-token"]' "$INIT_FILE")
MODEL=$(jq -r '.["model"]' "$INIT_FILE")

# Check if token was extracted successfully
if [ "$HF_TOKEN" == "null" ] || [ -z "$HF_TOKEN" ]; then
    echo "Error: Could not extract 'hf-token' from $INIT_FILE"
    exit 1
fi
# Check if token was extracted successfully
if [ "$MODEL" == "null" ] || [ -z "$MODEL" ]; then
    echo "Error: Could not extract 'model' from $INIT_FILE"
    exit 1
fi

# Export as environment variable
export HF_TOKEN
echo "HF_TOKEN loaded successfully."

# Load and run the model:
vllm serve "$MODEL"