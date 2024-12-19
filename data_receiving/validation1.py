import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_execution_mode_status(config_file="config.json"):
    try:
        # Load configuration
        with open(config_file, "r") as file:
            config = json.load(file)

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


# Run the function
validate_execution_mode_status()
