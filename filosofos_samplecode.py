import time
import random
import threading
from tkinter import END
N = 5
TIEMPO_TOTAL = 3

class filosofo(threading.Thread):
    semaforo = threading.Lock() #SEMAFORO BINARIO ASEGURA LA EXCLUSION MUTUA
    estado = [] #PARA CONOCER EL ESTADO DE CADA FILOSOFO
    tenedores = [] #ARRAY DE SEMAFOROS PARA SINCRONIZAR ENTRE FILOSOFOS, MUESTRA QUIEN ESTA EN COLA DEL TENEDOR
    count=0
    def __init__(self,ventana):
        super().__init__()      #HERENCIA
        filosofo.semaforo.acquire()  # Bloqueo con el semáforo
        self.id=filosofo.count #DESIGNA EL ID AL FILOSOFO
        self.comida=0
        self.vent=ventana

        self.vent.labels[self.id].config(bg="white")
        filosofo.count+=1 #AGREGA UNO A LA CANT DE FILOSOFOS
        filosofo.estado.append('PENSANDO') #EL FILOSOFO ENTRA A LA MESA EN ESTADO PENSANDO
        filosofo.tenedores.append(threading.Semaphore(0)) #AGREGA EL SEMAFORO DE SU TENEDOR( TENEDOR A LA IZQUIERDA)
        self.vent.escribe("FILOSOFO {0} - PENSANDO".format(self.id))
        filosofo.semaforo.release()  # Libero el semáforo

    def pensar(self):
        time.sleep(random.randint(0,5)) #CADA FILOSOFO SE TOMA DISTINTO TIEMPO PARA PENSAR, ALEATORIO

    def derecha(self,i):
        return (i-1)%N #BUSCAMOS EL INDICE DE LA DERECHA

    def izquierda(self,i):
        return(i+1)%N #BUSCAMOS EL INDICE DE LA IZQUIERDA

    def verificar(self,i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i]='COMIENDO'
            filosofo.tenedores[i].release()  #SI SUS VECINOS NO ESTAN COMIENDO AUMENTA EL SEMAFORO DEL TENEDOR Y CAMBIA SU ESTADO A COMIENDO

    def tomar(self):
        time.sleep(2)
        filosofo.semaforo.acquire() #SEÑALA QUE TOMARA LOS TENEDORES (EXCLUSION MUTUA)
        filosofo.estado[self.id] = 'HAMBRIENTO'
        self.vent.labels[self.id].config(bg="cyan")
        self.verificar(self.id) #VERIFICA SUS VECINOS, SI NO PUEDE COMER NO SE BLOQUEARA EN EL SIGUIENTE ACQUIRE
        filosofo.semaforo.release() #SEÑALA QUE YA DEJO DE INTENTAR TOMAR LOS TENEDORES (CAMBIAR EL ARRAY ESTADO)
        filosofo.tenedores[self.id].acquire() #SOLO SI PODIA TOMARLOS SE BLOQUEARA CON ESTADO COMIENDO

    def soltar(self):
        filosofo.semaforo.acquire() #SEÑALA QUE SOLTARA LOS TENEDORES
        filosofo.estado[self.id] = 'PENSANDO'
        self.vent.escribe("FILOSOFO {} PENSANDO".format(self.id))
        self.vent.labels[self.id].config(bg="white")
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release() #YA TERMINO DE MANIPULAR TENEDORES

    def comer(self):
        self.vent.tenedores[self.id].config(bg="blue")
        self.vent.tenedores[(self.id-1)%N].config(bg="blue")
        print("FILOSOFO {} coge tenedor {} y {}".format(self.id, self.id,(self.id+1)%N))

        self.vent.escribe("FILOSOFO {} COMIENDO".format(self.id))

        self.vent.labels[self.id].config(bg="gold")
        self.vent.tenedores[self.id].config(bg="blue", fg="white")
        self.vent.tenedores[(self.id-1)%N].config(bg="blue", fg="white")
        time.sleep(4) #TIEMPO PARA COMER
        self.vent.escribe("FILOSOFO {} TERMINO DE COMER".format(self.id))

        print("FILOSOFO {} suelta tenedor {} y {}".format(self.id, self.id,(self.id+1)%N))
        self.vent.tenedores[self.id].config(bg="grey", fg="white")
        self.vent.tenedores[(self.id-1)%N].config(bg="grey", fg="white")

        self.comida+=1
        self.vent.caja[self.id].delete(0,END)
        self.vent.caja[self.id].insert(0,self.comida)

    def run(self):
        self.vent.labels[self.id].config(bg="pink")
        for i in range(random.randint(1,5)):
            self.pensar() #EL FILOSOFO PIENSA
            self.tomar() #AGARRA LOS TENEDORES CORRESPONDIENTES
            self.comer() #COME
            self.soltar() #SUELTA LOS TENEDORES
            self.vent.labels[self.id].config(bg="pale green")
        self.vent.escribe("FILOSOFO {} HA FINALIZADO".format(self.id))
        self.vent.labels[self.id].config(bg="red")