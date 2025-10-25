from openai import OpenAI
import tiktoken
import numpy as np
from typing import List, Dict, Tuple

# Set up OpenAI

client = OpenAI(
    api_key="nice_try"
)

# Model for extracting embeddings only
EMBED_MODEL = "text-embedding-3-large"

# i wrote this
def view_tokenization(text: str, model: str = EMBED_MODEL):
    enc = tiktoken.encoding_for_model(model)
    token_ids = enc.encode(text)
    out = []
    for tid in token_ids:
        tok = enc.decode([tid]) 
        out.append(tok)
    return out


# From reference code
def embed_text(text: str, model: str = EMBED_MODEL) -> List[float]:
    """Embed any text span."""
    resp = client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding

def get_token_embeddings(text: str, model: str = EMBED_MODEL) -> List[Dict[str, object]]:
    """
    Tokenize `text` with tiktoken, then embed each decoded token string individually.
    Returns a list of {token_id, token_text, embedding}.
    Note: these are *standalone* token-string embeddings (not contextual hidden states).
    """
    enc = tiktoken.encoding_for_model(model)
    token_ids = enc.encode(text)
    out = []
    for tid in token_ids:
        tok = enc.decode([tid])          # may include leading space for wordpiece-like tokens
        emb = embed_text(tok, model)
        out.append({"token_id": tid, "token_text": tok, "embedding": emb})
    return out



def build_context_windows(
    text: str, target: str, window: int = 3
) -> List[Tuple[str, Tuple[int,int]]]:
    """
    Very simple whitespace tokenization to build short context windows around `target`.
    Returns [(window_text, (start_idx, end_idx)), ...]
    """
    words = text.split()
    out = []
    for i, w in enumerate(words):
        # match target ignoring case and basic punctuation stripping
        core = w.strip(",.;:?!\"'()[]{}").lower()
        if core == target.lower():
            L = max(0, i - window)
            R = min(len(words), i + window + 1)
            span = " ".join(words[L:R])
            out.append((span, (L, R)))
    return out

def embed_context_windows(text: str, target: str, window: int = 3, model: str = EMBED_MODEL):
    """
    For each occurrence of `target`, embed the surrounding window text.
    Returns a list of dicts with {'window_text', 'embedding'}.
    """
    wins = build_context_windows(text, target, window)
    results = []
    for span, _ in wins:
        results.append({
            "window_text": span,
            "embedding": embed_text(span, model)
        })
    return results

def cosine_sim(a: List[float], b: List[float]) -> float:
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / denom) if denom else 0.0

# written by me (henry)
TOKENIZER_ENCODING = tiktoken.get_encoding('cl100k_base')

def tokenize_helper(string: str):
    return TOKENIZER_ENCODING.encode(string)

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
pca = PCA(n_components=2)
def pca_transform(data):
    normalized = StandardScaler().fit_transform(data)
    frame = pd.DataFrame(normalized)
    return pca.fit_transform(frame)