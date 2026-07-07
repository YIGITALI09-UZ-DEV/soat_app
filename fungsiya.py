from datetime import datetime

# Boshlang'ich soat, daqiqa va sekund
def vaqt(dt=None):
    #hozir = datetime.now()
    #soat = int(datetime.now().strftime("%H"))
    #minut = int(datetime.now().strftime("%M"))
    #sekund = int(datetime.now().strftime("%S"))
    #misekund = hozir.microsecond // 1000 
    return datetime.now().strftime("%H:%M:%S")