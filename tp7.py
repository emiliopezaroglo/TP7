import matplotlib
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
# Définition des classes
#-------------------------------------------------------------------------------

class Proie():
    vie = 30 # durée de vie maximale d'une proie
    age_division = 5 # âge minimal pour division

    def __init__(self, x, y, age):
        self.x = x # position en x (indice)
        self.y = y # position en y (indice)
        self.age = age 
    
        
class Pred():
    vie = 100 # durée de vie maximale d'un prédateur
    age_division = 20 # âge minimal pour division
    reserves_division = 10 # réserves minimales pour division
    reserves_satiete = 20 # réserves maximales
    
    def __init__(self, x, y, age, reserves):
        self.x = x
        self.y = y
        self.age = age
        self.reserves = reserves
		
            
#-------------------------------------------------------------------------------
# Définition des fonctions
#-------------------------------------------------------------------------------
        
def placement_initial(nbr_ind, type_ind, type_autre_ind):
    """ Fonction qui prend en arguments le nombre et le type d'individu à placer ainsi que le type d'individu à ne pas placer.
    Retourne la grille et les dictionnaires pred_ref et proie_ref ajustés """
    
    for i in range(nbr_ind): # boucle sur le nombre d'individus à placer
        x = np.arange(0,50,1) # liste des positions possibles (1D)
        pos = np.random.choice(x,size=(2),replace=False) # retourne une liste (2,) d'entiers aléatoires entre 0 et 49 sans répétition
        pos = pos[0],pos[1] # tuple
        
        if grille[pos] == None: # absence d'individu
            grille[pos] = type_ind # ajoute le type d'individu à la grille
            if type_ind == type_proie:
                age = np.random.randint(Proie.vie+1)
                proie_ref[pos] = Proie(pos[0], pos[1], age) # crée une instance de proie et l'ajoute au dictionnaire
            elif type_ind == type_pred:
                age = np.random.randint(Pred.vie+1)
                pred_ref[pos] = Pred(pos[0], pos[1],age, reserves0) # crée une instance de pred et l'ajoute au dictionnaire
                
        elif grille[pos] == type_autre_ind: # individu de l'autre espèce
            grille[pos] += type_ind # ajoute le type d'individu à la grille sans enlever l'autre
            if type_ind == type_proie:
                age = np.random.randint(Proie.vie+1)
                proie_ref[pos] = Proie(pos[0], pos[1], age)
            elif type_ind == type_pred:
                age = np.random.randint(Pred.vie+1)
                pred_ref[pos] = Pred(pos[0], pos[1],age, reserves0)
                
    return grille, pred_ref, proie_ref
            
def voisinage(objet):
    """Fonction qui prend en argument un objet (proie ou pred) et retourne un dictionnaire 
    ayant pour clés les coordonnées de 5 points voisins et pour valeurs l'état de ces points (None, 1 ou 2)"""
    
    x, y = objet.x, objet.y # coordonnées de l'objet
    pts_etats_voisins = {} # Initialisation du dictionnaire
    L = [] 
    

    if (x,y) == (0,0): # coin inférieur gauce
        pts_voisins = [[x+1,y], [x+1,y+1], [x,y+1], [49,y], [49,y+1], [49,49], [0,49], [x+1,49]]
    elif (x,y) == (49,0): # coin inférieur droit
        pts_voisins = [[x-1,y],[x-1,y+1],[x,y+1], [0,0], [0,1], [49,49], [48,49], [0,49]]
    elif (x,y) == (0,49): # coin supérieur gauche
        pts_voisins = [[x+1,y],[x+1,y-1],[x,y-1], [0,0], [1,0], [49,49], [49,48], [49,0]]
    elif (x,y) == (49,49): # coin supérieur droit
        pts_voisins = [[x-1,y],[x-1,y-1],[x,y-1], [49,0], [48,0], [0,49], [1,49], [0,0]]
    
    elif x == 0 : # bordure gauche
        pts_voisins = [[x+1,y],[x+1,y-1],[x+1,y+1],[x,y-1],[x,y+1], [49,y], [49,y+1], [49,y-1]]
    elif x == 49: # bordure droite
        pts_voisins = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1], [0,y], [0,y-1], [0,y+1]]
    elif y == 0: # bordure du bas
        pts_voisins = [[x+1,y],[x+1,y+1],[x-1,y],[x-1,y+1],[x,y+1], [x,49], [x-1,49], [x+1,49]]
    elif y == 49: # bordure du haut
        pts_voisins = [[x+1,y],[x+1,y-1],[x-1,y-1],[x-1,y],[x,y-1], [x,0], [x-1,0], [x+1,0]]
    else:
        pts_voisins = [[x+1,y],[x+1,y-1],[x+1,y+1],[x-1,y-1],[x-1,y],[x-1,y+1],
                       [x,y-1],[x,y+1]]

    while len(L) < 5: # on veut explorer uniquement 5 points
        randi = np.random.randint(len(pts_voisins)) # génère un entier entre 0 et le nombre de points voisins
        if randi in L: # point déjà explorer
            continue # on passe au prochain entier
        else: # point inexplorer
            L.append(randi) # on ajoute à L l'entier utilisé
            pt = pts_voisins[randi] # point explorer
            pts_etats_voisins[tuple(pt)] = grille[tuple(pt)] # ajout de la paire point-état au dictionnaire
    
    return pts_etats_voisins
    

def run(t):
    """ Fonction qui """
    
    global pred_xdata, pred_ydata, proie_xdata, proie_ydata, line1, line2, data_out
    
    # Tableaux initialisés à chaque itération
    pred_xdata, pred_ydata = [], [] # tableaux contenant les positions (x,y) des prédateurs
    proie_xdata, proie_ydata = [], [] # tableaux contenant les positions (x,y) des proies
    
    # ajustement du tableau de sortie
    data_out[t,0] = t # temps de l'itération
    data_out[t,1] = len(pred_ref) # nombre de prédateurs à ce temps
    data_out[t,2] = len(proie_ref) # nombre de proies à ce temps
    # enregistrement dans le fichier 'data.CSV' du tableau 'data_out'
    with open('data.CSV', 'w') as f:
	    np.savetxt(f, data_out, delimiter=',', header='t, pred, proie')
    
    
    # Ajustements relatifs aux prédateurs
    for pos, pred in pred_ref.copy().items():
        """ boucle sur une copie du dictionnaire des prédateurs afin
        que les modifications ne pertubent pas la boucle. 'pos' est un tuple 
	    et 'pred' une instance de Pred """
		
        pred_xdata = np.append(pred_xdata, pos[0])
        pred_ydata = np.append(pred_ydata, pos[1])
		
		
        # élimine les prédateurs trop agés et sans réserves
        if pred.age >= pred.vie or pred.reserves <= 0:
            pred_ref.pop(pos)
            grille[pos] = None 
            continue # on passe au prochain pédateur dans la 'for' boucle
		
        voisins = voisinage(pred)
		
        # génère de nouveaux prédateurs par division
        if pred.reserves >= Pred.reserves_division and pred.age >= Pred.age_division:
            for pt, etat in voisins.items():
                if etat != type_pred and etat != (type_proie + type_pred): # vérifie qu'il n'y a pas de prédateurs au point considéré
                    grille[pt] = type_pred
                    pred_ref[pt] = Pred(pt[0], pt[1], 0, pred.reserves/2)
                    pred.age = 0 
                    #pred.reserves /= 2
                    break # ne peut se produire qu'une fois par prédateur

        # vérifie s'il y a une proie à la position du prédateur et ajuste le cas échéant
        if pred.reserves < pred.reserves_satiete:
            if grille[pos] == type_proie + type_pred: # Il y a une proie sur la case du prédateur
                grille[pos] = type_pred # élimine la proie dans la grille
                pred.reserves += 1 
                proie_ref.pop(pos) # élimine la proie dans le dictionnaire des proies

        # vérifie s'il y a une proie à proximité et ajuste le cas échéant
        if pred.reserves < pred.reserves_satiete:
            for pt, etat in voisins.items():
                if etat == type_proie:
                    grille[pt] = type_pred # prédateur au point voisin
                    grille[pos] = None # None au point original du prédateur
                    pred_ref[pt] = pred # prédateur au point voisin
                    pred_ref.pop(pos) # plus de prédateur au point original
                    proie_ref.pop(pt) # plus de proie au point voisin
                    pred.reserves += 1 # incrémente la réserve du prédateur
                    break # ne peut manger qu'une proie par pas temporel

        pred.age += 1
        pred.reserves -= perte_par_cycle
        



    # Ajustements relatifs aux proies
    for pos, proie in proie_ref.copy().items(): # positions des proies
        
        proie_xdata = np.append(proie_xdata, pos[0])
        proie_ydata = np.append(proie_ydata, pos[1])

        # élimine les proies trop agées
        if proie.age >= proie.vie:
            proie_ref.pop(pos)
            grille[pos] = None 

        voisins = voisinage(proie)
        for pt, etat in voisins.items():
            if (etat == None or etat == type_pred) and proie.age >= Proie.age_division:
                if etat == None:
                    grille[pt] = type_proie
                elif etat == type_pred:
                    grille[pt] += type_proie

                proie_ref[pt] = Proie(pt[0], pt[1], 0)
                proie.age = 0
                break # une seule division par proie par temps
    
        proie.age += 1
        
    
    
    plt.title('t = ' + str(t))
    line1.set_data(pred_xdata, pred_ydata)
    line2.set_data(proie_xdata, proie_ydata)
    
    return line1, line2,

    

def init():
    """Fonction qui initialise les données à chaque itération"""
    line1.set_data([],[])
    line2.set_data([],[])
    return line1, line2,
    
            
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


def main():
    global grille, pred_ref, proie_ref, type_proie, type_pred, reserves0, perte_par_cycle, ax, pred_xdata, pred_ydata, proie_xdata, proie_ydata, line1, line2, n_pred, n_proie, data_out
    
    # Initialisation des constantes
    L = 50
    n_pred0 = 10
    n_proie0 = 200
    reserves0 = 6.
    perte_par_cycle = 0.5
    n_iter = 1000
    type_pred = 2
    type_proie = 1
    
    temps_simul = np.arange(n_iter) # liste des temps de simulation
    
    # Initialisation des dictionnaires contenant les positions des proies et prédateurs
    # Les positions sont les clés et les instances sont les valeurs
    pred_ref = {}
    proie_ref = {}
    
    # Initialisation du tableau du nombre de proies et prédateurs en fonction du temps
    data_out = np.empty((n_iter,3))
    
    # Initialisation de la grille
    grille = np.full((L,L), None)
    
    # Placement initiale des populations
    grille, pred_ref, proie_ref = placement_initial(n_pred0, type_pred, type_proie)
    grille, pred_ref, proie_ref = placement_initial(n_proie0, type_proie, type_pred)
    
   # figure
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-0.5,50)
    ax.set_ylim(-0.5,50)
    line1, = ax.plot([], [], 'rs', ms=5)
    line2, = ax.plot([], [], 'bo', ms=3)

    # animation
    anim = animation.FuncAnimation(fig, run, init_func=init, frames=temps_simul, interval=10, repeat=False)
	
    plt.show()
    
    plt.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\Pezar\\ffmpeg\\bin\\ffmpeg.exe'
    writer = animation.FFMpegWriter(fps=30)
    
    anim.save('simul.mp4', writer=writer)
    
    
    
    



if __name__ == '__main__':
    main()
