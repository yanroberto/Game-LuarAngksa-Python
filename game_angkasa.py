import pygame
import math
import random

#Import background music
from pygame import mixer 

#Game sederharana by : yanroberto philip


#inisiasi pygame yang di import
pygame.init()

#resolusi_layar
lebar  = 800
tinggi = 600

#variabel untuk menyimpan ukuran layar
tampilan_layar = pygame.display.set_mode((lebar,tinggi))

#membuat caption/  judul
pygame.display.set_caption('Game Luar angkasa')

#variabel untuk menyimpan warna background RGB
putih  = (255,255,255)
hitam  = (0,0,0)

#background
background  = pygame.image.load ('background.png')

#background soung
mixer.music.load('background.wav')
mixer.music.play(-1)



#Variabel menyimpan time clock
clock = pygame.time.Clock()

#variabel untuk menyimpan nilai boolean
crash = False

#variabel simpan dan load gambar
Gambar_pemain = pygame.image.load('space-invaders.png')


#varibel menampung_icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#funsgi pemain 
def pemain (x,y):
    tampilan_layar.blit(Gambar_pemain,(x,y))


#definisikan  koordinat x dan y untuk meletakan gambar di layar
x = 370
y = 480
playerx_change =0

#membuat musuh lebih dari satu menggunakan list
Gambar_musuh      = []
musuhX            = []
musuhY            = []
pergerakan_musuhX = []
pergerakan_musuhY = []
jumlah_musuh      = 6

#kooridinat_musuh
for i in range(jumlah_musuh):
    Gambar_musuh.append(pygame.image.load('monsterr.png'))
    musuhX.append(random.randint(0,735))
    musuhY.append(random.randint(50,150))
    pergerakan_musuhX.append(4)
    pergerakan_musuhY.append(40)


#fungsi musuh
def musuh (x, y,i):
    tampilan_layar.blit(Gambar_musuh[i], (x,y))


#kooridinat_peluru
Gambar_peluru  = pygame.image.load('bullet.png')
peluruX = 0
peluruY = 480
pergerakan_peluruX = 0
pergerakan_peluruY = 10
status_peluru = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10


#fungsi game over
tulisan_gameOver = pygame.font.Font('freesansbold.ttf',64)

def game_over ():
 tulisan_game_over = tulisan_gameOver.render ("GAME OVER" ,True,(255,255,255))
 tampilan_layar.blit(tulisan_game_over,(200,250))


#funsgi menampilkan score
def tampilkan_score (x,y):
    score = font.render ("Score : " + str (score_value),True,(255,255,255))
    tampilan_layar.blit(score,(x,y))



#fungsi_tembakan
def tembakan_peluru (x,y) :
    global status_peluru
    status_peluru = "tembak"
    tampilan_layar.blit(Gambar_peluru,(x+16,y+10))


#fungsi Titik_Tengah antara dua titik [d= akar (x2-x2)^2 + (y2-y1)^2]
def JarakDua_titik (musuhX , musuhY, peluruX, peluruY):
    jarak = math.sqrt((math.pow(musuhX-peluruX ,2))+ (math.pow(musuhY-peluruY,2)))
    if jarak < 27 :
        return True
    else :
        return False    


# while conition jika crach true dan false 
while not crash :
    #menetapkan warna background #tampilan_layar.fill(hitam)
    #backgorund 
    tampilan_layar.blit(background,(0,0))

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crash = True
        

        #Untuk mengerakan gambar sesuai keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change  = -5
            if event.key == pygame.K_RIGHT:
                playerx_change  =  5
            if event.key == pygame.K_SPACE:
                if status_peluru is "ready":
                    suara_peluru = mixer.Sound('laser.wav')
                    suara_peluru.play()
                    # Get the current x koordinar
                    peluruX = x
                    tembakan_peluru (x,peluruY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerx_change  = 0        
    
    # pergerakan akan bertambah atau berkurang sebesar =0.5
    x +=playerx_change 

    #kondisi agar gambar tidak keluar dari layar
    if x<=0:
        x=0 
    elif x >= (800-64):
        x=736

    #pergerakan musuh dan batas gerakan musuh [agar tidak keluar layar]
    for i in range (jumlah_musuh) :
        
        #Game Over
        if musuhY[i] > 200:
            for j in range (jumlah_musuh) :
                musuhY[i] = 2000
            #memangil fungsi tampilkan game over
            game_over ()
            break

        musuhX[i] += pergerakan_musuhX[i]
        if musuhX[i]<=0:
            pergerakan_musuhX[i]=4
            musuhY[i] +=pergerakan_musuhY[i]
        elif musuhX[i] >= (800-64):
            pergerakan_musuhX[i]=-4
            musuhY[i] +=pergerakan_musuhY[i]

        #memangil fungsi jarak
        nilai_jarak = JarakDua_titik (musuhX[i],musuhX[i],peluruX,peluruY)
        if nilai_jarak:
            suara_tembakan = mixer.Sound('explosion.wav')
            suara_tembakan.play()
            peluruY = 480
            status_peluru = "ready"
            score_value += 1
            #print (score)
            musuhX[i] = random.randint(0,735)
            musuhY[i] = random.randint(50,150)
        
        #memangil fungsi musuh
        musuh(musuhX[i],musuhY[i] ,i)

    #pergerakan peluru
    if peluruY <= 0:
        peluruY =480
        status_peluru = "ready"

    if status_peluru  is "tembak" :
        tembakan_peluru (peluruX,peluruY)
        peluruY -= pergerakan_peluruY 

    


    #memangil fungsi pemain
    pemain(x,y)
    
    #memangil fungsi tampilkan score
    tampilkan_score(textX,textY)
    
    #update tampilan laayr
    pygame.display.update()
    clock.tick(60) #1menit


pygame.quit()
quit()