
## Q

I want to create a python script with the following requirements.

### Functionality

- Users evaluate if two AI agents conduct high-quality chat session. To this end, this script conducts a chat session between two AI agents and provides the users with the chat history.
  - To conduct the chat session between two AI agents, it uses `llm_party` library that is a third party library for creating a chat session between two AI agents.
- There are three types of configuration files:
  1. The configuration for `llm_party` library
  2. The initial instructions for the AI agents
  3. The configuration file for the test (e.g., the number of iterations of chat sessions)
- These configuration files are specified by the user as command-line arguments.
- Before executing the chat session, the configuration 1 and 2 are compiled into a single configuration file for `llm_party` library.
- The output of this script is as follows:
  1. The test result including the chat history between two AI agents.
  2. The compiled configuration file for `llm_party` library

### Parameters

It receives parameters as follows:

- `--party-conf` (or `-p`): the configuration file for `llm_party` library (required)
- `--exp-conf` (or `-t`): the configuration file for the test (required)
- `--init-instr-dir` (or `-i`): the directory that contains the initial instructions for the AI agents (required)
- `--verbose` (or `-v`): a flag to enable verbose mode
- `--output-dir` (or `-o`): the directory to save the output files (optional)

### Pseudo code

In my understanding, the pseudo code for this script is as follows:

```python
# Import the required libraries
from llm_party import start_session_controller as start_session
...

# Parse the command-line arguments
party_conf, exp_conf, init_instr_dir, verbose = ...

# Compile to the configuration for llm_party library
## Load the initial instructions
init_instr = [file.load() for file in init_instr_dir]
## Load the configuration for llm_party library
party_conf_dict = yaml.load(party_conf)
## Compile the configuration for llm_party library
for file, index in init_instr_dir:
    party_conf_dict["agent"][0]["init_instr"] = init_instr[index]

chat_session, _ = start_session(...)
json.dump(chat_session, os.path.join(output_dir, "chat_history.json"))
yaml.dump(party_conf_dict, os.path.join(output_dir, "party_conf.yaml"))

```

Note that the above pseudo code is just a rough sketch and may not be correct. We might need some additional processes such as the error handling.

### The attached files

- session_controller.py: the controller functions of `llm_party` library
- valid_config.yaml: an example of the configuration file for `llm_party` library. The value of `attendees.[0].instruction.text` is the initial instruction for the first AI agent. In our script this field is replaced by the content of the file in `--init-instr-dir` directory.

## Q

I want to create a python script with the following requirements.

### Functionality

- Users evaluate if two AI agents conduct high-quality chat session. To this end, this script conducts a chat session between two AI agents and provides the users with the chat history.
  - To conduct the chat session between two AI agents, it uses `llm_party` library that is a third party library for creating a chat session between two AI agents.
- There are three types of configuration files:
  1. The configuration for `llm_party` library
  2. The initial instructions for the AI agents
  3. The configuration file for the test (e.g., the number of iterations of chat sessions)
- These configuration files are specified by the user as command-line arguments.
- Before executing the chat session, the configuration 1 and 2 are compiled into a single configuration file for `llm_party` library.
  - The file paths of the initial instructions are specified in the `llm_party` configuration files as follows:

    ```yaml
    # party_conf_sample.yaml
    ...
    text: {{{ /path/to/initial/instruction1.md }}}
    ```

  - The `run` method in `md_jinja` library compiles the configuration files by loading the initial instructions specified by "{{{ ... }}}" and replacing them with the content of the file.
    - So, the initial instruction files are not required to be specified as command-line arguments.

- The output of this script is as follows:
  1. The test result including the chat history between two AI agents.
  2. The compiled configuration file for `llm_party` library

### Parameters

It receives parameters as follows:

- `--party-conf-dir` (or `-p`): a directory containing configuration files for `llm_party` library (required)
- `--exp-conf` (or `-t`): the configuration file for the test (required)
- `--verbose` (or `-v`): a flag to enable verbose mode
- `--output-dir` (or `-o`): the directory to save the output files (optional)

### Methods

- `main`: the main method of this script. It parses the command-line arguments and calls the `run` method.
- `run`: the controller method of this script.
- `conduct_session`

## Q

I am developing python project named `llm_eval`. I want to add a new python script with the following requirements.

### Functionality

- Like the script provided in `main.py`, this new script also allows users evaluate if two AI agents conduct high-quality chat session. To this end, this script conducts a chat session between two AI agents and provides the users with the chat history.
- By executing this script, it conducts multiple *experiment suites* that consists of multiple chat sessions between two AI agents.
- Here is a sample configuration file for the experiment suite list:

```yaml
# sample of "exp suites conf"
- exp suite: Experiment Suite 1
  # sessions are conducted by various agents and clients pair with the same configuration
  init instr dirs:
    - "/path/to/dir" # initial instruction dir 1. Typically used for agent's initial instruction
    - "/path/to/dir" # initial instruction dir 2. Typically used for client's initial instruction
  party conf: "/path/to/file.yaml"
  exp conf: "/path/to/file.yaml"
- exp suite: Experiment Suite 2
  # sessions are conducted by various agents and clients pair with the same configuration
  init instr dirs:
    - "/path/to/dir" # initial instruction dir 1. Typically used for agent's initial instruction
    - "/path/to/dir" # initial instruction dir 2. Typically used for client's initial instruction
  party conf: "/path/to/file.yaml"
  exp conf: "/path/to/file.yaml"
```

- Each element in "exp suites conf" represents the configuration of each experiment suite that consists of the following parameters:
  1. The initial instruction files located in "init instr dir 1"
  2. The second initial instruction file located in "init instr dir 2"
  3. party conf file specified as the value of "party conf"
  4. exp conf file specified as the value of "exp conf"
- To conduct each experiment suite, call `run_exp_suite` in `controller.py`. This method is still under development and not yet fully implemented yet. We need to implement placeholder method, add Docstring, error handling, and so on.

### Parameters

It receives parameters as follows:

- `--exp-suites-conf` (or `-c`): the configuration file for the experiment suites (required)
- `--verbose` (or `-v`): a flag to enable verbose mode
- `--output-dir` (or `-o`): the directory to save the output files (required)

### Pseudo code

Roughly speaking, the pseudo code for this script might be as follows (But, I am not sure if this is correct. Please correct it if I am wrong):

```python
def main():
    # Parse the command-line arguments
    exp_suites_conf, verbose, output_dir = ...

    # Load the configuration file for the experiment suites
    exp_suite_conf_list = yaml.load(exp_suites_conf)
    run(exp_suite_conf_list, verbose, output_dir)

def run(exp_suite_conf_list, verbose, output_dir):
    # Conduct each experiment suite
    for exp_suite in exp_suite_conf_list:
        run_exp_suite(exp_suite, verbose, output_dir)

def run_exp_suite(exp_suite, verbose, output_dir):
    init_instr_dirs = exp_suite["init instr dirs"]
    party_conf = exp_suite["party conf"]
    exp_conf = exp_suite["exp conf"]

    # Make the list of tuples by generating all combinations of the initial instruction directories. See the following example:
    # init_instr_dirs = ["/path/to/dir1", "/path/to/dir2"]
    # Assume that dir 1 contains 2 files and dir 2 contains 2 files. Then, the list of tuples is as follows:
    # [("path/to/dir1/file1.md", "path/to/dir2/file1.md"), ("path/to/dir1/file1.md", "path/to/dir2/file2.md"), ("path/to/dir1/file2.md", "path/to/dir2/file1.md"), ("path/to/dir1/file2.md", "path/to/dir2/file2.md")]
    init_instr_lists = make_init_instr_lists(init_instr_dirs)

    for init_instr in init_instr_lists:
        # Conduct the chat session
        run_exp_with_single_party_conf(init_instr, party_conf, exp_conf, verbose, output_dir)
```