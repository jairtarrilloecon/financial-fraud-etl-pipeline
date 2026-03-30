import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta

def generar_dataset_sucio(n_rows=2500):
    np.random.seed(42)
    random.seed(42)
    
    # Datos base
    ids = [f"TRX-{str(i).zfill(5)}" if random.random() > 0.05 else np.nan for i in range(1, n_rows + 1)]
    
    fechas = []
    base_date = datetime(2023, 1, 1)
    for _ in range(n_rows):
        dt = base_date + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        r = random.random()
        if r < 0.2:
            # Formato Americano
            fechas.append(dt.strftime("%m/%d/%Y %H:%M"))
        elif r < 0.4:
            # Formato Europeo
            fechas.append(dt.strftime("%d-%m-%Y %H:%M"))
        elif r < 0.6:
            # Unix Epoch Time
            fechas.append(str(int(time.mktime(dt.timetuple()))))
        elif r < 0.95:
            # Formato Standard (ideal)
            fechas.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            # Roto / Nulo
            fechas.append("ERROR_FECHA" if random.random() > 0.5 else np.nan)

    comercios = ["Amazon", "Vtex", "MercadoLibre", "Alibaba", "Netflix", "Uber", "Airbnb", "Shell Gas", "Starbucks", "Apple Store"]
    comercios_sucios = []
    for _ in range(n_rows):
        merch = random.choice(comercios)
        # Meter ruido tipográfico (simulando errores de encoding o sistemas Legacy)
        r = random.random()
        if r < 0.1: merch = merch.upper()
        elif r < 0.2: merch = merch.lower()
        elif r < 0.3: merch = merch.replace("a", "â").replace("e", "ë").replace("o", "ó")
        elif r < 0.4: merch = "  " + merch + "  "
        comercios_sucios.append(merch)

    montosStr = []
    for _ in range(n_rows):
        monto_base = round(random.uniform(5.0, 5000.0), 2)
        r = random.random()
        if r < 0.4:
            # USD sucio
            montosStr.append(f"$ {monto_base:,.2f}")
        elif r < 0.7:
            # Euro sucio (europeos usan coma para punto decimal y punto para miles)
            monto_euro = monto_base * 0.92
            monto_euro_str = f"{monto_euro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            montosStr.append(f"{monto_euro_str} €")
        elif r < 0.9:
            # Yen Japonés (sin decimales)
            monto_yen = int(monto_base * 150)
            montosStr.append(f"¥ {monto_yen}")
        elif r < 0.98:
            # GBP sin símbolo
            monto_gbp = monto_base * 0.79
            montosStr.append(f"{monto_gbp:.2f}")
        else:
            # Nulos
            montosStr.append(np.nan)

    paises = ["US", "USA", "Estados Unidos", "UK", "GBR", "Reino Unido", "ES", "España", "MX", "Mexico", "JP", "Japón", "PE", "Perú", "CO", "Colombia"]
    pais_lista = [random.choice(paises) if random.random() > 0.05 else np.nan for _ in range(n_rows)]

    ips = []
    for _ in range(n_rows):
        if random.random() < 0.1:
            ips.append(np.nan)
        elif random.random() < 0.05:
            # IP invalida simulando ataque o error
            ips.append(f"{random.randint(256,999)}.{random.randint(10,999)}.0.1")
        else:
            ips.append(f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}")

    
    df = pd.DataFrame({
        "TransactionID": ids,
        "Timestamp_mixed": fechas,
        "Merchant": comercios_sucios,
        "Amount_Currency": montosStr,
        "Country_Raw": pais_lista,
        "Customer_IP": ips
    })
    
    # Hacer que ciertas transacciones de madrugada en ciertos montos sean claramente fraude
    df.to_csv(r"d:\Proyectos\proyecto3-etl-fraude\data\raw\transacciones_corruptas.csv", index=False)
    print("¡Archivo CSV altamente corrupto generado exitosamente en data/raw/transacciones_corruptas.csv!")
    print("Total de filas:", n_rows)

if __name__ == "__main__":
    generar_dataset_sucio()
