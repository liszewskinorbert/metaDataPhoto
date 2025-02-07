from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Funkcja do pobierania treści strony za pomocą Selenium
def get_page_content(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)

    # Czekaj na załadowanie dynamicznych treści
    time.sleep(5)  # Czekaj 5 sekund (dostosuj zgodnie z potrzebami)

    # Pobierz treść HTML strony
    html_content = driver.page_source

    # Zamknij przeglądarkę
    driver.quit()

    return html_content

# Adres URL
url = 'http://192.168.1.245/home/index.html#hashHome'

# Pobierz zawartość strony
html_content = get_page_content(url)

# Analiza zawartości strony
soup = BeautifulSoup(html_content, 'html.parser')

# Funkcja pobierająca wartości z danych
def get_image_data(label):
    data_label = soup.find(string=label)
    if data_label:
        return data_label.find_next().text.strip()
    return "Nie znaleziono"

# Wyszukiwanie wszystkich wymaganych danych
black_and_white_images = get_image_data('Obrazy czarno-białe')
colored_images = get_image_data('Kolorowe obrazy')
total_images = get_image_data('Ogółem obrazów')
large_black_and_white_images = get_image_data('Duże obrazy czarno-białe')
large_colored_images = get_image_data('Duże obrazy kolorowe')

# Wydobywanie wartości procentowych dla tonerów
def get_toner_percentage(color):
    toner_meter = soup.find('meter', id=f'TONER_{color}')
    if toner_meter:
        # Wartość jest w przedziale 0-1, więc mnożymy przez 100 i dodajemy '%'
        percentage_value = float(toner_meter['value']) * 100
        return f"{percentage_value:.1f}%"  # Dwie cyfry po przecinku
    return "Nie znaleziono"

# Wydobywanie wartości tonera
cyan_percentage = get_toner_percentage('C')
magenta_percentage = get_toner_percentage('M')
yellow_percentage = get_toner_percentage('Y')
black_percentage = get_toner_percentage('K')

# Wyświetlanie wyników
print(f"Obrazy czarno-białe: {black_and_white_images}")
print(f"Kolorowe obrazy: {colored_images}")
print(f"Ogółem obrazów: {total_images}")
print(f"Duże obrazy czarno-białe: {large_black_and_white_images}")
print(f"Duże obrazy kolorowe: {large_colored_images}")
print(f"Procent Tonera C: {cyan_percentage}")
print(f"Procent Tonera M: {magenta_percentage}")
print(f"Procent Tonera Y: {yellow_percentage}")
print(f"Procent Tonera K: {black_percentage}")
