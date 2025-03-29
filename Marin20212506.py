"""
Práctica 2: Sistema Respiratorio

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Marin Paredes Leslie Avelladith
Número de control: 20212506
Correo institucional: l20212506@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m 
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,30,1E-3,6,3
N = round((tend-t0)/dt) + 1 #veces de solucion numerica, numeros enteros
t = np.linspace(t0,tend,N) #linea de tiempo de 0,10
u1 = 2.5*np.sin(m.pi/2*t) #respiracion normal
u2 = 1.5*np.sin(m.pi*t) # Respiracion anormal

#arreglo de todas las señales
u = np.stack((u1,u2), axis=1) 
signal=['normal','taquipnea']

def sys_respiratorio(RP,CL):

# Componentes del circuito RLC y función de transferencia
    RC = 1 # CALCULAR LA RESISTENCIA     TODO DENTRO DE LA FUNCIÓN DEBE IR CON TAB
    LC = 0.01 #
    CS = 0.005 #PROPONER CAPACITOR
    CW = 0.2

    alpha3 = CL*CS*LC*RP*CW
    alpha2 = CL*CS*LC + CL*LC*CW + CS*LC*CW + CL*CS*RC*RP*CW
    alpha1 = CL*CS*RC + CL*RC*CW + CS*RC*CW + CL*RP*CW
    alpha0 = CL + CW

#funcion de transferencia viene con denominador y numerador
    num = [alpha0] #sacado de la funcion PA(S)/Pao(S) = -->1<-- / CLS^2+RCS+1
    den = [alpha3,alpha2,alpha1,alpha0] #S2, S, CONSTANTE si fuera cubica sería S3, S2, S, CONSTANTE 1 / --> CLS^2+RCS+1 <--

#aplicacion de la funcion de transferencia
    sys = ctrl.tf(num,den)
    return sys #despliegue de funcion de transferencia

# Funcion de transferencia: Individuo saludable [control]
RP, CL = 0.5,0.2
sysS = sys_respiratorio(RP, CL)
print('Individuo sano [control]:')
print(sysS)

# Funcion de transferencia: Individuo enfermo [caso]
RP, CL = 7.5,0.4
sysE = sys_respiratorio(RP, CL)
print('Individuo enfermo [caso]:')
print(sysE)

def plotsignals(u,sysS,sysE,sysPID,signal):
    
    fig = plt.figure() #1era figura codigo basado en page 87 Inicializa la figura
    # plt.plot(t,u,'-',color=[],label = '$P_{ao}(t)') #Grafica la entrada
    
    # P A C I E N T E     S A N O       [ F I G U R A ]
    ts,Vs =ctrl.forced_response(sysS,t,u,x0)
    plt.plot(t,Vs,'-',color = [0.8,0.3,0.6],
             label='$P_A(t): Control$')
    
    # P A C I E N T E     E N F E R M O       [ F I G U R A ]
    ts, Ve = ctrl.forced_response(sysE,t,u,x0)
    plt.plot(t,Ve,'-',color = [0.3,0.8,0.8],
             label='$P_A(t): Caso$')
    
    # C O N T R O L     P I D      [ F I G U R A ]
    ts,pid = ctrl.forced_response(sysPID,t,Vs,x0)
    # plt.plot(t,u3,'-', linewidth=3, color = [0.8,0.3,0.6], label = 'Ve(t)' ) 
    plt.plot(t,pid,':', linewidth=3, color = [0.1,0.3,0.9], 
             label= '$PA(t): Tratamiento$')
    
    plt.grid(False)
    plt.xlim(0,30)
    plt.ylim(-3,3)
    plt.xticks(np.arange(0, 31, 2))
    plt.yticks(np.arange(-3, 3.5, 0.5))
    plt.xlabel('$t$ [s]')
    plt.ylabel('$PA(t)$ [V]')
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol=4,
               fontsize = 8, frameon = False)
    plt.show()
    
    ## Almacenamiento de figura 
    fig.set_size_inches(w,h)
    fig.tight_layout()
    namepng = 'python_' + signal + '.png'
    namepdf = 'python_' + signal + '.pdf'
    fig.savefig(namepng, dpi = 600,bbox_inches = 'tight')
    fig.savefig(namepdf, bbox_inches = 'tight')
    
def tratamiento(Cr, Re,Rr,Ce,sysE):
    numPID = [Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    X = ctrl.series(PID,sysE)
    sysPID = ctrl.feedback(X, 1, sign = -1) #Cierra el lazo, hace una comparativa 
    return sysPID
    
    # Controlador para la respiración normal 
    # Rendimiento del controlador 
    # kP: 15.8954
    # kI: 452.1208
    # kD: 0.042897
    # Settling time: 0.0994   
    # Overshoot: 9.37%
    # Peak: 1.09 
    # Cr = 1E-6 # Proponer un valor
    
Cr = 1E-6
kP = 15.8954
kI = 452.1208
kD = 0.042897
Re = 1 /(kI*Cr)
Rr = kP*Re
Ce = kD/Rr
    
sysPID = tratamiento(Cr, Re, Rr, Ce, sysE)
    
plotsignals(u1,sysS, sysE, sysPID, 'normal')
    
    # Controlador para la respiración anormal [taquipnea]
plotsignals(u2,sysS, sysE, sysPID, 'taquipnea')
    
   
  