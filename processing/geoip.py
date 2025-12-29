import geoip2.database

COUNTRY_DB = "data/geoip/GeoLite2-Country.mmdb"
CITY_DB = "data/geoip/GeoLite2-City.mmdb"

_country_reader = geoip2.database.Reader(COUNTRY_DB)
_city_reader = geoip2.database.Reader(CITY_DB)

def get_geo_info(ip: str) -> dict:
    """
    Devuelve información geográfica de una IP:
    país, región y ciudad (si existe)
    """
    data = {
        "country": "Unknown",
        "region": "Unknown",
        "city": "Unknown"
    }

    try:
        country_resp = _country_reader.country(ip)
        if country_resp.country.name:
            data["country"] = country_resp.country.name
    except Exception:
        pass

    try:
        city_resp = _city_reader.city(ip)
        if city_resp.subdivisions.most_specific.name:
            data["region"] = city_resp.subdivisions.most_specific.name
        if city_resp.city.name:
            data["city"] = city_resp.city.name
    except Exception:
        pass

    return data
