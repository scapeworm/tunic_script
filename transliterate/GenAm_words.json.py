#!/usr/bin/env python3

import abc
import enum
import json
import logging
import re
import sys


class Phoneme(enum.StrEnum):
    def __repr__(self):
        return str(self)


class ConsonantPhoneme(Phoneme):
    B = "b"
    CH = "tʃ"
    D = "d"
    DH = "ð"
    F = "f"
    G = "ɡ"
    HH = "h"
    JH = "dʒ"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    NG = "ŋ"
    P = "p"
    R = "ɹ"
    S = "s"
    SH = "ʃ"
    T = "t"
    TH = "θ"
    V = "v"
    W = "w"
    Y = "j"
    Z = "z"
    ZH = "ʒ"


class VowelPhoneme(Phoneme):
    AA = "ɑ"
    AE = "æ"
    AH = "ʌ"
    AO = "ɔ"
    AW = "aʊ"
    AX = "ə"
    AY = "aɪ"
    EH = "ɛ"
    EX = "ɜ"
    EY = "eɪ"
    IH = "ɪ"
    IY = "i"
    OW = "oʊ"
    OY = "ɔɪ"
    UH = "ʊ"
    UW = "u"


class CmudictComponent(enum.StrEnum):
    def __repr__(self):
        return str(self)

    @classmethod
    def parse(cls, s):
        try:
            return cls(s)
        except ValueError:
            return None


class CmudictConsonant(CmudictComponent):
    B = "B"
    CH = "CH"
    D = "D"
    DH = "DH"
    F = "F"
    G = "G"
    HH = "HH"
    JH = "JH"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    NG = "NG"
    P = "P"
    R = "R"
    S = "S"
    SH = "SH"
    T = "T"
    TH = "TH"
    V = "V"
    W = "W"
    Y = "Y"
    Z = "Z"
    ZH = "ZH"


class CmudictVowel(CmudictComponent):
    AA = "AA"
    AE = "AE"
    AH = "AH"
    AO = "AO"
    AW = "AW"
    AY = "AY"
    EH = "EH"
    ER = "ER"
    EY = "EY"
    IH = "IH"
    IY = "IY"
    OW = "OW"
    OY = "OY"
    UH = "UH"
    UW = "UW"


class CmudictStress(CmudictComponent):
    NONE = "0"
    PRIMARY = "1"
    SECONDARY = "2"


class CmudictSegment(abc.ABC):
    @property
    @abc.abstractmethod
    def phone(self):
        pass

    @abc.abstractmethod
    def phonemes(self):
        pass

    def __repr__(self):
        return str(self)


class CmudictConsonantSegment(CmudictSegment):
    def __init__(self, consonant):
        self.consonant = consonant

    @property
    def phone(self):
        return self.consonant

    def phonemes(self):
        if self.consonant == CmudictConsonant.B:
            yield ConsonantPhoneme.B
        if self.consonant == CmudictConsonant.CH:
            yield ConsonantPhoneme.CH
        if self.consonant == CmudictConsonant.D:
            yield ConsonantPhoneme.D
        if self.consonant == CmudictConsonant.DH:
            yield ConsonantPhoneme.DH
        if self.consonant == CmudictConsonant.F:
            yield ConsonantPhoneme.F
        if self.consonant == CmudictConsonant.G:
            yield ConsonantPhoneme.G
        if self.consonant == CmudictConsonant.HH:
            yield ConsonantPhoneme.HH
        if self.consonant == CmudictConsonant.JH:
            yield ConsonantPhoneme.JH
        if self.consonant == CmudictConsonant.K:
            yield ConsonantPhoneme.K
        if self.consonant == CmudictConsonant.L:
            yield ConsonantPhoneme.L
        if self.consonant == CmudictConsonant.M:
            yield ConsonantPhoneme.M
        if self.consonant == CmudictConsonant.N:
            yield ConsonantPhoneme.N
        if self.consonant == CmudictConsonant.NG:
            yield ConsonantPhoneme.NG
        if self.consonant == CmudictConsonant.P:
            yield ConsonantPhoneme.P
        if self.consonant == CmudictConsonant.R:
            yield ConsonantPhoneme.R
        if self.consonant == CmudictConsonant.S:
            yield ConsonantPhoneme.S
        if self.consonant == CmudictConsonant.SH:
            yield ConsonantPhoneme.SH
        if self.consonant == CmudictConsonant.T:
            yield ConsonantPhoneme.T
        if self.consonant == CmudictConsonant.TH:
            yield ConsonantPhoneme.TH
        if self.consonant == CmudictConsonant.V:
            yield ConsonantPhoneme.V
        if self.consonant == CmudictConsonant.W:
            yield ConsonantPhoneme.W
        if self.consonant == CmudictConsonant.Y:
            yield ConsonantPhoneme.Y
        if self.consonant == CmudictConsonant.Z:
            yield ConsonantPhoneme.Z
        if self.consonant == CmudictConsonant.ZH:
            yield ConsonantPhoneme.ZH

    @classmethod
    def parse(cls, s):
        consonant = CmudictConsonant.parse(s)
        if consonant is None:
            return None
        return cls(consonant)

    def __str__(self):
        return f"{self.consonant}"


class CmudictVowelSegment(CmudictSegment):
    def __init__(self, vowel, stress):
        self.vowel = vowel
        self.stress = stress

    @property
    def phone(self):
        return self.vowel

    def phonemes(self):
        if self.vowel == CmudictVowel.AA:
            yield VowelPhoneme.AA
        if self.vowel == CmudictVowel.AE:
            yield VowelPhoneme.AE
        if self.vowel == CmudictVowel.AH:
            if self.stress != CmudictStress.NONE:
                yield VowelPhoneme.AH
            else:
                yield VowelPhoneme.AX
        if self.vowel == CmudictVowel.AO:
            yield VowelPhoneme.AO
        if self.vowel == CmudictVowel.AW:
            yield VowelPhoneme.AW
        if self.vowel == CmudictVowel.AY:
            yield VowelPhoneme.AY
        if self.vowel == CmudictVowel.EH:
            yield VowelPhoneme.EH
        if self.vowel == CmudictVowel.ER:
            if self.stress != CmudictStress.NONE:
                yield VowelPhoneme.EX
            else:
                yield VowelPhoneme.AX
            yield ConsonantPhoneme.R
        if self.vowel == CmudictVowel.EY:
            yield VowelPhoneme.EY
        if self.vowel == CmudictVowel.IH:
            yield VowelPhoneme.IH
        if self.vowel == CmudictVowel.IY:
            yield VowelPhoneme.IY
        if self.vowel == CmudictVowel.OW:
            yield VowelPhoneme.OW
        if self.vowel == CmudictVowel.OY:
            yield VowelPhoneme.OY
        if self.vowel == CmudictVowel.UH:
            yield VowelPhoneme.UH
        if self.vowel == CmudictVowel.UW:
            yield VowelPhoneme.UW

    @classmethod
    def parse(cls, s):
        m = re.fullmatch(r"(.+?)([0-9]+)", s)
        if m is None:
            return None
        vowel = CmudictVowel.parse(m.group(1))
        if vowel is None:
            return None
        stress = CmudictStress.parse(m.group(2))
        if stress is None:
            return None
        return cls(vowel, stress)

    def __str__(self):
        return f"{self.vowel}{self.stress}"


def cmudict_word(field):
    m = re.fullmatch(r"([a-z'.-]+)(\([2-9][0-9]*\))?", field)
    return m.group(1)


def cmudict_phones(fields):
    for field in fields:
        consonant_segment = CmudictConsonantSegment.parse(field)
        if consonant_segment is not None:
            yield consonant_segment
            continue
        vowel_segment = CmudictVowelSegment.parse(field)
        if vowel_segment is not None:
            yield vowel_segment
            continue
        assert False, field


def cmudict_entries(lines):
    for line in lines:
        line = line.rstrip("\n")
        fields = line.split(" ")
        try:
            i = fields.index("#")
            fields = fields[:i]
        except ValueError:
            pass
        word = cmudict_word(fields[0])
        phones = list(cmudict_phones(fields[1:]))
        yield word, phones


def word_pronunciations(cmudict_entries):
    for word, phones in cmudict_entries:
        pronunciation = "".join(
            phoneme
            for phone in phones
            for phoneme in phone.phonemes()
        )
        yield word, pronunciation


def run(in_, out):
    words = {}

    for word, pronunciation in word_pronunciations(cmudict_entries(in_)):
        pronunciations = words.setdefault(word, [])
        if pronunciation not in pronunciations:
            pronunciations.append(pronunciation)
        else:
            logging.info(f"skip duplicate: {word} = {pronunciation}")

    logging.info(f"words generated: {len(words)}")

    json.dump(
        obj=words,
        fp=out,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def main():
    logging.basicConfig(
        level=logging.INFO,
    )

    run(in_=sys.stdin, out=sys.stdout)


if __name__ == "__main__":
    main()
