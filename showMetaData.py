from PIL import Image
import piexif


def dms_to_decimal(dms):
    """Konwertuje współrzędne DMS (stopnie, minuty, sekundy) na format dziesiętny."""
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0
    return degrees + minutes + seconds


def print_jpg_metadata(file_path):
    # Otwórz obraz JPG
    img = Image.open(file_path)

    # Wydobądź metadane EXIF
    exif_data = img._getexif()

    if exif_data is not None:
        for tag_id, value in exif_data.items():
            # Wydobądź nazwę tagu
            tag = piexif.TAGS['Exif'].get(tag_id, tag_id)
            print(f"{tag}: {value}")

            # Sprawdź, czy tag jest GPSLatitude lub GPSLongitude
            if tag_id == 34853:  # GPSInfo
                latitude = value.get(2)  # 2 to GPSLatitude
                latitude_ref = value.get(3)  # 3 to GPSLatitudeRef (N/S)
                longitude = value.get(4)  # 4 to GPSLongitude
                longitude_ref = value.get(5)  # 5 to GPSLongitudeRef (E/W)

                if latitude and longitude:
                    lat_decimal = dms_to_decimal(latitude)
                    if latitude_ref == 'S':
                        lat_decimal = -lat_decimal

                    long_decimal = dms_to_decimal(longitude)
                    if longitude_ref == 'W':
                        long_decimal = -long_decimal

                    print(f"Współrzędne geograficzne: {lat_decimal}, {long_decimal}")

    else:
        print("Brak metadanych EXIF w pliku.")




# Użycie funkcji
file_path = '20250206_094615.jpg'
print_jpg_metadata(file_path)
