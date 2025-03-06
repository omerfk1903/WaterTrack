import pandas as pd
import json
from os import getcwd
from datetime import datetime as dt
from random import randint

class bills : 

    def __init__(self):
        self.random = 0

        # Jsom dosya yolu
        self.json_file_path = "Data.json"

        # Excel için veri şablonu oluşturma
        self.data = {
            "Tarih (Ay/Yıl)": [],  # Tarih bilgisi için sütun
            "Daire No": [],        # Daire numarası
            "Geçen Ay Tüketim (m³)": [],  # Önceki ayın tüketimi
            "Bu Ay Tüketim (m³)": [],  # Bu ayın tüketimi
            "Fark (m³)": [],  # Tüketim farkı
            "Ödenecek Tutar (TL)": [],  # Hesaplanan ödeme miktarı
        }
        
        # INPUT
        self.InputDate = str(dt.now()).split(" ")[0]
        self.DataValue = [] 

        # Json dosyasından veri çekme 
        self.dataRead = self.DataRead(self.json_file_path)
        
    def DataWrite(self,file,datajson) :

        with open(file, "w", encoding="utf-8") as json_file : 
            json.dump(datajson,json_file,indent=4, ensure_ascii=False)

    def DataRead(self,file) : 

        with open(file, "r", encoding="utf-8") as json_file : 
            return json.load(json_file)
        
    def InputFunch(self) :  # Veri girişi yapılıyor

        datajson = self.dataRead["Ödemeler"]

        dateLen = len(datajson["Daire 1"])

        print(" !!!!! Harcanan su miktarının toplamı her zaman bir ay öncekinden yüksek olması gereklidir . !!!!! ")

        for Daires in datajson :
             
            last_bills = int(list(datajson[Daires][dateLen-1].values())[0]["Harcanan Su (m³)"])

            mt = f" {Daires} : Geçen ay harcadığı miktar : {last_bills} |  Bu ay harcadığı miktar : "
            
            if self.random == 1 : data = int(input(mt)) # Veri girişi yapılır
            else : data = randint(60,100)  # Sistemi denemek için kullanılır
            
            if last_bills < data : self.DataValue.append(data)
            else : break
        
    def Data_Adds(self) : 

        datajson = self.dataRead["Ödemeler"]

        for cnt,Daire in enumerate(datajson,start=0) :
            kup = self.DataValue[cnt] 
            add = {self.InputDate : {"Harcanan Su (m³)": kup,"Ödenecek Tutar (TL)" : kup*60} }
            if Daire not in datajson : datajson[Daire] = []
            if not isinstance(datajson[Daire],list) : datajson[Daire] = [datajson[Daire]] 
            datajson[Daire].append(add)
        
        self.DataWrite(file=self.json_file_path,datajson=self.dataRead)

    def Excel_From_Create(self) : 
        
        datajson = self.dataRead["Ödemeler"]
        ListeLen = 0

        for Daire in datajson : 
            Dairesİnfo = [out for out in datajson[Daire] if out != None and out != " "]
            Date_Len = len(Dairesİnfo) # Tarih içeriği miktarı
            Date = str(list(Dairesİnfo[len(Dairesİnfo)-1].keys())[0]) + " | " + str(list(Dairesİnfo[len(Dairesİnfo)-2].keys())[0]) # Geçmiş ayın ve Bu AYIN TARİH BİLGİSİ ALINIYOR
            Last_Month_Consumption = int(list(Dairesİnfo[Date_Len-2].values())[0]["Harcanan Su (m³)"])
            This_Mont_Consumption = int(list(Dairesİnfo[Date_Len-1].values())[0]["Harcanan Su (m³)"])
            diff = This_Mont_Consumption - Last_Month_Consumption # fark
            price = diff * 60 # fiyat
            DaireNumber = int(str(Daire).split(" ")[1]) # Daire

            if diff >= 0 : 
                self.data["Daire No"].append(DaireNumber)# DAİRE NUMARASINI ALIYOR
                self.data["Tarih (Ay/Yıl)"].append(Date)# TARİH BİLGİSİ EKLENİYOR
                self.data["Geçen Ay Tüketim (m³)"].append(Last_Month_Consumption)
                self.data["Bu Ay Tüketim (m³)"].append(This_Mont_Consumption)
                self.data["Fark (m³)"].append(diff)
                self.data["Ödenecek Tutar (TL)"].append(price)
                ListeLen = ListeLen + 1
            else : print(" THİS  : {0} > LAST : {1} ".format(This_Mont_Consumption,Last_Month_Consumption))

            Dairesİnfo.clear()

        if ListeLen == len(datajson) : 
        
            # DataFrame oluşturma
            df = pd.DataFrame(self.data)

            # Excel dosyasına yazma
            file_path = getcwd() + "\\Su_Tuketim_Takibi.xlsx"
            df.to_excel(file_path, index=False)
        
        else : print(" Veriler eksik ")

        for cls in self.data : self.data[cls].clear()

    def start(self) : 

        self.InputFunch()
        self.Data_Adds()
        self.Excel_From_Create()

Bills = bills()

if __name__ == "__main__" : 

    Bills.start()
    