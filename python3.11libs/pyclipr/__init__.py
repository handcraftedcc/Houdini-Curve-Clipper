from .pyclipr import *
from .version import __version__

# Clipper2 defines Bevel as JoinType value 1, but pyclipr 0.1.8 omits the
# symbolic name from its Python binding.
if not hasattr(JoinType, "Bevel"):
    JoinType.Bevel = JoinType(1)
    JoinType.__dict__["__entries"]["Bevel"] = (JoinType.Bevel, None)
