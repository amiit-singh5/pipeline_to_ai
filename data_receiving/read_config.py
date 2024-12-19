import json
import logging
import os

# Function to load configuration from config.json
def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        print(f"Error: The file {config_path} does not exist.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return None

# way of calling
config_path = 'config.json'
config = load_config(config_path)


def get_active_env(config):
    for env_name, env_settings in config.items():
        # Check if any execution mode has "status": true
        active_modes = {mode_name: mode_config for mode_name, mode_config in
                        env_settings.get("execution_mode", {}).items() if mode_config.get("status", True)}

        if active_modes:
            # print("1. active_modes : ", active_modes)
            # print(f"Environment: {env_name}")

            logging_config = env_settings.get("logging", {})

            return env_name,active_modes,env_settings.get("data_sources", []), logging_config

env_name, active_execution_modes, Data_Sources, logging_config = get_active_env(config)

print("env_name : ",env_name)
print("active_execution modes : ", active_execution_modes)
print("Data_Sources : ",Data_Sources)
print("logging_config : ", logging_config)

def validate_execution_mode_status(config):
    try:
        # Iterate over each environment to validate "status"
        for env_name, env_settings in config.items():
            #print("env_settings " , env_settings)
            execution_modes = env_settings.get("execution_mode", {})

            # Count how many modes have "status": true
            active_modes = [mode for mode, settings in execution_modes.items() if settings.get("status")]
            print("active_modes : ", active_modes)
            # Validate that only one mode is active at a time
            if len(active_modes) == 1:
                logging.info(f"Environment '{env_name}' is valid with active mode: {active_modes[0]}")
            elif len(active_modes) > 1:
                logging.error(
                    f"Environment '{env_name}' has multiple active modes: {active_modes}. Only one mode should be active.")
            else:
                logging.info(f"Environment '{env_name}' has no active execution mode.")

    except Exception as e:
        logging.error(f"Failed to validate execution modes: {e}")

validate_execution_mode_status(config)