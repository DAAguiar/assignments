""" Module to create a Region Enum to encode all available regions """

from enum import Enum, auto

class Region(Enum):
    """ Enum class to encode all possible regions values"""
    AT = auto()
    BE = auto()
    BG = auto()
    CH = auto()
    CY = auto()
    CZ = auto()
    DK = auto()
    EE = auto()
    EL = auto()
    ES = auto()
    FI = auto()
    FR = auto()
    HR = auto()
    HU = auto()
    IS = auto()
    IT = auto()
    LI = auto()
    LT = auto()
    LU = auto()
    LV = auto()
    MT = auto()
    NL = auto()
    NO = auto()
    PL = auto()
    PT = auto()
    RO = auto()
    SE = auto()
    SI = auto()
    SK = auto()
    DE = auto()
    AL = auto()
    IE = auto()
    ME = auto()
    MK = auto()
    RS = auto()
    AM = auto()
    AZ = auto()
    GE = auto()
    TR = auto()
    UA = auto()
    BY = auto()
    UK = auto()
    XK = auto()
    FX = auto()
    MD = auto()
    SM = auto()
    RU = auto()
    
    DE_TOT = auto()
    EU27_2020 = auto()
    EA18 = auto()
    EA19 = auto()
    EFTA = auto()
    EEA30_2007 = auto()
    EEA31 = auto()
    EU27_2007 = auto()
    EU28 = auto()

    _ignore_ = 'valid_countries'

    @classmethod
    def fetch_valid_countries(cls) -> None:
        if hasattr(cls, "valid_countries"):
            return cls.valid_countries
        else:
            valid_countries = []
            for x in cls:
                if len(x.name) <= 2:
                    valid_countries.append(x)
            cls.valid_countries = valid_countries        
            return cls.valid_countries


if __name__ == '__main__':
    region = Region.PT

    region_2 = Region.AM

    print(region.fetch_valid_countries())
    print(region_2.fetch_valid_countries())

    region3 = region.fetch_valid_countries()

    # print(type(region3))
    # print(region3.name)
