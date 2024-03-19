
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
- `--test-conf` (or `-t`): the configuration file for the test (required)
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
party_conf, test_conf, init_instr_dir, verbose = ...

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