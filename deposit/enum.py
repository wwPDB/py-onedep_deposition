import enum


class Status(enum.Enum):
    # TODO: Add more
    DEP = '1'
    PROC = '2'
    AUTH = '3'
    REPL = '4'


class ExperimentType(enum.Enum):
    XRAY = 'xray'
    FIBER = 'fiber'
    NEUTRON = 'neutron'
    EM = 'em'
    EC = 'ec'
    NMR = 'nmr'
    SSNMR = 'ssnmr'

class EMSubType(enum.Enum):
    HELICAL = "helical"
    SPA = "single"
    SUBTOMOGRAM = "subtomogram"
    TOMOGRAPHY = "tomography"

class Country(enum.Enum):
    UK = "United Kingdom"
    EUA = "United States"
    JAPAN = "Japan"
    INDIA = "India"
    CHINA = "China"
    # TODO: Add more countries

def get_enum_from_value(value):
    for name, member in Color.__members__.items():
        if member.value == value:
            return member
    raise ValueError("No matching enum found")