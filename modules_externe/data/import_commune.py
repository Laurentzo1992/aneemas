from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url
from django.http import JsonResponse
from paramettre.models import Regions, Provinces, Communes
import json


def commune(request):
    
    data = [
    {
        "nomcom": "bagassi",
        "nom": "BAGASSI",
        "province_id": "1"
    },
    {
        "nomcom": "banna",
        "nom": "BANA",
        "province_id": "1"
    },
    {
        "nomcom": "boromo",
        "nom": "BOROMO",
        "province_id": "1"
    },
    {
        "nomcom": "fara",
        "nom": "FARA",
        "province_id": "1"
    },
    {
        "nomcom": "pa",
        "nom": "P\u00c2",
        "province_id": "1"
    },
    {
        "nomcom": "poura",
        "nom": "POURA",
        "province_id": "1"
    },
    {
        "nomcom": "pompoi",
        "nom": "POMPO\u00cf",
        "province_id": "1"
    },
    {
        "nomcom": "biby",
        "nom": " SIBY",
        "province_id": "1"
    },
    {
        "nomcom": "yaho",
        "nom": "YAHO",
        "province_id": "1"
    },
    {
        "nomcom": "ouriry",
        "nom": "OURY",
        "province_id": "1"
    },
    {
        "nomcom": "balave",
        "nom": "BALAVE",
        "province_id": "1"
    },
    {
        "nomcom": "kouka",
        "nom": "KOUKA",
        "province_id": "1"
    },
    {
        "nomcom": "sanaba",
        "nom": "SANABA",
        "province_id": "1"
    },
    {
        "nomcom": "sami",
        "nom": "SAMI",
        "province_id": "1"
    },
    {
        "nomcom": "solenzo",
        "nom": "SOLENZO",
        "province_id": "1"
    },
    {
        "nomcom": "tansila",
        "nom": "TANSILA",
        "province_id": "1"
    },
    {
        "nomcom": "barani",
        "nom": "BARANI",
        "province_id": "1"
    },
    {
        "nomcom": "bomborokuy",
        "nom": "BOMBOROKUY",
        "province_id": "1"
    },
    {
        "nomcom": "bourasso",
        "nom": "BOURASSO",
        "province_id": "1"
    },
    {
        "nomcom": "djibasso",
        "nom": "DJIBASSO",
        "province_id": "1"
    },
    {
        "nomcom": "dokuy",
        "nom": "DOKUY",
        "province_id": "1"
    },
    {
        "nomcom": "doumbala",
        "nom": "DOUMBALA",
        "province_id": "1"
    },
    {
        "nomcom": "kombori",
        "nom": "KOMBORI",
        "province_id": "1"
    },
    {
        "nomcom": "madouba",
        "nom": "MADOUBA",
        "province_id": "1"
    },
    {
        "nomcom": "nouna",
        "nom": "NOUNA",
        "province_id": "1"
    },
    {
        "nomcom": "sono",
        "nom": "SONO",
        "province_id": "1"
    },
    {
        "nomcom": "bondoukuy",
        "nom": "BONDOUKUY",
        "province_id": "1"
    },
    {
        "nomcom": "dedougou",
        "nom": "DEDOUGOU",
        "province_id": "1"
    },
    {
        "nomcom": "douroula",
        "nom": "DOUROULA",
        "province_id": "1"
    },
    {
        "nomcom": "kona",
        "nom": "KONA",
        "province_id": "1"
    },
    {
        "nomcom": "ouarkoye",
        "nom": "OUARKOYE",
        "province_id": "1"
    },
    {
        "nomcom": "safane",
        "nom": "SAFANE",
        "province_id": "1"
    },
    {
        "nomcom": "tcheriba",
        "nom": "TCHERIBA",
        "province_id": "1"
    },
    {
        "nomcom": "gassan",
        "nom": "GASSAN",
        "province_id": "1"
    },
    {
        "nomcom": "gossina",
        "nom": "GOSSINA",
        "province_id": "1"
    },
    {
        "nomcom": "kougny",
        "nom": "KOUGNY",
        "province_id": "1"
    },
    {
        "nomcom": "toma",
        "nom": "TOMA",
        "province_id": "1"
    },
    {
        "nomcom": "yaba",
        "nom": "YABA",
        "province_id": "1"
    },
    {
        "nomcom": "ye",
        "nom": "YE",
        "province_id": "1"
    },
    {
        "nomcom": "di",
        "nom": "DI",
        "province_id": "1"
    },
    {
        "nomcom": "gomboro",
        "nom": "GOMBORO",
        "province_id": "1"
    },
    {
        "nomcom": "kassoum",
        "nom": "KASSOUM",
        "province_id": "1"
    },
    {
        "nomcom": "kiembara",
        "nom": "KIEMBARA",
        "province_id": "1"
    },
    {
        "nomcom": "lanfiera",
        "nom": "LANFIERA",
        "province_id": "1"
    },
    {
        "nomcom": "lankkoe",
        "nom": "LANKOE",
        "province_id": "1"
    },
    {
        "nomcom": "toeni",
        "nom": "TOENI",
        "province_id": "1"
    },
    {
        "nomcom": "tougan",
        "nom": "TOUGAN",
        "province_id": "1"
    },
    {
        "nomcom": "banfora",
        "nom": "BANFORA",
        "province_id": "2"
    },
    {
        "nomcom": "beregadougou",
        "nom": "BEREGADOUGOU",
        "province_id": "2"
    },
    {
        "nomcom": "mangodara",
        "nom": "MANGODARA",
        "province_id": "2"
    },
    {
        "nomcom": "moussoddougou",
        "nom": "MOUSSODOUGOU",
        "province_id": "2"
    },
    {
        "nomcom": "niangoloko",
        "nom": "NIANGOLOKO",
        "province_id": "2"
    },
    {
        "nomcom": "ouo",
        "nom": "OUO",
        "province_id": "2"
    },
    {
        "nomcom": "sideradougou",
        "nom": "SIDERADOUGOU",
        "province_id": "2"
    },
    {
        "nomcom": "soubaka",
        "nom": "SOUBAKA",
        "province_id": "2"
    },
    {
        "nomcom": "tiefora",
        "nom": "TIEFORA",
        "province_id": "2"
    },
    {
        "nomcom": "dakoro",
        "nom": "DAKORO",
        "province_id": "2"
    },
    {
        "nomcom": "douna",
        "nom": "DOUNA",
        "province_id": "2"
    },
    {
        "nomcom": "kankalaba",
        "nom": "KANKALABA",
        "province_id": "2"
    },
    {
        "nomcom": "loumana",
        "nom": "LOUMANA",
        "province_id": "2"
    },
    {
        "nomcom": "niankorodougou",
        "nom": "NIANKORODOUGOU",
        "province_id": "2"
    },
    {
        "nomcom": "oueleni",
        "nom": "OUELENI",
        "province_id": "2"
    },
    {
        "nomcom": "sind",
        "nom": "SINDOU",
        "province_id": "2"
    },
    {
        "nomcom": "wolokonto",
        "nom": "WOLOKONTO",
        "province_id": "2"
    },
    {
        "nomcom": "komki",
        "nom": "KOMKI IPALA",
        "province_id": "3"
    },
    {
        "nomcom": "komsilga",
        "nom": "KOMSILGA",
        "province_id": "3"
    },
    {
        "nomcom": "koubri",
        "nom": "KOUBRI",
        "province_id": "3"
    },
    {
        "nomcom": "ouagadoudougou",
        "nom": "OUAGADOUGOU",
        "province_id": "3"
    },
    {
        "nomcom": "pabre",
        "nom": "PABRE",
        "province_id": "3"
    },
    {
        "nomcom": "saaba",
        "nom": "SAABA",
        "province_id": "3"
    },
    {
        "nomcom": "tanghin",
        "nom": "TANGHIN DASSOURI",
        "province_id": "3"
    },
    {
        "nomcom": "bagre",
        "nom": "BAGRE",
        "province_id": "4"
    },
    {
        "nomcom": "bane",
        "nom": "BANE",
        "province_id": "4"
    },
    {
        "nomcom": "beguedo",
        "nom": "BEGUEDO",
        "province_id": "4"
    },
    {
        "nomcom": "bissiga",
        "nom": "BISSIGA",
        "province_id": "4"
    },
    {
        "nomcom": "bittou",
        "nom": "BITTOU",
        "province_id": "4"
    },
    {
        "nomcom": "boussoum",
        "nom": "BOUSSOUMA",
        "province_id": "4"
    },
    {
        "nomcom": "garango",
        "nom": "GARANGO",
        "province_id": "4"
    },
    {
        "nomcom": "komtoega",
        "nom": "KOMTOEGA",
        "province_id": "4"
    },
    {
        "nomcom": "niaogho",
        "nom": "NIAOGHO",
        "province_id": "4"
    },
    {
        "nomcom": "tenkodogo",
        "nom": "TENKODOGO",
        "province_id": "4"
    },
    {
        "nomcom": "zabre",
        "nom": "ZABRE",
        "province_id": "4"
    },
    {
        "nomcom": "zoaga",
        "nom": "ZOAGA",
        "province_id": "4"
    },
    {
        "nomcom": "comin",
        "nom": "COMIN YANGA",
        "province_id": "4"
    },
    {
        "nomcom": "dourtenga",
        "nom": "DOURTENGA",
        "province_id": "4"
    },
    {
        "nomcom": "ouargaye",
        "nom": "OUARGAYE",
        "province_id": "4"
    },
    {
        "nomcom": "sangha",
        "nom": "SANGHA",
        "province_id": "4"
    },
    {
        "nomcom": "soudougui",
        "nom": "SOUDOUGUI",
        "province_id": "4"
    },
    {
        "nomcom": "yargatenga",
        "nom": "YARGATENGA",
        "province_id": "4"
    },
    {
        "nomcom": "andemtenga",
        "nom": "ANDEMTENGA",
        "province_id": "4"
    },
    {
        "nomcom": "baskoure",
        "nom": "BASKOURE",
        "province_id": "4"
    },
    {
        "nomcom": "dialgaye",
        "nom": "DIALGAYE",
        "province_id": "4"
    },
    {
        "nomcom": "goughin",
        "nom": "GOUNGHIN",
        "province_id": "4"
    },
    {
        "nomcom": "kando",
        "nom": "KANDO",
        "province_id": "4"
    },
    {
        "nomcom": "koupela",
        "nom": "KOUPELA",
        "province_id": "4"
    },
    {
        "nomcom": "pouytenga",
        "nom": "POUYTENGA",
        "province_id": "4"
    },
    {
        "nomcom": "tensobentenga",
        "nom": "TENSOBENTENGA",
        "province_id": "4"
    },
    {
        "nomcom": "yargo",
        "nom": "YARGO",
        "province_id": "4"
    },
    {
        "nomcom": "bourzanga",
        "nom": "BOURZANGA",
        "province_id": "5"
    },
    {
        "nomcom": "guibare",
        "nom": "GUIBARE",
        "province_id": "5"
    },
    {
        "nomcom": "kougoussi",
        "nom": "KONGOUSSI",
        "province_id": "5"
    },
    {
        "nomcom": "nassere",
        "nom": "NASSERE",
        "province_id": "5"
    },
    {
        "nomcom": "rollo",
        "nom": "ROLLO",
        "province_id": "5"
    },
    {
        "nomcom": "rouko",
        "nom": "ROUKO",
        "province_id": "5"
    },
    {
        "nomcom": "sabce",
        "nom": "SABCE",
        "province_id": "5"
    },
    {
        "nomcom": "tikare",
        "nom": "TIKARE",
        "province_id": "5"
    },
    {
        "nomcom": "zimtenga",
        "nom": "ZIMTENGA",
        "province_id": "5"
    },
    {
        "nomcom": "boala",
        "nom": "BOALA",
        "province_id": "5"
    },
    {
        "nomcom": "boulsa",
        "nom": "BOULSA",
        "province_id": "5"
    },
    {
        "nomcom": "bouroum",
        "nom": "BOUROUM",
        "province_id": "5"
    },
    {
        "nomcom": "dargo",
        "nom": "DARGO",
        "province_id": "5"
    },
    {
        "nomcom": "nagbingou",
        "nom": "NAGBINGOU",
        "province_id": "5"
    },
    {
        "nomcom": "tougouri",
        "nom": "TOUGOURI",
        "province_id": "5"
    },
    {
        "nomcom": "yalgo",
        "nom": "YALGO",
        "province_id": "5"
    },
    {
        "nomcom": "zeguedeguin",
        "nom": "ZEGUEDEGUIN",
        "province_id": "5"
    },
    {
        "nomcom": "barsalogho",
        "nom": "BARSALOGHO",
        "province_id": "5"
    },
    {
        "nomcom": "boussouma",
        "nom": "BOUSSOUMA",
        "province_id": "5"
    },
    {
        "nomcom": "dablo",
        "nom": "DABLO",
        "province_id": "5"
    },
    {
        "nomcom": "kaya",
        "nom": "KAYA",
        "province_id": "5"
    },
    {
        "nomcom": "korsimoro",
        "nom": "KORSIMORO",
        "province_id": "5"
    },
    {
        "nomcom": "mane",
        "nom": "MANE",
        "province_id": "5"
    },
    {
        "nomcom": "namissiguima",
        "nom": "NAMISSIGUIMA",
        "province_id": "5"
    },
    {
        "nomcom": "pensa",
        "nom": "PENSA",
        "province_id": "5"
    },
    {
        "nomcom": "pibaore",
        "nom": "PIBAORE",
        "province_id": "5"
    },
    {
        "nomcom": "pissila",
        "nom": "PISSILA",
        "province_id": "5"
    },
    {
        "nomcom": "zila",
        "nom": "ZIGA",
        "province_id": "5"
    },
    {
        "nomcom": "bingo",
        "nom": "BINGO",
        "province_id": "6"
    },
    {
        "nomcom": "imasgo",
        "nom": "IMASGO",
        "province_id": "6"
    },
    {
        "nomcom": "kindi",
        "nom": "KINDI",
        "province_id": "6"
    },
    {
        "nomcom": "kokologho",
        "nom": "KOKOLOGHO",
        "province_id": "6"
    },
    {
        "nomcom": "koudougou",
        "nom": "KOUDOUGOU",
        "province_id": "6"
    },
    {
        "nomcom": "sigle",
        "nom": "SIGLE",
        "province_id": "6"
    },
    {
        "nomcom": "soaw",
        "nom": "SOAW",
        "province_id": "6"
    },
    {
        "nomcom": "sourgou",
        "nom": "SOURGOU",
        "province_id": "6"
    },
    {
        "nomcom": "thyou",
        "nom": "THYOU",
        "province_id": "6"
    },
    {
        "nomcom": "dassa",
        "nom": "DASSA",
        "province_id": "6"
    },
    {
        "nomcom": "didyr",
        "nom": "DIDYR",
        "province_id": "6"
    },
    {
        "nomcom": "godyr",
        "nom": "GODYR",
        "province_id": "6"
    },
    {
        "nomcom": "kordie",
        "nom": "KORDIE",
        "province_id": "6"
    },
    {
        "nomcom": "kyon",
        "nom": "KYON",
        "province_id": "6"
    },
    {
        "nomcom": "pouni",
        "nom": "POUNI",
        "province_id": "6"
    },
    {
        "nomcom": "reo",
        "nom": "REO",
        "province_id": "6"
    },
    {
        "nomcom": "tenado",
        "nom": "TENADO",
        "province_id": "6"
    },
    {
        "nomcom": "zamo",
        "nom": "ZAMO",
        "province_id": "6"
    },
    {
        "nomcom": "zawara",
        "nom": "ZAWARA",
        "province_id": "6"
    },
    {
        "nomcom": "bieha",
        "nom": "BIEHA",
        "province_id": "6"
    },
    {
        "nomcom": "bouras",
        "nom": "BOURA",
        "province_id": "6"
    },
    {
        "nomcom": "leo",
        "nom": "LEO",
        "province_id": "6"
    },
    {
        "nomcom": "nebielianayou",
        "nom": "NEBIELIANAYOU",
        "province_id": "6"
    },
    {
        "nomcom": "niabouri",
        "nom": "NIABOURI",
        "province_id": "6"
    },
    {
        "nomcom": "silly",
        "nom": "SILLY",
        "province_id": "6"
    },
    {
        "nomcom": "to",
        "nom": "T\u00d6",
        "province_id": "6"
    },
    {
        "nomcom": "bakata",
        "nom": "BAKATA",
        "province_id": "6"
    },
    {
        "nomcom": "bougnounou",
        "nom": "BOUGNOUNOU",
        "province_id": "6"
    },
    {
        "nomcom": "cassou",
        "nom": "CASSOU",
        "province_id": "6"
    },
    {
        "nomcom": "dalo",
        "nom": "DALO",
        "province_id": "6"
    },
    {
        "nomcom": "sapouy",
        "nom": "SAPOUY",
        "province_id": "6"
    },
    {
        "nomcom": "doulougou",
        "nom": "DOULOUGOU",
        "province_id": "7"
    },
    {
        "nomcom": "gaongo",
        "nom": "GAONGO",
        "province_id": "7"
    },
    {
        "nomcom": "ipelce",
        "nom": "IPELCE",
        "province_id": "7"
    },
    {
        "nomcom": "kayao",
        "nom": "KAYAO",
        "province_id": "7"
    },
    {
        "nomcom": "kombissiri",
        "nom": "KOMBISSIRI",
        "province_id": "7"
    },
    {
        "nomcom": "sapone",
        "nom": "SAPONE",
        "province_id": "7"
    },
    {
        "nomcom": "toece",
        "nom": "TOECE",
        "province_id": "7"
    },
    {
        "nomcom": "guiaro",
        "nom": "GUIARO",
        "province_id": "7"
    },
    {
        "nomcom": "po",
        "nom": "PO",
        "province_id": "7"
    },
    {
        "nomcom": "tiebele",
        "nom": "TIEBELE",
        "province_id": "7"
    },
    {
        "nomcom": "ziou",
        "nom": "ZIOU",
        "province_id": "7"
    },
    {
        "nomcom": "bere",
        "nom": "BERE",
        "province_id": "7"
    },
    {
        "nomcom": "gogo",
        "nom": "GOGO",
        "province_id": "7"
    },
    {
        "nomcom": "gon_boussougou",
        "nom": "GON-BOUSSOUGOU",
        "province_id": "7"
    },
    {
        "nomcom": "manga",
        "nom": "MANGA",
        "province_id": "7"
    },
    {
        "nomcom": "bilanga",
        "nom": "BILANGA",
        "province_id": "8"
    },
    {
        "nomcom": "bogande",
        "nom": "BOGANDE",
        "province_id": "8"
    },
    {
        "nomcom": "coalla",
        "nom": "COALLA",
        "province_id": "8"
    },
    {
        "nomcom": "liptougou",
        "nom": "LIPTOUGOU",
        "province_id": "8"
    },
    {
        "nomcom": "manni",
        "nom": "MANNI",
        "province_id": "8"
    },
    {
        "nomcom": "piela",
        "nom": "PIELA",
        "province_id": "8"
    },
    {
        "nomcom": "thion",
        "nom": "THION",
        "province_id": "8"
    },
    {
        "nomcom": "diabo",
        "nom": "DIABO",
        "province_id": "8"
    },
    {
        "nomcom": "diapangou",
        "nom": "DIAPANGOU",
        "province_id": "8"
    },
    {
        "nomcom": "fada_ngourma",
        "nom": "FADA N'GOURMA",
        "province_id": "8"
    },
    {
        "nomcom": "matiacoali",
        "nom": "MATIACOALI",
        "province_id": "8"
    },
    {
        "nomcom": "tibga",
        "nom": "TIBGA",
        "province_id": "8"
    },
    {
        "nomcom": "yamba",
        "nom": "YAMBA",
        "province_id": "8"
    },
    {
        "nomcom": "bartiebougou",
        "nom": "BARTIEBOUGOU",
        "province_id": "8"
    },
    {
        "nomcom": "foutou",
        "nom": "FOUTOURI",
        "province_id": "8"
    },
    {
        "nomcom": "gayeri",
        "nom": "GAYERI",
        "province_id": "8"
    },
    {
        "nomcom": "diabiga",
        "nom": "DIABIGA",
        "province_id": "8"
    },
    {
        "nomcom": "pognoa",
        "nom": "POGNOA TIKONTI",
        "province_id": "8"
    },
    {
        "nomcom": "kompieng",
        "nom": "KOMPIENGA",
        "province_id": "8"
    },
    {
        "nomcom": "nadiagou",
        "nom": "NADIAGOU",
        "province_id": "8"
    },
    {
        "nomcom": "sankoado",
        "nom": "POGNOA SANKOADO",
        "province_id": "8"
    },
    {
        "nomcom": "tambarga",
        "nom": "TAMBARGA",
        "province_id": "8"
    },
    {
        "nomcom": "madjoari",
        "nom": "MADJOARI",
        "province_id": "8"
    },
    {
        "nomcom": "pama",
        "nom": "PAMA",
        "province_id": "8"
    },
    {
        "nomcom": "koalou",
        "nom": " DE KOALOU",
        "province_id": "8"
    },
    {
        "nomcom": "kompienbiga",
        "nom": "KOMPIENBIGA",
        "province_id": "8"
    },
    {
        "nomcom": "boutou",
        "nom": "BOTOU",
        "province_id": "8"
    },
    {
        "nomcom": "diapaga",
        "nom": "DIAPAGA",
        "province_id": "8"
    },
    {
        "nomcom": "kantchari",
        "nom": "KANTCHARI",
        "province_id": "8"
    },
    {
        "nomcom": "logobou",
        "nom": "LOGOBOU",
        "province_id": "8"
    },
    {
        "nomcom": "namounou",
        "nom": "NAMOUNOU",
        "province_id": "8"
    },
    {
        "nomcom": "partiaga",
        "nom": "PARTIAGA",
        "province_id": "8"
    },
    {
        "nomcom": "tansarga",
        "nom": "TANSARGA",
        "province_id": "8"
    },
    {
        "nomcom": "bama",
        "nom": "BAMA",
        "province_id": "9"
    },
    {
        "nomcom": "bobo",
        "nom": "BOBO-DIOULASSO",
        "province_id": "9"
    },
    {
        "nomcom": "dande",
        "nom": "DANDE",
        "province_id": "9"
    },
    {
        "nomcom": "faramana",
        "nom": "FARAMANA",
        "province_id": "9"
    },
    {
        "nomcom": "foutouri",
        "nom": "F\u00d6",
        "province_id": "9"
    },
    {
        "nomcom": "karangasso",
        "nom": "KARANGASSO-SAMBLA",
        "province_id": "9"
    },
    {
        "nomcom": "vigue",
        "nom": "KARANGASSO-VIGUE",
        "province_id": "9"
    },
    {
        "nomcom": "koundougou",
        "nom": "KOUNDOUGOU",
        "province_id": "9"
    },
    {
        "nomcom": "lena",
        "nom": "LENA",
        "province_id": "9"
    },
    {
        "nomcom": "padema",
        "nom": "PADEMA",
        "province_id": "9"
    },
    {
        "nomcom": "peni",
        "nom": "PENI",
        "province_id": "9"
    },
    {
        "nomcom": "satiri",
        "nom": "SATIRI",
        "province_id": "9"
    },
    {
        "nomcom": "toussiana",
        "nom": "TOUSSIANA",
        "province_id": "9"
    },
    {
        "nomcom": "banzou",
        "nom": "BANZON",
        "province_id": "9"
    },
    {
        "nomcom": "djigouera",
        "nom": "DJIGOUERA",
        "province_id": "9"
    },
    {
        "nomcom": "kangala",
        "nom": "KANGALA",
        "province_id": "9"
    },
    {
        "nomcom": "kologo",
        "nom": "KOLOKO",
        "province_id": "9"
    },
    {
        "nomcom": "kourinion",
        "nom": "KOURINION",
        "province_id": "9"
    },
    {
        "nomcom": "kourouma",
        "nom": "KOUROUMA",
        "province_id": "9"
    },
    {
        "nomcom": "morolaba",
        "nom": "MOROLABA",
        "province_id": "9"
    },
    {
        "nomcom": "ndorola",
        "nom": "N'DOROLA",
        "province_id": "9"
    },
    {
        "nomcom": "orodara",
        "nom": "ORODARA",
        "province_id": "9"
    },
    {
        "nomcom": "samogohiri",
        "nom": "SAMOGOHIRI",
        "province_id": "9"
    },
    {
        "nomcom": "samorogouan",
        "nom": "SAMOROGOUAN",
        "province_id": "9"
    },
    {
        "nomcom": "sindou",
        "nom": "SINDO",
        "province_id": "9"
    },
    {
        "nomcom": "bekuy",
        "nom": "BEKUY",
        "province_id": "9"
    },
    {
        "nomcom": "bereba",
        "nom": "BEREBA",
        "province_id": "9"
    },
    {
        "nomcom": "boni",
        "nom": "BONI",
        "province_id": "9"
    },
    {
        "nomcom": "founzan",
        "nom": "FOUNZAN",
        "province_id": "9"
    },
    {
        "nomcom": "hounde",
        "nom": "HOUNDE",
        "province_id": "9"
    },
    {
        "nomcom": "kotti",
        "nom": "KOTI",
        "province_id": "9"
    },
    {
        "nomcom": "koumbia",
        "nom": "KOUMBIA",
        "province_id": "9"
    },
    {
        "nomcom": "banh",
        "nom": "BANH",
        "province_id": "10"
    },
    {
        "nomcom": "ouindigui",
        "nom": "OUINDIGUI",
        "province_id": "10"
    },
    {
        "nomcom": "solle",
        "nom": "SOLLE",
        "province_id": "10"
    },
    {
        "nomcom": "tittao",
        "nom": "TITAO",
        "province_id": "10"
    },
    {
        "nomcom": "arbole",
        "nom": "ARBOLE",
        "province_id": "10"
    },
    {
        "nomcom": "bagare",
        "nom": "BAGARE",
        "province_id": "10"
    },
    {
        "nomcom": "bokin",
        "nom": "BOKIN",
        "province_id": "10"
    },
    {
        "nomcom": "gomponsom",
        "nom": "GOMPONSOM",
        "province_id": "10"
    },
    {
        "nomcom": "kirsi",
        "nom": "KIRSI",
        "province_id": "10"
    },
    {
        "nomcom": "latoden",
        "nom": "LA-TODEN",
        "province_id": "10"
    },
    {
        "nomcom": "pilimpikou",
        "nom": "PILIMPIKOU",
        "province_id": "10"
    },
    {
        "nomcom": "samba",
        "nom": "SAMBA",
        "province_id": "10"
    },
    {
        "nomcom": "yako",
        "nom": "YAKO",
        "province_id": "10"
    },
    {
        "nomcom": "barga",
        "nom": "BARGA",
        "province_id": "10"
    },
    {
        "nomcom": "kalsaka",
        "nom": "KALSAKA",
        "province_id": "10"
    },
    {
        "nomcom": "kossouka",
        "nom": "KOSSOUKA",
        "province_id": "10"
    },
    {
        "nomcom": "koumbri",
        "nom": "KOUMBRI",
        "province_id": "10"
    },
    {
        "nomcom": "namissiguim",
        "nom": "NAMISSIGUIMA",
        "province_id": "10"
    },
    {
        "nomcom": "ouahigouya",
        "nom": "OUAHIGOUYA",
        "province_id": "10"
    },
    {
        "nomcom": "oula",
        "nom": "OULA",
        "province_id": "10"
    },
    {
        "nomcom": "rambo",
        "nom": "RAMBO",
        "province_id": "10"
    },
    {
        "nomcom": "seguenega",
        "nom": "SEGUENEGA",
        "province_id": "10"
    },
    {
        "nomcom": "tangaye",
        "nom": "TANGAYE",
        "province_id": "10"
    },
    {
        "nomcom": "thiou",
        "nom": "THIOU",
        "province_id": "10"
    },
    {
        "nomcom": "zogore",
        "nom": "ZOGORE",
        "province_id": "10"
    },
    {
        "nomcom": "bassi",
        "nom": "BASSI",
        "province_id": "10"
    },
    {
        "nomcom": "boussou",
        "nom": "BOUSSOU",
        "province_id": "10"
    },
    {
        "nomcom": "gourcy",
        "nom": "GOURCY",
        "province_id": "10"
    },
    {
        "nomcom": "leba",
        "nom": "LEBA",
        "province_id": "10"
    },
    {
        "nomcom": "tougou",
        "nom": "TOUGO",
        "province_id": "10"
    },
    {
        "nomcom": "boudry",
        "nom": "BOUDRY",
        "province_id": "11"
    },
    {
        "nomcom": "kogo",
        "nom": "KOGO",
        "province_id": "11"
    },
    {
        "nomcom": "meguet",
        "nom": "MEGUET",
        "province_id": "11"
    },
    {
        "nomcom": "mogtedo",
        "nom": "MOGTEDO",
        "province_id": "11"
    },
    {
        "nomcom": "salogo",
        "nom": "SALOGO",
        "province_id": "11"
    },
    {
        "nomcom": "zam",
        "nom": "ZAM",
        "province_id": "11"
    },
    {
        "nomcom": "zorgho",
        "nom": "ZORGHO",
        "province_id": "11"
    },
    {
        "nomcom": "zoungou",
        "nom": "ZOUNGOU",
        "province_id": "11"
    },
    {
        "nomcom": "bousse",
        "nom": "BOUSSE",
        "province_id": "11"
    },
    {
        "nomcom": "laye",
        "nom": "LAYE",
        "province_id": "11"
    },
    {
        "nomcom": "niou",
        "nom": "NIOU",
        "province_id": "11"
    },
    {
        "nomcom": "sourgoubila",
        "nom": "SOURGOUBILA",
        "province_id": "11"
    },
    {
        "nomcom": "toeghin",
        "nom": "TOEGHIN",
        "province_id": "11"
    },
    {
        "nomcom": "absouya",
        "nom": "ABSOUYA",
        "province_id": "11"
    },
    {
        "nomcom": "dapelogo",
        "nom": "DAPELOGO",
        "province_id": "11"
    },
    {
        "nomcom": "loumbila",
        "nom": "LOUMBILA",
        "province_id": "11"
    },
    {
        "nomcom": "nagrengo",
        "nom": "NAGRENGO",
        "province_id": "11"
    },
    {
        "nomcom": "ourgoumanega",
        "nom": "OURGOU-MANEGA",
        "province_id": "11"
    },
    {
        "nomcom": "ziniar",
        "nom": "ZINIARE",
        "province_id": "11"
    },
    {
        "nomcom": "zitenga",
        "nom": "ZITENGA",
        "province_id": "11"
    },
    {
        "nomcom": "deou",
        "nom": "DEOU",
        "province_id": "12"
    },
    {
        "nomcom": "goromgorom",
        "nom": "GOROM-GOROM",
        "province_id": "12"
    },
    {
        "nomcom": "markoye",
        "nom": "MARKOYE",
        "province_id": "12"
    },
    {
        "nomcom": "oursi",
        "nom": "OURSI",
        "province_id": "12"
    },
    {
        "nomcom": "tinakoff",
        "nom": "TIN-AKOFF",
        "province_id": "12"
    },
    {
        "nomcom": "bani",
        "nom": "BANI",
        "province_id": "12"
    },
    {
        "nomcom": "dor",
        "nom": "DORI",
        "province_id": "12"
    },
    {
        "nomcom": "falagountou",
        "nom": "FALAGOUNTOU",
        "province_id": "12"
    },
    {
        "nomcom": "gorgadji",
        "nom": "GORGADJI",
        "province_id": "12"
    },
    {
        "nomcom": "sampelga",
        "nom": "SAMPELGA",
        "province_id": "12"
    },
    {
        "nomcom": "seytenga",
        "nom": "SEYTENGA",
        "province_id": "12"
    },
    {
        "nomcom": "aribinda",
        "nom": "ARIBINDA",
        "province_id": "12"
    },
    {
        "nomcom": "baraboule",
        "nom": "BARABOULE",
        "province_id": "12"
    },
    {
        "nomcom": "djibo",
        "nom": "DJIBO",
        "province_id": "12"
    },
    {
        "nomcom": "kelbo",
        "nom": "KELBO",
        "province_id": "12"
    },
    {
        "nomcom": "nassoumbou",
        "nom": "NASSOUMBOU",
        "province_id": "12"
    },
    {
        "nomcom": "pobemengao",
        "nom": "POBE MENGAO",
        "province_id": "12"
    },
    {
        "nomcom": "tongomael",
        "nom": "TONGOMAEL",
        "province_id": "12"
    },
    {
        "nomcom": "boundore",
        "nom": "BOUNDORE",
        "province_id": "12"
    },
    {
        "nomcom": "mansila",
        "nom": "MANSILA",
        "province_id": "12"
    },
    {
        "nomcom": "sebba",
        "nom": "SEBBA",
        "province_id": "12"
    },
    {
        "nomcom": "solhan",
        "nom": "SOLHAN",
        "province_id": "12"
    },
    {
        "nomcom": "tankougounadie",
        "nom": "TANKOUGOUNADIE",
        "province_id": "12"
    },
    {
        "nomcom": "titabe",
        "nom": "TITABE",
        "province_id": "12"
    },
    {
        "nomcom": "bondigui",
        "nom": "BONDIGUI",
        "province_id": "13"
    },
    {
        "nomcom": "diebougou",
        "nom": "DIEBOUGOU",
        "province_id": "13"
    },
    {
        "nomcom": "dolo",
        "nom": "DOLO",
        "province_id": "13"
    },
    {
        "nomcom": "iolonioro",
        "nom": "IOLONIORO",
        "province_id": "13"
    },
    {
        "nomcom": "tiankoura",
        "nom": "TIANKOURA",
        "province_id": "13"
    },
    {
        "nomcom": "dano",
        "nom": "DANO",
        "province_id": "13"
    },
    {
        "nomcom": "dissin",
        "nom": "DISSIN",
        "province_id": "13"
    },
    {
        "nomcom": "gueguere",
        "nom": "GUEGUERE",
        "province_id": "13"
    },
    {
        "nomcom": "koper",
        "nom": "KOPER",
        "province_id": "13"
    },
    {
        "nomcom": "niego",
        "nom": "NIEGO",
        "province_id": "13"
    },
    {
        "nomcom": "oronkua",
        "nom": "ORONKUA",
        "province_id": "13"
    },
    {
        "nomcom": "ouessa",
        "nom": "OUESSA",
        "province_id": "13"
    },
    {
        "nomcom": "zambo",
        "nom": "ZAMBO",
        "province_id": "13"
    },
    {
        "nomcom": "batie",
        "nom": "BATIE",
        "province_id": "13"
    },
    {
        "nomcom": "boussoukoula",
        "nom": "BOUSSOUKOULA",
        "province_id": "13"
    },
    {
        "nomcom": "kpere",
        "nom": "KPERE",
        "province_id": "13"
    },
    {
        "nomcom": "legmoin",
        "nom": "LEGMOIN",
        "province_id": "13"
    },
    {
        "nomcom": "midebdo",
        "nom": "MIDEBDO",
        "province_id": "13"
    },
    {
        "nomcom": "bouroumbouroum",
        "nom": "BOUROUM-BOUROUM",
        "province_id": "13"
    },
    {
        "nomcom": "boussera",
        "nom": "BOUSSERA",
        "province_id": "13"
    },
    {
        "nomcom": "djigoue",
        "nom": "DJIGOUE",
        "province_id": "13"
    },
    {
        "nomcom": "gaou",
        "nom": "GAOUA",
        "province_id": "13"
    },
    {
        "nomcom": "gbomblora",
        "nom": "GBOMBLORA",
        "province_id": "13"
    },
    {
        "nomcom": "kampti",
        "nom": "KAMPTI",
        "province_id": "13"
    },
    {
        "nomcom": "loropeni",
        "nom": "LOROPENI",
        "province_id": "13"
    },
    {
        "nomcom": "malba",
        "nom": "MALBA",
        "province_id": "13"
    },
    {
        "nomcom": "nako",
        "nom": "NAKO",
        "province_id": "13"
    },
    {
        "nomcom": "perigban",
        "nom": "PERIGBAN",
        "province_id": "13"
    }
]


    for item in data:
        province_id = int(item["province_id"])
        try:
            province = Provinces.objects.get(id=province_id)
        except Provinces.DoesNotExist:
            # Gérer le cas où la région n'existe pas
            continue

        commune = Communes(
            id_commune=item["nomcom"],
            commune=item["nom"],
            province_id=province,
        )
        commune.save()

    return JsonResponse({"message": "Données importées avec succès"})


