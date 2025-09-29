from dataclasses import dataclass

@dataclass
class Beam:
    speed: float = 250
    delay: float = 1
    duration: float = 1
    width: int = 16

beam_small = Beam(width=5)
beam_medium = Beam(width=8)
beam_large = Beam(width=10)
