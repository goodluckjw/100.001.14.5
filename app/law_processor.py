import re
from collections import defaultdict

def has_batchim(word):
    code = ord(word[-1]) - 0xAC00
    return (code % 28) != 0

def has_rieul_batchim(word):
    code = ord(word[-1]) - 0xAC00
    return (code % 28) == 8

def apply_josa_rule(orig_chunk, replace_chunk, josa):
    b_has_batchim = has_batchim(replace_chunk)
    b_has_rieul = has_rieul_batchim(replace_chunk)

    if josa is None:
        if not has_batchim(orig_chunk):
            if not b_has_batchim or b_has_rieul:
                return f'“{orig_chunk}”를 “{replace_chunk}”로 한다.'
            else:
                return f'“{orig_chunk}”를 “{replace_chunk}”으로 한다.'
        else:
            if not b_has_batchim or b_has_rieul:
                return f'“{orig_chunk}”을 “{replace_chunk}”로 한다.'
            else:
                return f'“{orig_chunk}”을 “{replace_chunk}”으로 한다.'

    rules = {
        "을": lambda: f'“{orig_chunk}”을 “{replace_chunk}”{"로" if b_has_rieul else "으로"} 한다.' if b_has_batchim else f'“{orig_chunk}을”을 “{replace_chunk}를”로 한다.',
        "를": lambda: f'“{orig_chunk}를”을 “{replace_chunk}을”로 한다.' if b_has_batchim else f'“{orig_chunk}”를 “{replace_chunk}”로 한다.',
        # 여기에 나머지 조사 규칙을 채우세요...
    }

    return rules.get(josa, lambda: f'“{orig_chunk}”를 “{replace_chunk}”로 한다.')()

                                                                                                                      
                                                                                                                      
