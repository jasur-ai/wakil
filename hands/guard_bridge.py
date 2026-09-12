"""Thin bridge so hands/ can validate mandates without importing all of brain/.

brain/guard.py is stdlib-only, so this is a path import — no package ceremony.
"""
from __future__ import annotations

import os
import sys

BRAIN = os.path.join(os.path.dirname(__file__), os.pardir, "brain")
if BRAIN not in sys.path:
    sys.path.insert(0, BRAIN)

from guard import validate_mandate  # noqa: E402,F401
