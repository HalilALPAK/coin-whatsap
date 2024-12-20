import requests
import time
import pywhatkit as kit
from datetime import datetime, timedelta

def fiyat():
    # CoinGecko API URL'si
    url = "https://api.coingecko.com/api/v3/simple/price"

    # Takip edilecek coinler ve para birimleri
    parameters = {
        "ids": "bitcoin,ethereum",  # Takip etmek istediğiniz coinler
        "vs_currencies": "usd,eur,try"  # İstediğiniz para birimleri
    }


    # API'ye istekte bulun
    response = requests.get(url, params=parameters)
    
    if response.status_code == 200:
        data = response.json()
        
        # Bitcoin ve Ethereum fiyatlarını al
        bitcoin_prices = data["bitcoin"]
        ethereum_prices = data["ethereum"]
        
        # Fiyatları birleştirerek string olarak döndür
        message = (
            f"Bitcoin Fiyatları:\n"
            f"  USD: ${bitcoin_prices['usd']}\n"
            f"  EUR: €{bitcoin_prices['eur']}\n"
            f"  TRY: ₺{bitcoin_prices['try']}\n\n"
            f"Ethereum Fiyatları:\n"
            f"  USD: ${ethereum_prices['usd']}\n"
            f"  EUR: €{ethereum_prices['eur']}\n"
            f"  TRY: ₺{ethereum_prices['try']}"
        )
        return message
    else:
        return f"API isteği başarısız oldu: {response.status_code}"

def mesaj_gonder(phone_number, message, dakika_sonra=2, wait_time=10):
    """
    Belirli bir süre sonra WhatsApp mesajı gönderir.

    Parametreler:
        phone_number (str): Alıcının telefon numarası (uluslararası formatta).
        message (str): Gönderilecek mesaj içeriği.
        dakika_sonra (int): Mesajın gönderileceği süre (dakika olarak, şu andan itibaren).
        wait_time (int): WhatsApp Web'in yüklenmesi için bekleme süresi (saniye olarak).
    """
    # Şu anki zamanı al ve gönderim saatini belirle
    now = datetime.now()
    send_time = now + timedelta(minutes=dakika_sonra)
    hour = send_time.hour
    minute = send_time.minute

    try:
        # Mesaj gönder
        kit.sendwhatmsg(
            phone_number,
            message,
            hour,
            minute,
            wait_time=wait_time
        )
        print(f"Mesaj {hour}:{minute}'de gönderilecek.")
    except Exception as e:
        print(f"Mesaj gönderilirken bir hata oluştu: {e}")

# Fiyat bilgilerini al ve mesaj gönder
message = fiyat()
if message:
    mesaj_gonder(
        "+905538855696",  # Alıcının telefon numarası
        message,         # Gönderilecek mesaj
        dakika_sonra=3,  # 2 dakika sonra gönder
        wait_time=10     # WhatsApp Web yüklenme süresi
    )
