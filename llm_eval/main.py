import llm_party
import md_jinja

import argparse
import os
import json
import yaml
from typing import List, Dict
from llm_party import initiate_session as start_session


def load_instructions(init_instr_dir: str) -> List[str]:
    """
    Load initial instructions for AI agents from the specified directory in alphabetical order.

    Args:
        init_instr_dir (str): Directory containing initial instruction files.

    Returns:
        List[str]: List of initial instructions sorted alphabetically by file name.
    """
    instructions = []
    file_names = sorted(os.listdir(init_instr_dir))  # Sort file names alphabetically
    for file_name in file_names:
        file_path = os.path.join(init_instr_dir, file_name)
        with open(file_path, 'r') as file:
            instructions.append(file.read())
    return instructions

def compile_party_config(party_conf: str, init_instr: List[str]) -> Dict:
    """
    Compile the configuration for the llm_party library by merging initial instructions.

    Args:
        party_conf (str): Path to the party configuration file.
        init_instr (List[str]): List of initial instructions for AI agents.

    Returns:
        Dict: Compiled party configuration dictionary.
    """
    with open(party_conf, 'r') as file:
        party_conf_dict = yaml.safe_load(file)

    for i, instr in enumerate(init_instr):
        party_conf_dict['attendees'][i]['instruction']['text'] = instr

    return party_conf_dict

import datetime  # Add this import at the beginning of your file

def conduct_chat_session(party_conf_dict: Dict, test_conf: Dict, output_dir: str, verbose: bool):
    """
    Conduct a chat session based on the party configuration and test configuration, saving the session and configuration to files.

    This function initiates a chat session using the provided party configuration and test configuration. It generates a unique timestamp to append to the filenames of the saved chat session and party configuration, ensuring each session's output is uniquely identifiable. The chat session is conducted for a number of rounds specified in the test configuration.

    Args:
        party_conf_dict (Dict): Compiled party configuration dictionary. This dictionary should include the configuration for each attendee of the chat session, such as their roles, initial instructions, and any other relevant settings.
        test_conf (Dict): Test configuration dictionary. This dictionary specifies the parameters for the chat session. Key parameters include:
            - 'num_rounds' (int): The number of chat rounds to be conducted. If not specified, defaults to 3.
            - Other parameters can be included based on the requirements of the `llm_party` library or specific test scenarios.
        output_dir (str): Directory to save output files. This includes the chat session history and the party configuration, both appended with a timestamp for uniqueness.
        verbose (bool): Enable verbose mode. If True, additional details about the chat session will be printed to the console.

    The function saves two files in the specified output directory:
        - A JSON file containing the chat history, named `chat_history_YYYYMMDD_HHMMSS.json`, where `YYYYMMDD_HHMMSS` is the timestamp at the start of the session.
        - A YAML file containing the compiled party configuration, named `party_conf_YYYYMMDD_HHMMSS.yaml`, with the same timestamp.

    The timestamp format is YYYYMMDD_HHMMSS, representing the year, month, day, hour, minute, and second at the start of the chat session.
    """
    # Define file paths with timestamp
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    filepath_of_chat_session = os.path.join(output_dir, f'chat_history_{timestamp}.json')
    file_path_of_party_conf_dict = os.path.join(output_dir, f'party_conf_{timestamp}.yaml')

    # Start the chat session
    num_rounds = test_conf.get('num_rounds', 3)
    for _ in range(num_rounds):
        chat_session, _ = start_session(party_conf_dict, output=print if verbose else None)

        # Save the chat history with timestamp in filename
        with open(filepath_of_chat_session, 'w') as file:
            json.dump(chat_session.to_dict(), file, indent=2)

        # TODO: Dump chat history as readable text in a separate file

        # Save the compiled configuration for llm_party library with timestamp in filename
        with open(file_path_of_party_conf_dict, 'w') as file:
            yaml.dump(party_conf_dict, file)

def main():
    """
    Main function to conduct a chat session between two AI agents.

    This function parses command-line arguments, loads initial instructions,
    compiles the party configuration, loads the test configuration, and
    conducts the chat session based on the test configuration.

    Command-line arguments:
        --party-conf, -p: Configuration file for llm_party library (required).
        --test-conf, -t: Configuration file for the test (required).
        --init-instr-dir, -i: Directory containing initial instructions for AI agents (required).
        --verbose, -v: Enable verbose mode (optional).
        --output-dir, -o: Directory to save output files (optional, default: current directory).
    """
    parser = argparse.ArgumentParser(description='Conduct a chat session between two AI agents.')
    parser.add_argument('--party-conf', '-p', type=str, required=True, help='Configuration file for llm_party library')
    parser.add_argument('--test-conf', '-t', type=str, required=True, help='Configuration file for the test')
    parser.add_argument('--init-instr-dir', '-i', type=str, required=True, help='Directory containing initial instructions for AI agents')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose mode')
    parser.add_argument('--output-dir', '-o', type=str, default='.', help='Directory to save output files')

    args = parser.parse_args()

    # Load initial instructions
    init_instr = load_instructions(args.init_instr_dir)

    # Compile the configuration for llm_party library
    party_conf_dict = compile_party_config(args.party_conf, init_instr)

    # Load the test configuration
    with open(args.test_conf, 'r') as file:
        test_conf = yaml.safe_load(file)

    # Conduct the chat session based on the test configuration
    conduct_chat_session(party_conf_dict, test_conf, args.output_dir, args.verbose)

