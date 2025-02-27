# -*- coding: utf-8 -*-
"""
English-Thai Machine Translation

from VISTEC-depa Thailand Artificial Intelligence Research Institute

Website: https://airesearch.in.th/releases/machine-translation-models/
"""
import os
import tarfile
from collections import defaultdict

from pythainlp.corpus import download, get_corpus_path
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path

from fairseq.models.transformer import TransformerModel
from sacremoses import MosesTokenizer


_EN_TH_MODEL_NAME = "scb_1m_en-th_moses"
# SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0.tar.gz
_EN_TH_FILE_NAME = "SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0"

_TH_EN_MODEL_NAME = "scb_1m_th-en_spm"
# SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0.tar.gz
_TH_EN_FILE_NAME = "SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0"


def _get_translate_path(model: str, *path: str) -> str:
    return os.path.join(get_full_data_path(model), *path)


def _download_install(name: str) -> None:
    if get_corpus_path(name) is None:
        download(name, force=True, version="1.0")
        tar = tarfile.open(get_corpus_path(name), "r:gz")
        tar.extractall()
        tar.close()
    if not os.path.exists(get_full_data_path(name)):
        os.mkdir(get_full_data_path(name))
        with tarfile.open(get_corpus_path(name)) as tar:
            tar.extractall(path=get_full_data_path(name))


def download_model_all() -> None:
    """
    Download all translation models in advanced
    """
    _download_install(_EN_TH_MODEL_NAME)
    _download_install(_TH_EN_MODEL_NAME)


class EnThTranslator:
    """
    English-Thai Machine Translation

    from VISTEC-depa Thailand Artificial Intelligence Research Institute

    Website: https://airesearch.in.th/releases/machine-translation-models/
    """
    def __init__(self):
        self._tokenizer = MosesTokenizer("en")

        self._model_name = _EN_TH_MODEL_NAME

        _download_install(self._model_name)
        self._model = TransformerModel.from_pretrained(
            model_name_or_path=_get_translate_path(
                self._model_name,
                _EN_TH_FILE_NAME,
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=_get_translate_path(
                self._model_name,
                _EN_TH_FILE_NAME,
                "vocab",
            ),
        )

    def translate(self, text: str) -> str:
        """
        Translate text from English to Thai

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from English to Thai::

            from pythainlp.translate import EnThTranslator

            enth = EnThTranslator()

            enth.translate("I love cat.")
            # output: ฉันรักแมว

        """
        tokens = " ".join(self._tokenizer.tokenize(text))
        translated = self._model.translate(tokens)
        return translated.replace(" ", "").replace("▁", " ").strip()


class ThEnTranslator:
    """
    Thai-English Machine Translation

    from VISTEC-depa Thailand Artificial Intelligence Research Institute

    Website: https://airesearch.in.th/releases/machine-translation-models/
    """
    def __init__(self):
        self._model_name = _TH_EN_MODEL_NAME

        _download_install(self._model_name)
        self._model = TransformerModel.from_pretrained(
            model_name_or_path=_get_translate_path(
                self._model_name,
                _TH_EN_FILE_NAME,
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=_get_translate_path(
                self._model_name,
                _TH_EN_FILE_NAME,
                "vocab",
            ),
            bpe="sentencepiece",
            sentencepiece_model=_get_translate_path(
                self._model_name,
                _TH_EN_FILE_NAME,
                "bpe",
                "spm.th.model",
            ),
        )

    def translate(self, text: str) -> str:
        """
        Translate text from Thai to English

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to English::

            from pythainlp.translate import ThEnTranslator

            then = ThEnTranslator()

            then.translate("ฉันรักแมว")
            # output: I love cat.

        """
        return self._model.translate(text)
