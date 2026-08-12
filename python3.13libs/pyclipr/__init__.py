from .pyclipr import *
from .version import __version__

# Clipper2 defines Bevel as JoinType value 1, but the upstream
# Python 3.13 binding omitted the symbolic enum member.
if not hasattr(JoinType, "Bevel"):
    JoinType.Bevel = JoinType(1)
    JoinType.__dict__["__entries"]["Bevel"] = (JoinType.Bevel, None)
