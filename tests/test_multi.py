from dataclasses import dataclass
import os
from typing import Text

from dataconf import multi


class TestMulti:
    def test_simple(self) -> None:
        @dataclass
        class A:
            a: Text

        expected = A(a="test")
        assert multi.string("a = test").on(A) == expected
        assert multi.dict({"a": "test"}).on(A) == expected

    def test_chain(self) -> None:
        @dataclass
        class A:
            a: Text
            b: int

        assert multi.string("a = test").string("b = 2").on(A) == A(a="test", b=2)

    def test_complex(self) -> None:
        @dataclass
        class N:
            b: int
            c: int
            d: int

        @dataclass
        class A:
            a: N

        assert multi.string("a { b = 1\nc = 2 }").string("a { c = 3\nd = 4 }").on(
            A
        ) == A(a=N(b=1, c=3, d=4))

    def test_multi_source(self) -> None:
        @dataclass
        class A:
            a: Text
            b: int

        os.environ["DATACLASS_A"] = "1"
        assert multi.string("b = 2").env("DATACLASS").on(A) == A(a="1", b=2)
        os.environ.pop("DATACLASS_A")