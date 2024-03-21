import yaml
from llm_eval.service import compile_party_config, conduct_chat_session, make_init_instr_lists
from typing import Dict, Any


def run_exp_suite(exp_suite: Dict[str, Any], verbose: bool, output_dir: str):
    """
    Conduct an experiment suite by running chat sessions for all combinations of initial instructions.

    Args:
        exp_suite (Dict[str, Any]): Configuration for the experiment suite, including initial instruction directories,
                                    party configuration file path, and experiment configuration file path.
        verbose (bool): Flag to enable verbose mode for detailed logging.
        output_dir (str): Directory to save the output files of the chat sessions.

    Raises:
        ValueError: If the required keys are missing in the exp_suite configuration.
    """
    # Validate required keys in exp_suite
    required_keys = ["init instr dirs", "party conf", "exp conf"]
    if not all(key in exp_suite for key in required_keys):
        raise ValueError(f"Experiment suite configuration is missing required keys: {', '.join(required_keys)}")

    init_instr_dirs = exp_suite["init instr dirs"]
    party_conf = exp_suite["party conf"]
    exp_conf = exp_suite["exp conf"]

    # Generate all combinations of initial instruction files
    init_instr_lists = make_init_instr_lists(init_instr_dirs)

    for init_instr_list in init_instr_lists:
        # Conduct the chat session for each combination of initial instructions
        run_exp_with_single_party_conf(init_instr_list, party_conf, exp_conf, output_dir, verbose)

def run_exp_with_single_party_conf(init_instr_list, party_conf, exp_conf, output_dir, verbose):
    """
    Party configuration must contain exactly the same number of the attendees as the length of init_instr_list.
    Typically, the first attendee plays the AI agent role and the second plays the human client role.
    """
    party_conf_dict = compile_party_config(party_conf, init_instr_list)

    # Load the test configuration
    with open(exp_conf, 'r') as file:
        exp_conf_dict = yaml.safe_load(file)

    # Conduct the chat session based on the test configuration
    conduct_chat_session(party_conf_dict, exp_conf_dict, output_dir, verbose)
