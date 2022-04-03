import re
from typing import Optional

reaction_to_lang = {
    "ac": "en-us",
    "ag": "en-us",
    "ai": "en-us",
    "ao": "pt",
    "ar": "es",
    "as": "en-us",
    "at": "de",
    "au": "en-us",
    "aw": "nl",
    "bb": "en-us",
    "be": "nl",
    "bf": "fr",
    "bi": "fr",
    "bj": "fr",
    "bl": "fr",
    "bn": "en-us",
    "bo": "es",
    "bq": "nl",
    "br": "pt",
    "bs": "en-us",
    "bw": "en-us",
    "bz": "en-us",
    "ca": "en-us",
    "cd": "fr",
    "cf": "fr",
    "cg": "fr",
    "ch": "de",
    "ci": "fr",
    "ck": "en-us",
    "cl": "es",
    "cm": "fr",
    "cn": "zh",
    "co": "es",
    "cp": "fr",
    "cr": "es",
    "cu": "es",
    "cv": "pt",
    "cw": "nl",
    "cx": "en-us",
    "de": "de",
    "dj": "fr",
    "dm": "en-us",
    "do": "es",
    "ea": "es",
    "ec": "es",
    "es": "es",
    "fj": "en-us",
    "fk": "en-us",
    "fm": "en-us",
    "fr": "fr",
    "ga": "fr",
    "gb": "en-us",
    "gd": "en-us",
    "gf": "fr",
    "gg": "en-us",
    "gh": "en-us",
    "gi": "en-us",
    "gm": "en-us",
    "gn": "fr",
    "gp": "fr",
    "gq": "es",
    "gs": "en-us",
    "gt": "es",
    "gu": "en-us",
    "gw": "pt",
    "gy": "en-us",
    "hn": "es",
    "ic": "es",
    "im": "en-us",
    "io": "en-us",
    "it": "it",
    "je": "en-us",
    "jm": "en-us",
    "jp": "ja",
    "ke": "en-us",
    "ki": "en-us",
    "kn": "en-us",
    "ky": "en-us",
    "lc": "en-us",
    "li": "de",
    "lr": "en-us",
    "mc": "fr",
    "ml": "fr",
    "mp": "en-us",
    "mq": "fr",
    "ms": "en-us",
    "mu": "en-us",
    "mw": "en-us",
    "mx": "es",
    "mz": "pt",
    "na": "en-us",
    "nc": "fr",
    "ne": "fr",
    "nf": "en-us",
    "ng": "en-us",
    "ni": "es",
    "nl": "nl",
    "nz": "en-us",
    "pa": "es",
    "pe": "es",
    "pf": "fr",
    "pl": "pl",
    "pm": "fr",
    "pn": "en-us",
    "pr": "es",
    "pt": "pt",
    "pw": "en-us",
    "py": "es",
    "re": "fr",
    "ru": "ru",
    "sb": "en-us",
    "sc": "en-us",
    "sg": "en-us",
    "sh": "en-us",
    "sl": "en-us",
    "sm": "it",
    "sn": "fr",
    "sr": "nl",
    "ss": "en-us",
    "st": "pt",
    "sv": "es",
    "sx": "nl",
    "ta": "en-us",
    "tc": "en-us",
    "td": "fr",
    "tf": "fr",
    "tg": "fr",
    "tt": "en-us",
    "ug": "en-us",
    "um": "en-us",
    "us": "en-us",
    "uy": "es",
    "va": "it",
    "vc": "en-us",
    "ve": "es",
    "vg": "en-us",
    "vi": "en-us",
    "wf": "fr",
    "yt": "fr",
    "zm": "en-us",
    "zw": "en-us",
}


def detect_lang(event: dict) -> Optional[str]:
    reaction_name = event.get("reaction")
    m = re.findall("/(?!flag-\b)\b\\w+/", reaction_name)
    if m is not None and m != []:
        country = m[0]
        return reaction_to_lang.get(country)
    return reaction_to_lang.get(reaction_name)