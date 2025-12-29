import geoip2.database

reader = geoip2.database.Reader("data/geoip/GeoLite2-Country.mmdb")
response = reader.country("8.8.8.8")
print(response.country.name)
