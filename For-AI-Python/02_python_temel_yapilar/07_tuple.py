# tuple -> ()
koordinat = (10, 20)
renkler = ("kırmızı", "mavi", "yeşil")

# liste vs tuple
liste = [1, 2, 3]
liste[0] = 99 # çalışır
print(liste) # [99, 2, 3]

tup = (1, 2, 3)
# tup[0] = 99 # TypeError: 'tuple' object does not support item assignment

# indeksleme
t = (10, 20, 30)
print(t[1]) # 20
print(t[-1]) # 30

# slicing
t = (10, 20, 30, 40)
print(t[1:3]) # (20, 30)

# tek elemanlı tuple
x = (5) # x = 5
print(type(x)) # tuple? int? cevap <class 'int'>

x = (5,)
print(type(x)) # <class 'tuple'>

# tuple unpacking 
koordinat = (10, 20)
x, y = koordinat
print(x) # 10
print(y) # 20

# tuple metotları
t = (20, 20, 30, 40)

print(t.count(20)) # 2
print(t.index(30)) # 2