from utils.config import MORSE_DICT

def decode_sequence(sequence):
    return MORSE_DICT.get(sequence, "?")