from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url
from django.http import JsonResponse
from paramettre.models import Regions, Provinces, Communes
import json



def import_provinces(request):

    data = [


{
    "id": "1",
    "numero": "01",
    "nomprov": "Balé",
    "region_id": "1",
    "created": "null",
    "modified": "2018-04-24 03:35:47"
},
{
    "id": "2",
    "numero": "03",
    "nomprov": "Banwa",
    "region_id": "1",
    "created": "null",
    "modified": "2018-04-24 03:36:07"
},
{
    "id": "3",
    "numero": "18",
    "nomprov": "Kossi",
    "region_id": "1",
    "created": "null",
    "modified": "2018-04-24 03:36:49"
},
{
    "id": "4",
    "numero": "24",
    "nomprov": "Mouhoun",
    "region_id": "1",
    "created": "null",
    "modified": "2018-04-24 03:37:16"
},
{
    "id": "5",
    "numero": "27",
    "nomprov": "Nayala",
    "region_id": "1",
    "created": "null",
    "modified": "2018-04-24 03:37:32"
},
{
    "id": "6",
    "numero": "38",
    "nomprov": "Sourou",
    "region_id": "1",
    "created": "null",
    "modified": "2018-04-24 03:38:12"
},
{
    "id": "7",
    "numero": "08",
    "nomprov": "Comoé",
    "region_id": "2",
    "created": "null",
    "modified": "2018-04-24 03:38:46"
},
{
    "id": "8",
    "numero": "22",
    "nomprov": "Léraba",
    "region_id": "2",
    "created": "null",
    "modified": "2018-04-24 03:39:11"
},
{
    "id": "9",
    "numero": "14",
    "nomprov": "Kadiogo",
    "region_id": "3",
    "created": "null",
    "modified": "2018-04-24 03:39:35"
},
{
    "id": "10",
    "numero": "06",
    "nomprov": "Boulgou",
    "region_id": "4",
    "created": "null",
    "modified": "2018-04-24 03:40:37"
},
{
    "id": "11",
    "numero": "19",
    "nomprov": "Koulpélogo",
    "region_id": "4",
    "created": "null",
    "modified": "2018-04-24 03:41:17"
},
{
    "id": "12",
    "numero": "20",
    "nomprov": "Kouritenga",
    "region_id": "4",
    "created": "null",
    "modified": "2018-04-24 03:41:37"
},
{
    "id": "13",
    "numero": "02",
    "nomprov": "Bam",
    "region_id": "5",
    "created": "null",
    "modified": "2018-05-13 14:11:44"
},
{
    "id": "14",
    "numero": "26",
    "nomprov": "Namentenga",
    "region_id": "5",
    "created": "null",
    "modified": "2018-04-24 03:42:32"
},
{
    "id": "15",
    "numero": "34",
    "nomprov": "Sanmatenga",
    "region_id": "5",
    "created": "null",
    "modified": "2018-04-24 03:43:43"
},
{
    "id": "16",
    "numero": "07",
    "nomprov": "Boulkiemdé",
    "region_id": "6",
    "created": "null",
    "modified": "2018-05-01 22:27:32"
},
{
    "id": "17",
    "numero": "33",
    "nomprov": "Sanguié",
    "region_id": "6",
    "created": "null",
    "modified": "2018-04-24 03:45:38"
},
{
    "id": "18",
    "numero": "36",
    "nomprov": "Sissili",
    "region_id": "6",
    "created": "null",
    "modified": "2018-04-24 03:46:24"
},
{
    "id": "19",
    "numero": "43",
    "nomprov": "Ziro",
    "region_id": "6",
    "created": "null",
    "modified": "2018-04-24 03:47:00"
},
{
    "id": "20",
    "numero": "04",
    "nomprov": "Bazèga",
    "region_id": "7",
    "created": "null",
    "modified": "2018-04-24 03:47:22"
},
{
    "id": "21",
    "numero": "25",
    "nomprov": "Nahouri",
    "region_id": "7",
    "created": "null",
    "modified": "2018-04-24 03:49:17"
},
{
    "id": "22",
    "numero": "45",
    "nomprov": "Zoundwéogo",
    "region_id": "7",
    "created": "null",
    "modified": "2019-05-06 13:26:41"
},
{
    "id": "23",
    "numero": "10",
    "nomprov": "Gnagna",
    "region_id": "8",
    "created": "null",
    "modified": "2018-04-24 03:50:47"
},
{
    "id": "24",
    "numero": "11",
    "nomprov": "Gourma",
    "region_id": "8",
    "created": "null",
    "modified": "2018-04-24 03:50:57"
},
{
    "id": "25",
    "numero": "16",
    "nomprov": "Komondjari",
    "region_id": "8",
    "created": "null",
    "modified": "2018-04-24 03:51:31"
},
{
    "id": "26",
    "numero": "17",
    "nomprov": "Kompienga",
    "region_id": "8",
    "created": "null",
    "modified": "2018-04-24 03:51:53"
},
{
    "id": "27",
    "numero": "39",
    "nomprov": "Tapoa",
    "region_id": "8",
    "created": "null",
    "modified": "2018-04-24 03:52:16"
},
{
    "id": "28",
    "numero": "12",
    "nomprov": "Houet",
    "region_id": "9",
    "created": "null",
    "modified": "2018-04-24 03:52:38"
},
{
    "id": "29",
    "numero": "15",
    "nomprov": "Kénédougou",
    "region_id": "9",
    "created": "null",
    "modified": "2018-04-24 03:53:02"
},
{
    "id": "30",
    "numero": "40",
    "nomprov": "Tuy",
    "region_id": "9",
    "created": "null",
    "modified": "2019-05-06 13:26:14"
},
{
    "id": "31",
    "numero": "23",
    "nomprov": "Loroum",
    "region_id": "10",
    "created": "null",
    "modified": "2018-04-24 03:54:08"
},
{
    "id": "32",
    "numero": "31",
    "nomprov": "Passoré",
    "region_id": "10",
    "created": "null",
    "modified": "2018-04-24 03:54:41"
},
{
    "id": "33",
    "numero": "42",
    "nomprov": "Yatenga",
    "region_id": "10",
    "created": "null",
    "modified": "2018-04-24 03:55:02"
},
{
    "id": "34",
    "numero": "44",
    "nomprov": "Zondoma",
    "region_id": "10",
    "created": "null",
    "modified": "2018-04-24 03:55:26"
},
{
    "id": "35",
    "numero": "09",
    "nomprov": "Ganzourgou",
    "region_id": "11",
    "created": "null",
    "modified": "2018-04-24 03:55:51"
},
{
    "id": "36",
    "numero": "21",
    "nomprov": "Kourwéogo",
    "region_id": "11",
    "created": "null",
    "modified": "2018-04-24 03:56:10"
},
{
    "id": "37",
    "numero": "29",
    "nomprov": "Oubritenga",
    "region_id": "11",
    "created": "null",
    "modified": "2018-04-24 03:56:29"
},
{
    "id": "38",
    "numero": "30",
    "nomprov": "Oudalan",
    "region_id": "12",
    "created": "null",
    "modified": "2018-04-24 03:56:51"
},
{
    "id": "39",
    "numero": "35",
    "nomprov": "Séno",
    "region_id": "12",
    "created": "null",
    "modified": "2018-04-24 03:57:15"
},
{
    "id": "40",
    "numero": "37",
    "nomprov": "Soum",
    "region_id": "12",
    "created": "null",
    "modified": "2018-04-24 03:57:34"
},
{
    "id": "41",
    "numero": "41",
    "nomprov": "Yagha",
    "region_id": "12",
    "created": "null",
    "modified": "2018-04-24 03:57:52"
},
{
    "id": "42",
    "numero": "05",
    "nomprov": "Bougouriba",
    "region_id": "13",
    "created": "null",
    "modified": "2018-04-24 03:58:13"
},
{
    "id": "43",
    "numero": "13",
    "nomprov": "Ioba",
    "region_id": "13",
    "created": "null",
    "modified": "2018-04-24 03:58:43"
},
{
    "id": "44",
    "numero": "28",
    "nomprov": "Noumbiel",
    "region_id": "13",
    "created": "null",
    "modified": "2018-04-24 03:59:04"
},
{
    "id": "45",
    "numero": "32",
    "nomprov": "Poni",
    "region_id": "13",
    "created": "null",
    "modified": "2018-04-24 03:59:20"
}
]
    for item in data:
        region_id = int(item["region_id"])
        try:
            region = Regions.objects.get(id=region_id)
        except Regions.DoesNotExist:
            # Gérer le cas où la région n'existe pas
            continue

        province = Provinces(
            numero=item["numero"],
            nomprov=item["nomprov"],
            region_id=region,
            created=item["created"],
            modified=item["modified"]
        )
        province.save()

    return JsonResponse({"message": "Données importées avec succès"})

