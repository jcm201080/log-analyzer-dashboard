import os
import geoip2.database

# Rutas configurables por entorno
COUNTRY_DB = os.getenv(
    "GEOIP_COUNTRY_DB",
    "data/geoip/GeoLite2-Country.mmdb"
)

CITY_DB = os.getenv(
    "GEOIP_CITY_DB",
    "data/geoip/GeoLite2-City.mmdb"
)

_country_reader = None
_city_reader = None

# Inicializar readers SOLO si existen los ficheros
if os.path.exists(COUNTRY_DB):
    try:
        _country_reader = geoip2.database.Reader(COUNTRY_DB)
    except Exception:
        _country_reader = None

if os.path.exists(CITY_DB):
    try:
        _city_reader = geoip2.database.Reader(CITY_DB)
    except Exception:
        _city_reader = None


def get_geo_info(ip: str) -> dict:
    """
    Devuelve información geográfica de una IP:
    país, región y ciudad (si existe).
    Si no hay base GeoIP, devuelve valores 'Unknown'.
    """
    data = {
        "country": "Unknown",
        "region": "Unknown",
        "city": "Unknown"
    }

    if _country_reader:
        try:
            country_resp = _country_reader.country(ip)
            if country_resp.country.name:
                data["country"] = country_resp.country.name
        except Exception:
            pass

    if _city_reader:
        try:
            city_resp = _city_reader.city(ip)
            if city_resp.subdivisions.most_specific.name:
                data["region"] = city_resp.subdivisions.most_specific.name
            if city_resp.city.name:
                data["city"] = city_resp.city.name
        except Exception:
            pass

    return data
