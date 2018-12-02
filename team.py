from dataclasses import dataclass

@dataclass
class TeamInfo:
    ap_rank: int
    coaches_rank: int
    home_status : int
    talent: float
    statistics : list