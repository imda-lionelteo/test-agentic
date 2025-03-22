from dataclasses import dataclass
from typing import Literal


@dataclass
class Feedback:
    """
    Feedback is a data model that holds the feedback for the diagrams.
    """

    feedback: str
    score: Literal["pass", "fail"]
