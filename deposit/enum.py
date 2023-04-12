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

class FileType(enum.Enum):
    LAYER = "layer-lines"
    FSC_XML = "fsc-xml"
    PDB_COORD = "co-pdb"
    MMCIF_COORD = "co-cif"
    EM_MAP = "vo-map"
    ENTRY_IMAGE = "img-emdb"
    EM_ADDITIONAL_MAP = "add-map"
    EM_MASK = "mask-map"
    EM_HALF_MAP = "half-map"
    CRYSTAL_STRUC_FACTORS = "xs-cif"
    CRYSTAL_MTZ = "xs-mtz"
    CRYSTAL_PARAMETER = "xa-par"
    CRYSTAL_TOPOLOGY = "xa-top"
    VIRUS_MATRIX = "xa-mat"
    NMR_ACS = "nm-shi"
    NMR_RESTRAINT_AMBER = "nm-res-amb"
    NMR_TOPOLOGY_AMBER = "nm-aux-amb"
    NMR_RESTRAINT_BIOSYM = "nm-res-bio"
    NMR_RESTRAINT_CHARMM = "nm-res-cha"
    NMR_RESTRAINT_CNS = "nm-res-cns"
    NMR_RESTRAINT_CYANA = "nm-res-cya"
    NMR_RESTRAINT_DYNAMO = "nm-res-dyn"
    NMR_RESTRAINT_PALES = "nm-res-dyn"
    NMR_RESTRAINT_TALOS = "nm-res-dyn"
    NMR_RESTRAINT_GROMACS = "nm-res-gro"
    NMR_TOPOLOGY_GROMACS = "nm-aux-gro"
    NMR_RESTRAINT_ISD = "nm-res-isd"
    NMR_RESTRAINT_ROSETTA = "nm-res-ros"
    NMR_RESTRAINT_SYBYL = "nm-res-syb"
    NMR_RESTRAINT_XPLOR = "nm-res-xpl"
    NMR_RESTRAINT_OTHER = "nm-res-oth"
    NMR_SPECTRAL_PEAK = "nm-pea-any"
    NMR_UNIFIED_NEF = "nm-uni-nef"
    NMR_UNIFIED_STAR = "nm-uni-str"