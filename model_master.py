import os

from mortm.mortm import MORTM
from mortm.progress import _DefaultLearningProgress
from mortm.tokenizer import Tokenizer, get_token_converter, TO_TOKEN, TO_MUSIC
from mortm.convert import MIDI2Seq
from mortm.de_convert import ct_token_to_midi

from typing import Optional

import torch

def count_files_in_directory(directory: str) -> int:
    """
    指定したディレクトリ内のファイル数をカウントする（サブディレクトリは除外）。
    """
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

class ModelMaster:
    def __init__(self):
        self.model: Optional[MORTM] = MORTM(progress=_DefaultLearningProgress(),vocab_size=393)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.eval()
        self.tokenizer = Tokenizer(get_token_converter(TO_TOKEN))
        pass

    def set_model(self, path):
        self.model.load_state_dict(torch.load(path))
        self.model.to(self.device)

    def continue_measure(self, path: str, file_name):
        directory = path.split(file_name)[0]
        con = MIDI2Seq(self.tokenizer, directory=directory, file_name=file_name, program_list=[0])
        con()
        if not con.is_error:
            seq = con.aya_node[1][:-1]
            gene = self.model.top_p_sampling_measure(seq, p=0.95, max_measure=5, temperature=1.0, context_measure=9)

            t = Tokenizer(get_token_converter(TO_MUSIC))
            t.rev_mode()
            save_file_name = f"gen_{count_files_in_directory('./server/generate_midi/')}.mid"
            save_file_path = f"./server/generate_midi/{save_file_name}"
            _ = ct_token_to_midi(t, gene, save_file_path)

            return save_file_name, save_file_path


