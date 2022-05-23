from tqdm import tqdm
from functools import partial

progress = partial(tqdm, ascii="─╾━")
