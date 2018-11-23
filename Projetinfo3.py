from math import*
import random as RND

def CreeMonde(L): # OK
    M=[[0 for i in range(L)] for j in range(L)]
    #Matrice vide au début 
    for i in range(L):
        M[i][i]=0
        for j in range(i):
            # Création d'une matrice symétrique (qui illustre les différents chemins possibles)
            M[i][j]=RND.randint (0,1)
            M[j][i]=M[i][j]     
    return(M)

def voisins(i,M): # OK
    #On prend un point dans M
    L=[]
    for j in range (len(M)):
        if M[i][j]==1:  # signifie que i et j sont reliés
            L=L+[j]
    return L #liste des voisins immédiat de i 
    
def voisinssauf(i,M,v): # OK
    #Récurrence des voisins (on somme tous les voisins des i points)
    #( une seule apparition)
    L=[]
    for j in range(len(M)):
            if M[i][j]==1 and j not in v:
                L=L+[j]
    return L
    #on créait une liste contenant tous les voisins du point i qui n'appartiennent  pas à v
    
def composanteconnexe(M,x):
    # NE FONCTIONNE PAS CAR LE "p in L" DU FOR N'EST CALCULE
    # QU'AVEC LA VALEUR INITIALE DE L... PAS DE MISE A JOUR AU
    # FUR ET A MESURE QUE L EVOLUE
    #récurrence à faire sur tous les voisinssauf
    L=[x]
    for p in L:
        V=voisinssauf(p,M,L)
        #On prend un noeud, on fait voisinssauf sur ce noeud pour avoir
        # l'ensemble de ses voisins sauf lui
        L=L+V
        #On met ca dans une liste
    return L
    #Ensemble des noeuds pouvant etre atteints à partir du noeud x
    #On prend le noeud suivant et on recommence et on ajoute à la liste 

def composanteconnexePROF(M,x):
    L=[x]
    # On part de "x"
    i=0
    # "i" marque la position dans L de la valeur traitee
    while i<len(L):
        # Tant qu'on n'a pas epuise le contenu de L
        V=voisinssauf(L[i],M,L)
        L=L+V
        i=i+1
    return L

#on relie le point de départ à tous les autres noeuds dans le but de
#créer un monde formé par l'ensemble des composantes connexes de M
#(à partir du point de départ, on peut ainsi rejoindre la nourriture,
#ou qu'elle soit dans le monde M)

def PremierAbsent(C,M):
    # PROGRAMMEE PAR LE PROF => UTILE POUR MONDEENTIER
    # \exists i\in C tel que i\not\in M => renvoie i, sinon renvoie -1
    Presents=[n in C for n in range(len(M))]
    # Liste des valeurs de "n in C": True si oui, False si non
    if False in Presents:
        # False in Presents => il existe une valeur de M qui n'est pas dans C
        return(Presents.index(False))
        # On renvoie la premiere trouvee
    else:
        # sinon, on renvoie -1
        return(-1)
    
def MondeEntier(M):
    # Modifie M de façon qu'il ne comporte qu'une composante connexe
    if len(M)>0:
        C=composanteconnexePROF(M,0)
        i=PremierAbsent(C,M)
        while i!=-1:
            # IL RESTE DES NOEUDS NON ATTEIGNABLES
            M[max(C)][i]=1
            M[i][max(C)]=1
            C=composanteconnexePROF(M,0)
            i=PremierAbsent(C,M)

# STOP CONTROLE ICI

def fourmis(N,Fourmilière,Nourriture): # créations de N fourmis (au départ toutes dans la fourmilière
    éclaireuses=[]
    ouvrières=[]
    F=[]
    for k in range (N):
        if random()<=0.75:
            éclaireuses=éclaireuses+[[k,Fourmilière,0]]
            #[Numéro de la fourmis, Position initiale, elle cherche la nourriture]
        else:
            ouvrières=ouvrières+[[k,Fourmilière,0]]
            #[0=elle cherche la nourriture mais n'a pas le droit de bouger]
    F=[[éclaireuses],[ouvrières]]
    return F
    
#m=nombre de noeuds dans le monde N=nb total de fourmis          
def simulateur(m,N):
    Ph=[[0 for i in range(len(m))] for j in range (len(m))]#Matrice vide au début car pas de phéromone
    M=MondeEntier2(m)
    Fourmilière=RND.randint(0,len(M)-1)
    Nourriture=RND.randint(0,len(M)-1)
    F=fourmis(N,Fourmilière, Nourriture)
    éclaireuses=F[0]#toutes les éclaireuses
    Nb=0 # Nombre de fourmis qui ont trouvé la nourriture
    Tour=0
    while Nb==0:
        Tour=Tour+1
        for k in range (len(éclaireuses)): # pour chaque fourmis éclaireuse
            dpt=éclaireuses[k][1]# k= une des fourmis; 1= SA POSITION en un noeud donné
            arr=RND.choice(voisins(dpt,M))#choix d'un noeud parmis les noeuds voisins à partir de la fourmilière ou du noeud donné
            éclaireuses[k][1]=arr # elle est passée au noeud suivant
            if arr==Fourmilière: #Première fourmis éclaireuse arrivée à la fourmilière==> Stopper le while
                Nb=Nb+1
             # (1) l'éclaireuse a trouvé la nourriture => elle cherche la fourmilière
            if éclaireuses[k][1]==Nourriture:
                éclaireuses[k][2]=1
            # (2)l'éclaireuse retourne à la fourmilière => phéromone
            if éclaireuses[k][2]==0:
                q=0
            else:
                q=11 #dépot de phéromone
            #(3) dépot phéromone ou pas sur chemin
            Ph[dpt][arr]=Ph[dpt][arr]+q
            Ph[arr][dpt]=Ph[dpt][arr]
        if Tour%100==0:
            print(Ph)

    return Ph #matrice avec les phéromones
        
    

    
              



              

def Phéromone(M):
    P=[[0 for i in range(len(M))] for j in range (len(M))]#Matrice vide au début car pas de phéromone
    return P    



#Il faut placer la fourmilière et la nourriture dans le monde de sorte qu'il y ait une distance assez importante
#Il faut créer une liste de fourmis
#Chaque fourmis =[n°,noeud, nature(éclaireuse?),destination]
#Créer une matrice P vide représentant la présence ou non de phéromone entre les différents noeuds
#A chaque noeud où se trouve la fourmis, on fait ''random()'' pour qu'elle prenne une chemin aléatoire parmi les chemins disponibles

       























def population(n,S,c):
      #   ON CRÉAIT UNE FOURMIS ÉCLAIREUSE f, positionnées à la fourmilière (S)
    P=[('éclaireuse',S)for i in range (n)] #on créé une liste de n fourmis éclaireuses
    n=len(P)
    for k in range (n):
        RND.choice
        
