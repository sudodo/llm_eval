import os
import yaml
import unittest
from typing import List, Dict
import unittest
from unittest.mock import patch, mock_open
import os
from llm_eval.service import load_instructions, compile_party_config, conduct_chat_session
from llm_party.model.session_models import ChatSession


class TestChatSession(unittest.TestCase):
    def setUp(self):
        self.init_instr_dir = 'test_instructions'
        self.party_conf = 'tests/data/test_party_conf.yaml'
        os.makedirs(self.init_instr_dir, exist_ok=True)
        with open(os.path.join(self.init_instr_dir, 'instr1.txt'), 'w') as file:
            file.write('Test instruction 1')
        with open(os.path.join(self.init_instr_dir, 'instr2.txt'), 'w') as file:
            file.write('Test instruction 2')

        # with open(self.party_conf, 'w') as file:
        #     yaml.dump({'attendees': [{'instruction': {'text': ''}}, {'instruction': {'text': ''}}]}, file)

    def tearDown(self):
        # os.remove(self.party_conf)
        for file_name in os.listdir(self.init_instr_dir):
            os.remove(os.path.join(self.init_instr_dir, file_name))
        os.rmdir(self.init_instr_dir)

    def test_load_instructions(self):
        instructions = load_instructions(self.init_instr_dir)
        self.assertEqual(len(instructions), 2)
        self.assertIn('Test instruction 1', instructions)
        self.assertIn('Test instruction 2', instructions)

    def test_compile_party_config(self):
        init_instr = ['Instruction 1', 'Instruction 2']
        party_conf_dict = compile_party_config(self.party_conf, init_instr)
        self.assertEqual(party_conf_dict['attendees'][0]['instruction']['text'], 'Instruction 1')
        self.assertEqual(party_conf_dict['attendees'][1]['instruction']['text'], 'Instruction 2')

    def test_conduct_chat_session(self):
        with open(self.party_conf, 'r') as file:
            party_conf_dict = yaml.safe_load(file)
        exp_conf = {'num_rounds': 2}
        output_dir = 'test_output'
        os.makedirs(output_dir, exist_ok=True)

        with patch('llm_eval.service.start_session') as mock_start_session:
            mock_start_session.return_value = ChatSession(), ""
            conduct_chat_session(party_conf_dict, exp_conf, output_dir, verbose=False)

        # Check if the correct number of rounds were conducted
        self.assertEqual(mock_start_session.call_count, 2)

        # Check if the chat history and party configuration files were created
        file_names = os.listdir(output_dir)
        self.assertEqual(len(file_names), 2)
        self.assertTrue(any(file_name.startswith('chat_history_') for file_name in file_names))
        self.assertTrue(any(file_name.startswith('party_conf_') for file_name in file_names))

        # Clean up the test output directory
        for file_name in file_names:
            os.remove(os.path.join(output_dir, file_name))
        os.rmdir(output_dir)

    def test_conduct_chat_session_default_rounds(self):
        with open(self.party_conf, 'r') as file:
            party_conf_dict = yaml.safe_load(file)
        exp_conf = {}
        output_dir = 'test_output'
        os.makedirs(output_dir, exist_ok=True)

        with patch('llm_eval.service.start_session') as mock_start_session:
            mock_start_session.return_value = ChatSession(), ""
            conduct_chat_session(party_conf_dict, exp_conf, output_dir, verbose=False)

        # Check if the default number of rounds (3) were conducted
        self.assertEqual(mock_start_session.call_count, 3)

        # Clean up the test output directory
        for file_name in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file_name))
        os.rmdir(output_dir)

if __name__ == '__main__':
    unittest.main()