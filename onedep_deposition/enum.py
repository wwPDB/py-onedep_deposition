import enum


class Status(enum.Enum):
    DEP = '1'
    PROC = '2'
    AUTH = '3'
    REPL = '4'
    AUCO = '5'
    AUXS = '6'
    AUXU = '7'
    HOLD = '8'
    HPUB = '9'
    OBS = '10'
    POLC = '11'
    REL = '12'
    REUP = '13'
    WAIT = '14'
    WDRN = '15'


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
    AFGHANISTAN = "Afghanistan"
    ALAND = 'Aland Islands'
    ALBANIA = "Albania"
    ALGERIA = "Algeria"
    AMERICAN_SAMOA = "American Samoa"
    ANDORRA = "Andorra"
    ANGOLA = "Angola"
    ANGUILLA = "Anguilla"
    ANTARCTICA = "Antarctica"
    ANTIGUA_BARBUDA = "Antigua And Barbuda"
    ARGENTINA = "Argentina"
    ARMENIA = "Armenia"
    ARUBA = "Aruba"
    AUSTRALIA = "Australia"
    AUSTRIA = "Austria"
    AZERBAIJAN = "Azerbaijan"
    BAHAMAS = "Bahamas"
    BAHRAIN = "Bahrain"
    BANGLADESH = "Bangladesh"
    BARBADOS = "Barbados"
    BELARUS = "Belarus"
    BELGIUM = "Belgium"
    BELIZE = "Belize"
    BENIN = "Benin"
    BERMUDA = "Bermuda"
    BHUTAN = "Bhutan"
    BOLIVIA = "Bolivia, Plurinational State Of"
    BONAIRE = "Bonaire, Sint Eustatius And Saba"
    BOSNIA_HERZEGOVINA = "Bosnia And Herzegovina"
    BOTSWANA = "Botswana"
    BOUVET = "Bouvet Island"
    BRAZIL = "Brazil"
    BRUNEI = "Brunei Darussalam"
    BULGARIA = "Bulgaria"
    BURKINA_FASO = "Burkina Faso"
    BURUNDI = "Burundi"
    CAMBODIA = "Cambodia"
    CAMEROON = "Cameroon"
    CANADA = "Canada"
    CAPE_VERDE = "Cape Verde"
    CAR = "Central African Republic"
    CAYMAN = "Cayman Islands"
    CHAD = "Chad"
    CHILE = "Chile"
    CHINA = "China"
    CHRISTMAS = "Christmas Island"
    COCOS = "Cocos (Keeling) Islands"
    COLOMBIA = "Colombia"
    COMOROS = "Comoros"
    CONGO = "Congo"
    COOK = "Cook Islands"
    COSTA_RICA = "Costa Rica"
    CROATIA = "Croatia"
    CUBA = "Cuba"
    CURAAAO = "CuraAao"
    CYPRUS = "Cyprus"
    CZECH_REPUBLIC = "Czech Republic"
    DENMARK = "Denmark"
    DJIBOUTI = "Djibouti"
    DOMINICA = "Dominica"
    DOMINICAN_REPUBLIC = "Dominican Republic"
    DRC = "Congo, The Democratic Republic Of The"
    ECUADOR = "Ecuador"
    EGYPT = "Egypt"
    EL_SALVADOR = "El Salvador"
    EQUATORIAL_GUINEA = "Equatorial Guinea"
    ERITREA = "Eritrea"
    ESTONIA = "Estonia"
    ETHIOPIA = "Ethiopia"
    FAROE = "Faroe Islands"
    FIJI = "Fiji"
    FINLAND = "Finland"
    FRANCE = "France"
    FRENCH_GUIANA = "French Guiana"
    FRENCH_POLYNESIA = "French Polynesia"
    FRENCH_SOUTHERN = "French Southern Territories"
    GABON = "Gabon"
    GAMBIA = "Gambia"
    GEORGIA = "Georgia"
    GERMANY = "Germany"
    GHANA = "Ghana"
    GIBRALTAR = "Gibraltar"
    GREECE = "Greece"
    GREENLAND = "Greenland"
    GRENADA = "Grenada"
    GUADELOUPE = "Guadeloupe"
    GUAM = "Guam"
    GUATEMALA = "Guatemala"
    GUERNSEY = "Guernsey"
    GUINEA = "Guinea"
    GUINEA_BISSAU = "Guinea-Bissau"
    GUYANA = "Guyana"
    HAITI = "Haiti"
    HEARD_MCDONALD = "Heard Island And Mcdonald Islands"
    HONDURAS = "Honduras"
    HONG_KONG = "Hong Kong"
    HUNGARY = "Hungary"
    ICELAND = "Iceland"
    INDIA = "India"
    INDONESIA = "Indonesia"
    IRAN = "Iran, Islamic Republic Of"
    IRAQ = "Iraq"
    IRELAND = "Ireland"
    ISLE_OF_MAN = "Isle Of Man"
    ISRAEL = "Israel"
    ITALY = "Italy"
    IVORY_COAST = "CAte D'Ivoire"
    JAMAICA = "Jamaica"
    JAPAN = "Japan"
    JERSEY = "Jersey"
    JORDAN = "Jordan"
    KAZAKHSTAN = "Kazakhstan"
    KENYA = "Kenya"
    KIRIBATI = "Kiribati"
    KUWAIT = "Kuwait"
    KYRGYZSTAN = "Kyrgyzstan"
    LAOS = "Lao People'S Democratic Republic"
    LATVIA = "Latvia"
    LEBANON = "Lebanon"
    LESOTHO = "Lesotho"
    LIBERIA = "Liberia"
    LIBYA = "Libya"
    LIECHTENSTEIN = "Liechtenstein"
    LITHUANIA = "Lithuania"
    LUXEMBOURG = "Luxembourg"
    MACAO = "Macao"
    MACEDONIA = "Macedonia"
    MADAGASCAR = "Madagascar"
    MALAWI = "Malawi"
    MALAYSIA = "Malaysia"
    MALDIVES = "Maldives"
    MALI = "Mali"
    MALTA = "Malta"
    MALVINAS = "Falkland Islands (Malvinas)"
    MARSHALL = "Marshall Islands"
    MARTINIQUE = "Martinique"
    MAURITANIA = "Mauritania"
    MAURITIUS = "Mauritius"
    MAYOTTE = "Mayotte"
    MEXICO = "Mexico"
    MICRONESIA = "Micronesia, Federated States Of"
    MOLDOVA = "Moldova, Republic Of"
    MONACO = "Monaco"
    MONGOLIA = "Mongolia"
    MONTENEGRO = "Montenegro"
    MONTSERRAT = "Montserrat"
    MOROCCO = "Morocco"
    MOZAMBIQUE = "Mozambique"
    MYANMAR = "Myanmar"
    NAMIBIA = "Namibia"
    NAURU = "Nauru"
    NEPAL = "Nepal"
    NETHERLANDS = "Netherlands"
    NEW_CALEDONIA = "New Caledonia"
    NEW_ZEALAND = "New Zealand"
    NICARAGUA = "Nicaragua"
    NIGER = "Niger"
    NIGERIA = "Nigeria"
    NIUE = "Niue"
    NORFOLK = "Norfolk Island"
    NORTH_KOREA = "Korea, Democratic People'S Republic Of"
    NORTHERN_MARIANA = "Northern Mariana Islands"
    NORWAY = "Norway"
    OMAN = "Oman"
    PAKISTAN = "Pakistan"
    PALAU = "Palau"
    PALESTINIAN = "Palestinian Territory"
    PANAMA = "Panama"
    PAPUA_NEW_GUINEA = "Papua New Guinea"
    PARAGUAY = "Paraguay"
    PERU = "Peru"
    PHILIPPINES = "Philippines"
    PITCAIRN = "Pitcairn"
    POLAND = "Poland"
    PORTUGAL = "Portugal"
    PUERTO_RICO = "Puerto Rico"
    QATAR = "Qatar"
    RAUNION = "RAunion"
    ROMANIA = "Romania"
    RUSSIA = "Russian Federation"
    RWANDA = "Rwanda"
    SAINT_BARTHALEMY = "Saint BarthAlemy"
    SAINT_HELENA = "Saint Helena, Ascension And Tristan Da Cunha"
    SAINT_KITTS = "Saint Kitts And Nevis"
    SAINT_LUCIA = "Saint Lucia"
    SAINT_MARTIN = "Saint Martin (French Part)"
    SAINT_PIERRE = "Saint Pierre And Miquelon"
    SAINT_VINCENT = "Saint Vincent And The Grenadines"
    SAMOA = "Samoa"
    SAN_MARINO = "San Marino"
    SAO_TOME_PRINCIPE = "Sao Tome And Principe"
    SAUDI_ARABIA = "Saudi Arabia"
    SENEGAL = "Senegal"
    SERBIA = "Serbia"
    SEYCHELLES = "Seychelles"
    SIERRA_LEONE = "Sierra Leone"
    SINGAPORE = "Singapore"
    SINT_MAARTEN = "Sint Maarten (Dutch Part)"
    SLOVAKIA = "Slovakia"
    SLOVENIA = "Slovenia"
    SOLOMON = "Solomon Islands"
    SOMALIA = "Somalia"
    SOUTH_AFRICA = "South Africa"
    SOUTH_GEORGIA = "South Georgia And The South Sandwich Islands"
    SOUTH_KOREA = "Korea, Republic Of"
    SOUTH_SUDAN = "South Sudan"
    SPAIN = "Spain"
    SRI_LANKA = "Sri Lanka"
    SUDAN = "Sudan"
    SURINAME = "Suriname"
    SVALBARD = "Svalbard And Jan Mayen"
    SWAZILAND = "Swaziland"
    SWEDEN = "Sweden"
    SWITZERLAND = "Switzerland"
    SYRIA = "Syrian Arab Republic"
    TAIWAN = "Taiwan"
    TAJIKISTAN = "Tajikistan"
    TANZANIA = "Tanzania, United Republic Of"
    THAILAND = "Thailand"
    TIMOR_LESTE = "Timor-Leste"
    TOGO = "Togo"
    TOKELAU = "Tokelau"
    TONGA = "Tonga"
    TRINIDAD_TOBAGO = "Trinidad And Tobago"
    TUNISIA = "Tunisia"
    TURKEY = "Turkey"
    TURKMENISTAN = "Turkmenistan"
    TURKS_CAICOS = "Turks And Caicos Islands"
    TUVALU = "Tuvalu"
    UAE = "United Arab Emirates"
    UGANDA = "Uganda"
    UK = "United Kingdom"
    UKRAINE = "Ukraine"
    URUGUAY = "Uruguay"
    USA = "United States"
    USA_ISLANDS = "United States Minor Outlying Islands"
    UZBEKISTAN = "Uzbekistan"
    VANUATU = "Vanuatu"
    VATICAN = "Holy See (Vatican City State)"
    VENEZUELA = "Venezuela, Bolivarian Republic Of"
    VIETNAM = "Viet Nam"
    VIRGIN_BRITISH = "Virgin Islands, British"
    VIRGIN_USA = "Virgin Islands, U.S."
    WALLIS_FUTUNA = "Wallis And Futuna"
    WESTERN_SAHARA = "Western Sahara"
    YEMEN = "Yemen"
    ZAMBIA = "Zambia"
    ZIMBABWE = "Zimbabwe"


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
