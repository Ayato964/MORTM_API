from mortm import constants
import torch
from mortm.mortm import MORTM
import pretty_midi as pm
import mortm.tokenizer as token
import numpy as np

from mortm.tokenizer import TO_TOKEN, TO_MUSIC

from mortm.progress import _DefaultLearningProgress
from mortm.tokenizer import get_token_converter
from mortm.de_convert import ct_tokens_to_midi


tokenizer = token.Tokenizer(token=get_token_converter(120, TO_MUSIC), load_data="model/vocab/vocab_list.json")

model = MORTM(
    progress=_DefaultLearningProgress(),
    vocab_size=327,
    position_length=8500,
    trans_layer=9, num_heads=32, d_model=1024,
    dim_feedforward=4096
)
model.load_state_dict(torch.load("model/MORTM.train.0.1.9445.pth"))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# メロディ生成の実行
np_notes = np.load("ex/Test1.npz")

start = np_notes[f'array1'][:50]

#start = [tokenizer.get(constants.START_SEQ_TOKEN)]

print(f"First:{start}")

#gene = model.top_p_sampling(start, tokenizer, max_length=20, temperature=2.0)
gene = model.top_k_sampling_with_temperature_sequence(start, max_length=500, temperature=1.1, top_k=5)

#gene = model.generate_by_length(start, max_length=20)

output = gene
for t in output:
    t: torch.Tensor = t
    print(f"{t}  {tokenizer.rev_get(t.tolist())}")


midi = ct_tokens_to_midi(tokenizer, output, "out/generate_test.midi")
