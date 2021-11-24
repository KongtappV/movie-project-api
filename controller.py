import sys
from flask import abort
import pymysql as mysql
from config import OPENAPI_AUTOGEN_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

sys.path.append(OPENAPI_AUTOGEN_DIR)
from openapi_server import models

db = mysql.connect(host=DB_HOST,
                   user=DB_USER,
                   passwd=DB_PASSWD,
                   db=DB_NAME)


def get_basins():
    cs = db.cursor()
    cs.execute("SELECT basin_id,ename FROM basin")
    result = [models.BasinShort(basin_id, name) for basin_id, name in cs.fetchall()]
    cs.close()
    return result


def get_basin_details(basin_id):
    cs = db.cursor()
    cs.execute("""
        SELECT basin_id, ename, area
        FROM basin
        WHERE basin_id=%s
        """, [basin_id])
    result = cs.fetchone()
    cs.close()
    if result:
        basin_id, name, area = result
        return models.BasinFull(basin_id, name, area)
    else:
        abort(404)


def get_stations(basin_id):
    cs = db.cursor()
    cs.execute("""
        SELECT station_id, s.ename
        FROM station s
        INNER JOIN basin b ON ST_CONTAINS(b.geometry, POINT(s.lon, s.lat))
        WHERE basin_id=%s
        """, [basin_id])
    result = [models.StationShort(station_id, name) for station_id, name in cs.fetchall()]
    cs.close()
    return result


def get_station_details(station_id):
    cs = db.cursor()
    cs.execute("""
    SELECT s.station_id, b.basin_id, s.ename, s.lat, s.lon
    FROM rainfall r
             INNER JOIN station s ON r.station_id = s.station_id # join rainfall and station
             INNER JOIN basin b ON ST_Contains(b.geometry, Point(s.lon, s.lat)) # Join the geometry and lat lon
    WHERE s.station_id = %s
    """, [station_id])
    result = cs.fetchone()
    cs.close()
    if result:
        station_id, basin_id, ename, lat, lon = result
        return models.StationFull(station_id, basin_id, ename, lat, lon)
    else:
        abort(404)

def get_basin_annual_rainfalls(basin_id, year):
    cs = db.cursor()
    cs.execute("""
    SELECT basin_id , year, AVG(annual_rainfall) as rainfall
    FROM (
    SELECT b.basin_id, r.year, SUM(r.amount) as annual_rainfall
    FROM rainfall r
            INNER JOIN station s ON r.station_id = s.station_id # join rainfall and station
            INNER JOIN basin b ON ST_Contains(b.geometry, Point(s.lon, s.lat)) # Join the geometry and lat lon
    WHERE b.basin_id=%s AND r.year=%s
    GROUP BY r.station_id, r.year
    )annual
    GROUP BY year
    """, [basin_id, year])
    result = cs.fetchone()
    cs.close()
    if result:
        basin_id, year, rainfall = result
        return models.BasinAnnualRainfalls(basin_id, year, rainfall)
    else:
        abort(404)
