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
        "과": lambda: f'“{orig_chunk}”과 “{replace_chunk}”{"로" if b_has_rieul else "으로"} 한다.' if b_has_batchim else f'“{orig_chunk}과”를 “{replace_chunk}와”로 한다.',
        "와": lambda: f'“{orig_chunk}와”를 “{replace_chunk}과”로 한다.' if b_has_batchim else f'“{orig_chunk}”를 “{replace_chunk}”로 한다.',
        "이": lambda: f'“{orig_chunk}”을 “{replace_chunk}”{"로" if b_has_rieul else "으로"} 한다.' if b_has_batchim else f'“{orig_chunk}이”를 “{replace_chunk}가”로 한다.',
        "가": lambda: f'“{orig_chunk}가”를 “{replace_chunk}이”로 한다.' if b_has_batchim else f'“{orig_chunk}”를 “{replace_chunk}”로 한다.',
        "이나": lambda: f'“{orig_chunk}이나”를 “{replace_chunk}나”로 한다.' if not b_has_batchim else f'“{orig_chunk}”을 “{replace_chunk}”{"로" if b_has_rieul else "으로"} 한다.',
        "나": lambda: f'“{orig_chunk}나”를 “{replace_chunk}이나”로 한다.' if b_has_batchim else f'“{orig_chunk}”를 “{replace_chunk}”로 한다.',
        "으로": lambda: f'“{orig_chunk}으로”를 “{replace_chunk}로”로 한다.' if not b_has_batchim or b_has_rieul else f'“{orig_chunk}”을 “{replace_chunk}”으로 한다.',
        "로": lambda: f'“{orig_chunk}로”를 “{replace_chunk}으로”로 한다.' if b_has_batchim and not b_has_rieul else f'“{orig_chunk}”를 “{replace_chunk}”로 한다.',
        "는": lambda: f'“{orig_chunk}는”을 “{replace_chunk}은”으로 한다.' if b_has_batchim else f'“{orig_chunk}”를 “{replace_chunk}”로 한다.',
        "은": lambda: f'“{orig_chunk}은”을 “{replace_chunk}는”으로 한다.' if not b_has_batchim else f'“{orig_chunk}”을 “{replace_chunk}”{"로" if b_has_rieul else "으로"} 한다.',
    }

    return rules.get(josa, lambda: f'“{orig_chunk}”를 “{replace_chunk}”로 한다.')()

def extract_chunk_and_josa(token, searchword):
    josa_list = ["으로", "이나", "과", "와", "을", "를", "이", "가", "나", "로", "은", "는"]
    pattern = re.compile(rf'({searchword})(?:{"|".join(josa_list)})?$')
    match = pattern.match(token)
    if match:
        chunk = searchword
        suffix = token[len(searchword):]
        josa = suffix if suffix in josa_list else None
        return chunk, josa
    return token, None

def group_locations(locs):
    if len(locs) == 1:
        return locs[0]
    return 'ㆍ'.join(locs[:-1]) + ' 및 ' + locs[-1]

def build_amendment(law_name, amendments, idx):
    parts = []
    for (chunk, replace_chunk, josa), loc_list in amendments.items():
        loc_str = group_locations(loc_list)
        amendment = apply_josa_rule(chunk, replace_chunk, josa)
        parts.append(f'{loc_str} 중 {amendment}')
    prefix = chr(9312 + idx) if idx < 20 else f'({idx + 1})'
    return f'{prefix} {law_name} 일부를 다음과 같이 개정한다.\n' + '\n'.join(parts)

# Example Usage
if __name__ == "__main__":
    amendments_example = {
        ("위원회", "달걀", "는"): ["제58조제1항", "제58조제2항", "제58조제3항", "제58조제4항"],
        ("위원회", "달걀", None): ["제58조제3항제1호", "제58조제4항"]
    }
    law_name_example = "여신전문금융업법"
    idx_example = 0
    print(build_amendment(law_name_example, amendments_example, idx_example))
