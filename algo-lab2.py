ad_soyad = str (input("adinizi soyadinizi giriniz : "))
diploma_notu = float (input("diploma notunuzu giriniz :"))
sinav_puani = float (input("sinav puaninizi giriniz :"))
kayitlilik_durumu = int (input("onceki yil kayit durumunuz var ise 1, onceki yil kayit durunmunuz yok ise 0 giriniz :"))

OBP = diploma_notu * 5

alaniniz_disinda_ekpuan = OBP * 0.12 / ( 1 + kayitlilik_durumu )
alaninizla_ilgili_ekpuan = OBP * ( 0.12 + 0.06 ) / ( 1 + kayitlilik_durumu ) 

alaniniz_disinda_puan = sinav_puani + alaniniz_disinda_ekpuan
alaninizla_ilgili_puan = sinav_puani + alaninizla_ilgili_ekpuan

print( "Alaniniz disinda bir yuksekogretim programini tercih etmeniz durumunda kazanacaginiz ek puan miktari:" , format(alaniniz_disinda_ekpuan,".5f"))
print( "Alaninizla ilgili bir yuksekogretim programini tercih etmeniz durumunda kazanacaginiz ek puan miktari:" , format(alaninizla_ilgili_ekpuan,".5f"))
print( "Alaniniz disinda bir yuksekogretim programini tercih etmeniz durumunda elde edeceginiz yerlestirme puani" , format(alaniniz_disinda_puan,".5f"))
print( "Alaninizla ilgili bir yuksekogretim programini tercih etmeniz durumunda elde edeceginiz yerlestirme puani" , format(alaninizla_ilgili_puan,".5f"))
