import llm_party
import md_jinja
import argparse
import yaml
from llm_eval.service import load_instructions, compile_party_config, conduct_chat_session

def run_exp(init_instr_dir, party_conf, exp_conf, output_dir, verbose):
    # Load initial instructions
    init_instr = load_instructions(init_instr_dir)

    # Compile the configuration for llm_party library
    party_conf_dict = compile_party_config(party_conf, init_instr)

    # Load the test configuration
    with open(exp_conf, 'r') as file:
        exp_conf_dict = yaml.safe_load(file)

    # Conduct the chat session based on the test configuration
    conduct_chat_session(party_conf_dict, exp_conf_dict, output_dir, verbose)

def main():
    """
    Main function to conduct a chat session between two AI agents.

    This function parses command-line arguments, loads initial instructions,
    compiles the party configuration, loads the test configuration, and
    conducts the chat session based on the test configuration.

    Command-line arguments:
        --party-conf, -p: Configuration file for llm_party library (required).
        --exp-conf, -t: Configuration file for the test (required).
        --init-instr-dir, -i: Directory containing initial instructions for AI agents (required).
        --verbose, -v: Enable verbose mode (optional).
        --output-dir, -o: Directory to save output files (optional, default: current directory).
    """
    parser = argparse.ArgumentParser(description='Conduct a chat session between two AI agents.')
    parser.add_argument('--party-conf', '-p', type=str, required=True, help='Configuration file for llm_party library')
    parser.add_argument('--exp-conf', '-t', type=str, required=True, help='Configuration file for the test')
    parser.add_argument('--init-instr-dir', '-i', type=str, required=True, help='Directory containing initial instructions for AI agents')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose mode')
    parser.add_argument('--output-dir', '-o', type=str, default='.', help='Directory to save output files')

    args = parser.parse_args()
    run_exp(args.init_instr_dir, args.party_conf, args.exp_conf, args.output_dir, args.verbose)