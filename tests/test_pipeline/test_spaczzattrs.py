"""Tests for the spaczzattrs module."""
import pytest
from spacy.language import Language
from spacy.tokens import Doc

from spaczz.attrs import SpaczzAttrs
from spaczz.exceptions import AttrOverwriteWarning


@pytest.fixture
def doc(nlp: Language) -> Doc:
    """Doc for testing."""
    return nlp("one ent test.")


def test_initialize_again_skips() -> None:
    """Subsequent `SpaczzAttrs` initializations do nothing."""
    SpaczzAttrs.initialize()
    assert SpaczzAttrs._initialized is True


def test_get_token_types(nlp: Language) -> None:
    """Returns token match types."""
    doc = nlp("one ent")
    doc[0]._.spaczz_counts = (0, 0, 0)
    doc[1]._.spaczz_ratio = 100
    assert doc[0]._.spaczz_types == {"regex"}
    assert doc[1]._.spaczz_types == {"fuzzy"}


def test_get_spaczz_span(doc: Doc) -> None:
    """Returns spaczz span boolean."""
    for token in doc[:2]:
        token._.spaczz_token = True
    assert doc[:2]._.spaczz_span is True


def test_get_span_types1(doc: Doc) -> None:
    """Returns span match types."""
    for token in doc[:2]:
        token._.spaczz_ratio = 100
        token._.spaczz_counts = (0, 0, 0)
    assert doc[:2]._.spaczz_types == {"regex", "fuzzy"}


def test_get_span_types2(doc: Doc) -> None:
    """Returns span match types."""
    for token in doc[:2]:
        token._.spaczz_ratio = 100
    assert doc[:2]._.spaczz_types == {"fuzzy"}


def test_get_span_types3(doc: Doc) -> None:
    """Returns span match types."""
    for token in doc[:2]:
        token._.spaczz_counts = (0, 0, 0)
    assert doc[:2]._.spaczz_types == {"regex"}


def test_get_ratio1(doc: Doc) -> None:
    """Returns span ratio."""
    for token in doc[:2]:
        token._.spaczz_ratio = 100
    assert doc[:2]._.spaczz_ratio == 100


def test_get_ratio2(doc: Doc) -> None:
    """Returns span ratio."""
    doc[0]._.spaczz_ratio = 100
    doc[1]._.spaczz_counts = (0, 0, 0)
    assert doc[:2]._.spaczz_ratio is None


def test_get_counts1(doc: Doc) -> None:
    """Returns span counts."""
    for token in doc[:2]:
        token._.spaczz_counts = (0, 0, 0)
    assert doc[:2]._.spaczz_counts == (0, 0, 0)


def test_get_counts2(doc: Doc) -> None:
    """Returns span counts."""
    doc[0]._.spaczz_ratio = 100
    doc[1]._.spaczz_counts = (0, 0, 0)
    assert doc[:2]._.spaczz_counts is None


def test_get_spaczz_doc(doc: Doc) -> None:
    """Returns spaczz doc boolean."""
    for token in doc[:2]:
        token._.spaczz_token = True
    assert doc._.spaczz_doc is True


def test_get_doc_types(doc: Doc) -> None:
    """Returns doc match types."""
    doc[0]._.spaczz_ratio = 100
    doc[1]._.spaczz_counts = (0, 0, 0)
    assert doc._.spaczz_types == {"fuzzy", "regex"}


def test_init_w_duplicate_custom_attrs_warns() -> None:
    """`.initialize()` raises `AttributeError` if duplicate custom attrs exist."""
    SpaczzAttrs._initialized = False
    with pytest.warns(AttrOverwriteWarning):
        SpaczzAttrs.initialize()
