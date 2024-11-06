from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import re
import pandas as pd
import difflib

from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource

# List of wines with price information
wines_with_prices = [
    ("Abrasado Unique Parcel Malbec", 143.00),
    ("Achaval Ferrer Finca Bella Vista Malbec", 650.00),
    ("Achaval Ferrer Finca Mirador Malbec", 650.00),
    ("Achaval Ferrer Quimera", 210.00),
    ("Achaval Ferrer Quimerino Tinto", 120.00),
    ("Adrianna Vineyard Fortuna Terrae Malbec - Safra 2017", 899.00),
    ("Adrianna Vineyard Mundus Bacilus Terrae Malbec - Safra 2017", 2200.00),
    ("Alamos Cabernet Sauvignon", 59.40),
    ("Alamos Malbec", 59.40),
    ("Alamos Reserva Malbec", 82.00),
    ("Alma Negra Misterio", 125.00),
    ("Alto - Alta Vista", 440.00),
    ("Ambrosia Precioso - Malbec", 192.40),
    ("Ambrosia Vina Única Malbec", 117.00),
    ("Angelica Zapata Cabernet Franc", 128.00),
    ("Angelica Zapata Cabernet Sauvignon Alta", 128.00),
    ("Angelica Zapata Malbec Alta", 151.05),
    ("Asadito de Obra Malbec - Familia Millan - Mosquita Muerta", 36.00),
    ("Asadito de Obra Cabernet Sauvignon - Familia Millan - Mosquita Muerta", 36.00),
    ("Baldomir Terroirs Serie Single Vineyards Vistalba Mlabec 2013", 270.00),
    ("Baldomir Terroirs Serie Single Vineyards La Consulta Malbec 2014", 270.00),
    ("Barda Pinot Noir - Chacra", 198.00),
    ("BenMarco Expressivo", 155.00),
    ("Black River Malbec - Humberto Canale", 72.00),
    ("Bodegas Budeguer - 4000 Black Blend Gran Reserva", 115.00),
    ("Bodegas Budeguer - 4000 Blue Blend Reserva", 80.00),
    ("Bodegas Budeguer - 4000 Blue Malbec Reserva", 80.00),
    ("Bodegas Budeguer - 4000 Gran Reserva Cabernet Sauvignon", 115.00),
    ("Bodegas Budeguer - 4000 Gran Reserva Malbec", 115.00),
    ("Bodegas Budeguer - 4000 Gran Reserva Petit Verdot", 115.00),
    ("Bodegas Budeguer - 4000 Reserva Syrah", 80.00),
    ("Bodegas Budeguer - Partida Limitada Corte de Bodegas", 165.00),
    ("Bodegas Budeguer - Partida Limitada Merlot", 165.00),
    ("Bodegas Budeguer - Partida Limitada Pinot Noir", 165.00),
    ("Bramare Cabernet Sauvignon", 230.00),
    ("Bramare Malbec", 230.00),
    ("Bressia Monteagrelo Malbec", 93.00),
    ("Bressia Piel Negra", 154.00),
    ("Bressia Conjuro", 330.00),
    ("Bressia Malbec Doc", 650.00),
    ("Bressia Ultima Hoja", 660.00),
    ("Cadus Single Vineyard Malbec Las Torcazas", 193.00),
    ("Catena Alta Malbec", 340.00),
    ("Catena Zapata Estiba Reservada Safra 2015", 2250.00),
    ("Carmelo Patti Cabernet Sauvignon", 145.00),
    ("Carmelo Patti Malbec", 145.00),
    ("Cheval Des Andes", 637.00),
    ("Colome 1831 Malbec", 260.00),
    ("Cordero Con Piel de Lobo Blend de Tintas", 39.60),
    ("Cordero Con Piel de Lobo Bonarda", 39.60),
    ("Cordero Con Piel de Lobo Cabernet Sauvignon 750ml", 39.60),
    ("Cordero Con Piel de Lobo Malbec 750 Ml", 39.60),
    ("Cordero Con Piel de Lobo Merlot 750 Ml", 39.60),
    ("Cordero Con Piel de Lobo Syrah 750 Ml", 39.60),
    ("Clos de Los Siete", 88.00),
    ("Domaine Nico Le Paradis", 1190.00),
    ("Don Genaro Cabernet Sauvignon - Familia Millan - Mosquita Muerta", 51.15),
    ("Don Genaro Malbec - Familia Millan - Mosquita Muerta", 51.15),
    ("Don Genaro Private Selection Malbec - Familia Millan - Mosquita Muerta", 92.07),
    ("Don Juan Reserva", 121.00),
    ("Dv Catena Cabernet/Malbec", 73.15),
    ("Dv Catena Divina Italia Malbec - Bonarda", 195.00),
    ("Dv Catena Domingo", 135.00),
    ("Dv Catena L' Esploratore Malbec", 143.00),
    ("Dv Catena La Piramide Cabernet Sauvingon", 135.00),
    ("Dv Catena Malbec/Malbec", 104.50),
    ("Dv Catena Nicasia Malbec Single Vineyard", 159.00),
    ("El Enemigo Bonarda", 125.00),
    ("El Enemigo Cabernet Franc", 125.00),
    ("El Enemigo Malbec", 125.00),
    ("El Mendocino Malbec", 46.00),
    ("El Provenier Icono", 234.00),
    ("Enrique Foster Firmado Bonarda", 240.00),
    ("Enrique Foster Firmado Malbec", 240.00),
    ("Enrique Foster Malbec Edicion Limitada", 142.00),
    ("Enrique Foster Reserva Bonarda", 78.00),
    ("Enrique Foster Reserva Malbec", 78.00),
    ("Enrique Foster S,V, Finca Los Barrancos Malbec", 80.00),
    ("Enzo Bianchi Gran Corte", 440.00),
    ("Escorihuela Gascon Gran Reserva Cabernet Sauvignon", 94.00),
    ("Escorihuela Gascon Gran Reserva Malbec", 94.00),
    ("Escorihuela Gascon MEG Blend", 220.00),
    ("Escorihuela Gascon The President Blend", 165.00),
    ("Escorihuela Gascon The President Malbec", 187.00),
    ("Fabre Montmayou Gran Vin", 150.00),
    ("Familia Schroeder Blend - Patagonia", 179.40),
    ("Familia Schroeder Malbec - Patagonia", 179.40),
    ("Familia Schroeder Pinot - Patagonia", 179.40),
    ("Felipe Rutini Safra 2012", 2180.00),
    ("Finca Perdriel Centenario - Bodega Norton", 143.00),
    ("Fond de Cave Gran Reserva Malbec  - Trapiche", 91.00),
    ("Fuego Blanco Flinstone Cabernet Franc", 99.39),
    ("Gran Enemigo Agrelo", 199.00),
    ("Gran Enemigo Cepillo", 199.00),
    ("Gran Enemigo Chacayes", 199.00),
    ("Gran Enemigo Gualtalary Cabernet Franc", 328.00),
    ("Gran Sombreno Malbec", 89.00),
    ("Gran Tonel 137 Malbec", 143.00),
    ("Hermandad Blend", 126.00),
    ("Hermandad Malbec", 126.00),
    ("Hermandad Winemaker Seriers Petit Verdot", 175.00),
    ("Huentala Block 03 La Isabel Estate Malbec 2019", 250.00),
    ("Irracional Malbec", 163.00),
    ("Jorge Rubio A Contramano Cabernet Sauvignon", 78.00),
    ("Jorge Rubio A Contramano Criolla", 78.00),
    ("Jorge Rubio A Contramano Malbec", 78.00),
    ("Jorge Rubio Malbec de Anfora", 220.00),
    ("Jorge Rubio Privado Bonarda", 74.00),
    ("Jorge Rubio Privado Pinot Noir", 74.00),
    ("Jorge Rubio Privado Tempranillo", 74.00),
    ("Jose Zuccardi Malbec", 220.00),
    ("Judas Blend", 399.00),
    ("Judas Malbec", 395.00),
    ("Kaiken Luxury Edition 20 Anos", 220.00),
    ("kaiken Mai", 275.00),
    ("La Cupula Malbec - Familia Millan - 97 Pontos Robert Parker - Lançamento", 690.00),
    ("La Linda Malbec", 60.00),
    ("La Linterna Cabernet Sauvignon Cafayate", 429.00),
    ("La Linterna Malbec Pedernal", 429.00),
    ("La Linterna Pinot Noir Los Arboles", 429.00),
    ("La Piel de Judas Acto II - Edicion Limitada", 550.00),
    ("Lamborghini Malbec - Tinto de Umbria, Italia", 94.50),
    ("Las Perdices Alae Malbec", 418.00),
    ("Las Perdices Tinamu", 198.00),
    ("Las Perdices Chac Chac Malbec", 39.00),
    ("Los Haroldos Gran Corte - Blend de Terroirs - Blend de 7 Uvas - Safra 2020", 132.00),
    ("Los Intocables Blend Bourbon Barrel", 66.50),
    ("Los Intocables Cabernet Bourbon Barrel", 66.50),
    ("Luca Beso de Dante", 220.00),
    ("Luca Pinot Noir G lot", 158.00),
    ("Luca Old Wine Malbec", 158.00),
    ("Luigi Bosca de Sangre Malbec", 110.00),
    ("Luigi Bosca de Sangre Malbec Doc", 110.00),
    ("Luigi Bosca Malbec", 72.00),
    ("Luigi Bosca Paraiso - Icono", 590.00),
    ("Malbec Argentino - Catena Zapata", 345.00),
    ("Malcriado Mosquita Muerta", 378.00),
    ("Mara Merlot - Vino Sustentable", 88.00),
    ("Margarita para los Chanchos Cabernet Sauvignon", 66.00),
    ("Margarita para los Chanchos Malbec", 66.00),
    ("Mariflor Malbec", 210.00),
    ("Marchiori & Barraud Malbec", 91.00),
    ("Matervini Alteza - Salta", 550.00),
    ("Matervini Antes Andes Canota Malbec", 380.00),
    ("Matervini Calcha Malbec", 420.00),
    ("Matervini Finca - Perdriel Malbec", 550.00),
    ("Matervini Piedras Viejas -- El Challao - Las Heras", 780.00),
    ("Matervini Tinto Chacayes Vale de Uco", 275.00),
    ("Mauricio Lorca Gran Opalo Blend", 100.00),
    ("Mauricio Lorca Inspirado Cabernet Franc", 220.00),
    ("Mauricio Lorca Poetico Cabernet Sauvignon", 80.00),
    ("Mil Demonios Assemblage", 110.00),
    ("Mil Demonios Corte Calchaqui", 165.00),
    ("Mil Demônios Lucifer", 230.00),
    ("Mil Demônios Malbec", 118.00),
    ("Mil Demonios Pirata Cabernet Sauvignon", 148.00),
    ("Mil Demônios Samurai", 165.00),
    ("Mil Demônios Vikingo Corte de Petit Verdot", 165.00),
    ("Mosquita Muerta Blend de Tintas 750 Ml", 143.00),
    ("Mosquita Muerta Malbec 750 Ml", 143.00),
    ("Nicasia Red Blend Malbec", 59.40),
    ("Nicasia Red Blend Cabernet Franc", 59.40),
    ("Nico by Luca", 480.00),
    ("Nicola Catena Parcela Bonarda", 230.00),
    ("Nicolas Catena Zapata", 370.00),
    ("Norton Doc", 59.00),
    ("Numina Gran Corte", 129.00),
    ("Numina Malbec", 99.00),
    ("Numina Pinot Noir", 99.00),
    ("Outro Loco Mas Malbec", 40.00),
    ("Padrillos Malbec", 135.00),
    ("Pequenas Produciones Malbec", 125.00),
    ("Pequenas Produciones Syrah", 125.00),
    ("Perro Callejero Blend de Malbec", 66.00),
    ("Perro Callejero Cabernet Franc 750 Ml", 66.00),
    ("Perro Callejero Pinot Noir 750 Ml", 66.00),
    ("Piattelli Arlene", 190.00),
    ("Piattelli Gran Reserva Malbec Mendoza", 121.00),
    ("Piattelli Gran Reserva Malbec Salta", 121.00),
    ("Piattelli Reserva Malbec Mendoza", 77.00),
    ("Piattelli Reserva Malbec/tannat", 77.00),
    ("Piattelli Reserva Cabernet Sauvignon", 77.00),
    ("Piattelli Trinita Grand Reserve", 190.00),
    ("Pionero Blend Gualtallary", 590.00),
    ("Pispi Blend de Tintas 750 Ml", 95.00),
    ("ProXecto Cabernet Franc Valle de Uco Safra 2019", 132.00),
    ("ProXecto Malbec Valle de Uco Safra 2019", 132.00),
    ("Pulenta Estate Malbec", 120.00),
    ("Pulenta Gran Corte", 325.00),
    ("Pulenta Gran Merlot", 290.00),
    ("Pulenta Gran Cabernet Franc", 365.00),
    ("Pulenta Gran Cabernet Sauvignon", 290.00),
    ("Pulenta Gran Malbec", 365.00),
    ("Pulenta Gran Pinot Noir", 365.00),
    ("Pulenta Homenagem Porsche 70 Anos - Cabernet Sauvignon - Safra 2020", 590.00),
    ("Pulenta La Flor Blend", 69.00),
    ("Pulenta La Flor Cabernet Sauvignon", 69.00),
    ("Pulenta La Flor Malbec", 69.00),
    ("Pulenta Limited Editions Porsche Macan Gran Corte Safra 2014", 900.00),
    ("Raquis Las Bases", 599.00),
    ("Rutini Antologia - LI (51)", 308.00),
    ("Rutini Antologia - LIII (53)", 275.00),
    ("Rutini Antologia - LXI (61)", 345.00),
    ("Rutini Antologia - XLIX (49)", 275.00),
    ("Rutini Antologia - XXXVIII (38)", 275.00),
    ("Rutini Antologia - LX (60)", 340.00),
    ("Rutini Antologia - LXII (62)", 355.00),
    ("Rutini Cabernet Franc /Malbec", 110.00),
    ("Rutini Encuentro Malbec", 80.00),
    ("Rutini Malbec", 148.00),
    ("Rutini Single Vineyard Gualtalary Cabernet Sauvignon", 297.00),
    ("Saint Felicien Bonarda", 145.00),
    ("Saint Felicien Cabernet Franc", 72.00),
    ("Saint Felicien Malbec", 66.00),
    ("Salentein Reserva Malbec", 80.00),
    ("Salentein Reserva Pinot", 72.00),
    ("San Pedro de Yacochuya", 138.00),
    ("Sapo de Otro Pozo Blend de Tintas 750 Ml", 110.00),
    ("Saurus Barrel Fermented Cabernet Franc", 118.00),
    ("Saurus Estate Pinot Noir", 78.00),
    ("Siesta Single Vineyard Malbec", 148.00),
    ("Sin Reglas Cabernet Sauvignom", 77.00),
    ("Sin Reglas Assemblage", 77.00),
    ("Sottano Malbec", 65.00),
    ("Sottano Reserva Blend", 66.00),
    ("Sottano Reserva de Familia 3S Cabernet Malbec", 99.00),
    ("Sottano Reserva de Familia 3S Malbec", 99.00),
    ("Sottano Reserva de Familia 3S Pinot Noir", 99.00),
    ("Sottano Reserva Malbec", 66.00),
    ("Susana Balbo Nosotros Single Vineyard Nomade", 530.00),
    ("Tapiz Las Notas de Jean Claude", 385.00),
    ("Tapiz Retrato por Jean Claude", 396.00),
    ("Tinto Zuccardi", 175.00),
    ("Trivento Eolo Malbec", 390.00),
    ("Trapiche Iscay Malbec - Cabernet Franc", 323.00),
    ("Trumpeter Malbec", 60.00),
    ("Vicentin Colosso Los Chacayes Malbec", 160.00),
    ("Vicentin El Renegado", 69.00),
    ("Vina Cobos Vinculum Malbec", 379.00),
    ("Vistalba Corte A", 297.00),
    ("Zuccardi Finca Piedra Infinita Paraje Altamira Safra 2019", 980.00),
    ("Zuccardi Concreto Malbec", 168.00),
    ("Zuccardi Aluvional Paraje Altamira", 390.00),
    ("Zuccardi Q Cabernet Sauvignon", 99.00),
    ("Zuccardi Q Malbec", 99.00),
    ("Yacochuya Tinto", 289.00),
    ("Gran Enemigo Gualtalary Safra 2019 100 pts - 2 Premiacao de 100 Pontos", 550.00),
    ("Jorge Rubio Edicion Tinto Tardio - Dulce Natural", 52.00)
]

# Shuffle and select a subset of wines
random.shuffle(wines_with_prices)
wines_with_prices = wines_with_prices[:10]

# Setting up Selenium WebDriver
driver = webdriver.Chrome()  # ChromeDriver will be automatically found if it's in your PATH
wait = WebDriverWait(driver, 10)

wine_rankings = []

try:
    driver.get("https://www.vivino.com/")
    
    for wine, price in wines_with_prices:
        # Locate the search bar and enter the wine name
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(wine)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        time.sleep(3)

        try:
            # Get the first wine result and its rating
            wine_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.wine-card__content")))
            wine_name = wine_element.find_element(By.CSS_SELECTOR, "span.wine-card__name").text
            wine_rating = wine_element.find_element(By.CSS_SELECTOR, "div.average__number").text.replace(",", ".")  
            wine_link = wine_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            # Check if the extracted name is too different from the provided name
            similarity = difflib.SequenceMatcher(None, wine, wine_name).ratio()
            if similarity < 0.6:
                user_input = input(f"The extracted wine name '{wine_name}' is different from the provided name '{wine}'. Do you want to include it? (y/n): ").strip().lower()
                if user_input != 'y':
                    continue
            
            
            wine_rankings.append((wine_name, float(wine_rating), price, wine_link))
            print(f"{wine}: {wine_rating}")
        except Exception as e:
            print(f"Could not find rating for {wine}: {e}")

    # Create a DataFrame for plotting
    df = pd.DataFrame(wine_rankings, columns=["Wine", "Rating", "Price", "Link"])
    
    # Plotting with Bokeh
    source = ColumnDataSource(df)
    
    p = figure(title="Wine Price vs Rating", x_axis_label='Rating', y_axis_label='Price (R$)', tools=["pan,box_zoom,reset"])
    
    hover = HoverTool(tooltips=[
        ("Wine", "@Wine"),
        ("Price", "@Price{0.00}"),
        ("Rating", "@Rating{0.0}"),
        ("Link", "<a href='@Link' target='_blank'>Vivino Link</a>")
    ])
    p.add_tools(hover)
    
    p.circle(x='Rating', y='Price', size=10, source=source, fill_alpha=0.6)
    
    show(p)

finally:
    driver.quit()
