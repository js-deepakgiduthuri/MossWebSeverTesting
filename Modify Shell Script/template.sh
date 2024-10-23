#!/bin/bash

# Dictionary mapping SIM card operator names to APNs
declare -A sim_apn_dict=(
    #PLACEHERE
    #enddict
)

# Function to detect modem and extract operator name
detect_modem() {
    modem_list=$(mmcli -L)

    if [[ "$modem_list" == *"No modems were found"* ]]; then
        echo "No modem detected."
        return 1
    else
        modem_info=$(mmcli -m 0)
        operator=$(echo "$modem_info" | grep "operator name" | awk -F': ' '{print $2}')
        primary_port="ttyUSB2"  # Hardcoded for simplicity
        echo "Modem detected. Operator: $operator"
        return 0
    fi
}

# Function to create a new network using nmcli
create_nmcli_connection() {
    operator=$1
    port=$2

    apn="${sim_apn_dict[$operator]}"

    if [[ -n "$apn" ]]; then
        connection_name="home"

        # Check if the connection already exists
        existing_connection=$(nmcli c show "$connection_name" 2>/dev/null)
        if [[ -n "$existing_connection" ]]; then
            echo "Connection '$connection_name' already exists. No new connection created."
            return
        fi

        echo "Creating network connection for operator $operator with APN $apn..."
        nmcli c add type gsm ifname "$port" con-name "$connection_name" apn "$apn"
    else
        echo "APN for operator $operator not found in the dictionary."
    fi
}

# Main logic to detect modem and create a network connection
while true; do
    detect_modem
    if [ $? -eq 0 ]; then
        create_nmcli_connection "$operator" "$primary_port"
    fi

    # Check every 5 seconds
    sleep 5
done
