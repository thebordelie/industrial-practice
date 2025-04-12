from typing import Optional

from model.establishment import Establishment
from repository.establishment_repository import DataProvider
import mariadb
import sys, os, json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class OpenSearch(DataProvider):
    def __init__(self, username: str, password: str, host: str, port: int, database: str):
        super().__init__(username, password, host, port, database)
        try:
            self.conn = mariadb.connect(
                user=username,
                password=password,
                host=host,
                port=port,
                database=database

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def get_data(self) -> list[Establishment]:
        cur = self.conn.cursor()

        cur.execute(
            f"""SELECT 
        twogisitemid,
        attributegroup.name,
        attributegroup.isprimary,
        attribute.name,
        items.name,
        coordinates.Latitude,
        coordinates.Longitude,
        addressname
        from twogisattributegrouptwogisattributegroupattribute 
        JOIN attribute ON 
        twogisattributegrouptwogisattributegroupattribute.Attributesid = attribute.id 
        JOIN attributegroup ON 
        twogisattributegrouptwogisattributegroupattribute.groupsid = attributegroup.id
        JOIN items ON 
        twogisitemid = items.id 
        JOIN coordinates ON items.PointId = coordinates.id
        ORDER BY items.id, isprimary desc, attributegroup.name;"""
        )

        array = []

        i = cur.next()

        obj = {
            'twogisitemid': i[0],
            'name': i[4],
            i[1]: [i[3]],
            'coordinates': [str(round(i[5], 6)), str(round(i[6], 6))],
            'addressname': i[7]
        }

        for i in cur:

            if i[0] != obj['twogisitemid']:
                array.append(obj)
                obj = {
                    'twogisitemid': i[0],
                    'name': i[4],
                    'coordinates': [str(round(i[5], 6)), str(round(i[6], 6))],
                    'addressname': i[7]
                }

            if obj.get(i[1]):
                obj[i[1]].append(i[3])
            else:
                obj[i[1]] = [i[3]]

        array.append(obj)

        with open(f'{ROOT_DIR}/data/twogis/final_data.json', 'w', encoding='utf-8') as f:
            json.dump(array, f, ensure_ascii=False)

        return []

    def add_data(self, establishment: Establishment):
        pass
