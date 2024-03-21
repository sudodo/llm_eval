import argparse
import yaml
from typing import List, Dict
from llm_eval.controller import run_exp_suite

def load_exp_suites_conf(exp_suites_conf_path: str) -> List[Dict]:
    """
    Load the experiment suites configuration from a YAML file.

    Args:
        exp_suites_conf_path (str): Path to the YAML file containing the experiment suites configuration.

    Returns:
        List[Dict]: A list of dictionaries, each representing the configuration for an experiment suite.
    """
    with open(exp_suites_conf_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    """
    Main function to run experiment suites for evaluating chat sessions between two AI agents.

    This script parses command-line arguments to receive the configuration file for experiment suites,
    a flag to enable verbose mode, and the output directory to save the results. It then loads the
    experiment suites configuration and conducts each experiment suite as specified.
    """
    parser = argparse.ArgumentParser(description='Run experiment suites for evaluating chat sessions between two AI agents.')
    parser.add_argument('--exp-suites-conf', '-c', type=str, required=True, help='Configuration file for the experiment suites')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose mode')
    parser.add_argument('--output-dir', '-o', type=str, required=True, help='Directory to save output files')

    args = parser.parse_args()

    # Load the configuration file for the experiment suites
    exp_suite_conf_list = load_exp_suites_conf(args.exp_suites_conf)

    # Conduct each experiment suite
    for exp_suite in exp_suite_conf_list:
        run_exp_suite(exp_suite, args.verbose, args.output_dir)

if __name__ == '__main__':
    main()