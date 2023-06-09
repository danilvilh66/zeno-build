"""Chatbots using API-based services."""
from __future__ import annotations

import os
from dataclasses import dataclass

from examples.analysis_gpt_mt import config


@dataclass(frozen=True)
class GptMtInstance:
    """An instance from the GPT-MT dataset.

    Attributes:
        data: The input sentence.
        label: The output sentence.
        doc_id: The document ID.
        lang_pair: The language pair.
    """

    data: str
    label: str
    doc_id: str
    lang_pair: str


def process_data(
    input_dir: str,
    lang_pairs: list[str],
) -> list[GptMtInstance]:
    """Load data."""
    # Load the data
    data: list[GptMtInstance] = []
    eval_dir = os.path.join(input_dir, "evaluation", "testset")
    for lang_pair in lang_pairs:
        src_lang, trg_lang = lang_pair[:2], lang_pair[2:]
        src_file = os.path.join(
            eval_dir, "wmt-testset", lang_pair, f"test.{src_lang}-{trg_lang}.{src_lang}"
        )
        trg_file = os.path.join(
            eval_dir, "wmt-testset", lang_pair, f"test.{src_lang}-{trg_lang}.{trg_lang}"
        )
        doc_file = os.path.join(
            eval_dir,
            "wmt-testset-docids",
            lang_pair,
            f"test.{src_lang}-{trg_lang}.docids",
        )
        with open(src_file, "r") as src_in, open(trg_file, "r") as trg_in, open(
            doc_file, "r"
        ) as doc_in:
            for src_line, trg_line, doc_line in zip(src_in, trg_in, doc_in):
                data.append(
                    GptMtInstance(
                        src_line.strip(), trg_line.strip(), doc_line.strip(), lang_pair
                    )
                )
    return data


def process_output(
    input_dir: str,
    lang_pairs: list[str],
    model_preset: str,
) -> list[str]:
    """Load model outputs."""
    # Load the data
    data: list[str] = []
    model_path = config.model_configs[model_preset].path
    system_dir = os.path.join(input_dir, "evaluation", "system-outputs", model_path)
    for lang_pair in lang_pairs:
        src_lang, trg_lang = lang_pair[:2], lang_pair[2:]
        sys_file = os.path.join(
            system_dir, lang_pair, f"test.{src_lang}-{trg_lang}.{trg_lang}"
        )
        with open(sys_file, "r") as sys_in:
            for sys_line in sys_in:
                data.append(sys_line.strip())
    return data
