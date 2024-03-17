import graphviz as gv
from typing import Any, List, Optional, Tuple
from pprint import pprint
from collections import deque

class Node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.altura=1 #Este atributo tiene la altura
        self.FE=0 #Este atributo tiene el facto de equilibrio del nodo

#Añadi la clase cola del profesor     
class Queue:

    def __init__(self) -> None:
        self.queue: List[Any] = []

    def add(self, elem: Any) -> None:
        self.queue.append(elem)

    def remove(self) -> Any:
        return self.queue.pop(0)

    def is_empty(self) -> bool:
        return len(self.queue) == 0     

class Tree:

    def __init__(self, root: "Node" = None) -> None:
        self.root = root
        
    

class AVL(Tree):


    def __init__(self, root: "Node" = None) -> None:
        super().__init__(root)
        self.n=0

    #En esta funcion se calcula el factor de equilibrio de un nodo
    #Apartir de la altura de los subarboles derecho e izquierdo
    def FacEqui(self,node:"Node") -> int:
        if node is None :
            return 0
        node.FE=self.altura(node.right)-self.altura(node.left)
        return node.FE
    
    #Aqui se calcula la altura de un nodo
    def altura(self,node:"Node") -> int:
        if node is None:
            return 0
        node.altura= 1 + max(self.altura(node.left), self.altura(node.right))
        return node.altura

    def postorder(self) -> None:
        self.postorder_r(self.root)

    def postorder_r(self, node: "Node") -> None:
        if node is not None:
            self.postorder_r(node.left)
            self.postorder_r(node.right)
            print(node.data, end = ' ')
            print("Mi factor E es",node.FE)

    #Aqui estan todos los metodos de las rotaciones del arbol AVL

    #Esta es simple izquierda       
    @staticmethod
    def SL(node: "Node")-> "Node":
        aux=node.right
        node.right=aux.left
        aux.left=node
        return aux
    
    #Esta es simple derecha
    @staticmethod
    def SR( node: "Node")->"Node":
        aux=node.left
        node.left=aux.right
        aux.right=node
        return aux
        
    #Esta es doble derecha izquierda
    def DRL(self,node: "Node"):
        node.right=self.SR(node.right)
        return self.SL(node)
    # Y esta es doble izquierda derecha
    def DLR(self,node: "Node"):
        node.left=self.SL(node.left)
        return self.SR(node)

    #metodo de busqueda
    def search(self, elem: Any) -> Tuple[Optional["Node"], Optional["Node"]]:
        p, pad = self.root, None
        while p is not None:
            if elem == p.data:
                return p, pad
            elif elem < p.data:
                pad = p
                p = p.left
            else:
                pad = p
                p = p.right
        return p, pad
    
    #Funcion para calcular el padre
    def pad(self,elem:Any) -> Tuple[Optional["Node"], Optional["Node"]]:
        p,pad=self.search(elem)
        if elem == self.root.data:
            print("El elemento no tiene padre pues es la raiz")
        else:    
            if p is not None:
                print("Yo",pad.data ,"soy el padre de",p.data)
                return p,pad
            else:
                print("No esta en el arbol ")
                return None,None
        
    #funcion para calcular el tio
    def tio(self,elem:Any)->"Node":
        pad,abu=self.abu(elem)
        if abu is not None:
            if abu.left==pad and abu.right is not None:
                print("Yo",abu.right.data,"soy el tio de ",elem)
                return abu.right
            elif abu.right==pad and abu.left is not None:
                print("Yo",abu.left.data,"soy el tio de",elem)
                return abu.left
            else:
                print(elem,"No tiene tio")
        else:
            print(elem,"es la raiz y no tiene tio")
            return None
        
    #Funcion para calcular el abuelo
    def abu(self,elem:Any)->Tuple[Optional["Node"], Optional["Node"]]:
        p,pad=self.pad(elem)
        if pad is not None:
            pad,abu=self.pad(pad.data)
            if abu is not None:
                print("Yo",abu.data, "soy el abuelo de",elem)
                return pad,abu
            else:
                print(elem,"No tiene abuelo")
                return None, None
        else:
            print(elem,"No tiene abuelo")
            return None, None
        
    #Y este es el metodo de autobalanceo, de forma recursiva
    def autobalance(self, node: "Node") -> "Node":
        if node is None:
            return None
        #Aqui llamamos de nuevo a el metodo, pasandole el hijo izquieredo, luego derecho
        #Para luego realizar el balanceo. Siguiendo un estilo de postorden
        node.left = self.autobalance(node.left)
        node.right=self.autobalance(node.right)
        self.altura(node)
        self.FacEqui(node)
        
        #Aqui empezamos a revisar los factores de balanceo
        #Para poder saber si es necesario balancear el arbol
        if node.FE == -2:
            if node.left.FE < 0:
                #Este seria el caso de simple derecha (-2,-1)
                print("Balancing node:", node.data)
                print("Before balancing:")
                node = self.SR(node)
                self.FacEqui(node.right)
                print("Se hizo un simple righ")
            elif node.left.FE > 0:
                #Este es el caso de doble izquierda derecha (-2,1)
                print("Balancing node:", node.data)
                print("Before balancing:")
                node = self.DLR(node)
                self.FacEqui(node.right)
                self.FacEqui(node.left)
                print("Se realizo un double left right")
        elif node.FE == 2:
            if node.right.FE > 0:
                #Ese es el caso de simple izquierda (2,1)
                print("Balancing node:", node.data)
                print("Before balancing:")
                node = self.SL(node)
                self.FacEqui(node.left)
                print("Se realizo un simple left")
            elif node.right.FE < 0:
                #Y este el caso de doble derecha izquierda (2,-1)
                print("Balancing node:", node.data)
                print("Before balancing:")
                node = self.DRL(node)
                self.FacEqui(node.right)
                self.FacEqui(node.left)
                print("Se realizo un double right left")       
        self.altura(node)
        self.FacEqui(node)
        return node

    #metodo de insercion
    def insert(self, elem: Any) -> bool:
        to_insert = Node(elem)
        if self.root is None:
            self.root = to_insert
            return True
        else:
            p, pad = self.search(elem)
            if p is None:
                if elem < pad.data:
                    pad.left = to_insert
                else:
                    pad.right = to_insert
                self.root=self.autobalance(self.root)
                print("Node inserted:", elem)
                self.n+=1
                return True
            return False
        
    def delete(self, elem: Any, mode: bool = True) -> bool:
        # Buscar el nodo a eliminar y su padre
        p, pad = self.search(elem)

        # Verificar si el nodo a eliminar existe
        if p is not None:
            # Caso 1: El nodo a eliminar es una hoja
            if p.left is None and p.right is None:
                if p == pad.left:
                    pad.left = None
                else:
                    pad.right = None
                del p
                # Caso 2: El nodo a eliminar tiene solo un hijo
            elif p.left is not None and p.right is None:
                if p == pad.left:
                    pad.left = p.left
                else:
                    pad.right = p.left
                del p
            elif p.left is None and p.right is not None:
                if p == pad.left:
                    pad.left = p.right
                else:
                    pad.right = p.right
                del p
                
            # Caso 3: El nodo a eliminar tiene dos hijos
            else:
                if p.left.right is None and p.left.left is None:
                    mode=False
                # Utilizar el predecesor o sucesor
                if mode:
                    pred, pad_pred = self.__pred(p)
                    p.data = pred.data
                    if pred.left is not None:
                        if pad_pred == p:
                            pad_pred.left = pred.left
                        else:
                            pad_pred.right = pred.left
                    else:
                        if pad_pred == p:
                            pad_pred.left = None
                        else:
                            pad_pred.right = None
                    del pred
                else:
                    sus, pad_sus = self.__sus(p)
                    p.data = sus.data
                    if sus.right is not None:
                        if pad_sus == p:
                            pad_sus.right = sus.right
                        else:
                            pad_sus.left = sus.right
                    else:
                        if pad_sus == p:
                            pad_sus.right = None
                        else:
                            pad_sus.left = None
                    del sus         
            # Balancear el árbol después de eliminar el nodo
            self.autobalance(pad)
            # Imprimir el árbol para verificar
            self.graphTree()
            return True
        return False



    def __pred(self, node: "Node") -> Tuple["Node", "Node"]:
        p, pad = node.left, node
        while p.right is not None:
            p, pad = p.right, p
        return p, pad

    def __sus(self, node: "Node") -> Tuple["Node", "Node"]:
        p, pad = node.right, node
        while p.left is not None:
            p, pad = p.left, p
        return p, pad
    

    #Funcion de recorrido por niveles
    def Recorrido_por_Niveles(self) -> None:
        if self.root is not None:
            queue = Queue()
            queue.add(self.root)
            self._Recorrido_RC(queue)

    def _Recorrido_RC(self, queue: "Queue") -> None:
        while not queue.is_empty():
            node = queue.remove()
            print(node.data, end=" ")
            if node.left:
                queue.add(node.left)
            if node.right:
                queue.add(node.right)

    #Aquí genera como tal el gráfico 
    def graphTree(self) -> None:
        tree = gv.Digraph()
        self._graph(self.root, tree)
        tree.render("avl_tree", format='png', view=True, cleanup=True)

    #Construye recursivamente la representación visual
    def _graph(self, root: Optional["Node"], tree: gv.Digraph, level: int = 0) -> None:
        if root is not None:
            tree.node(f"{root.data}", label=f"{root.data} (Nivel: {level})")

            if root.left:
                tree.edge(f"{root.data}", f"{root.left.data}")
                self._graph(root.left, tree, level + 1)

            if root.right:
                tree.edge(f"{root.data}", f"{root.right.data}")
                self._graph(root.right, tree, level + 1)
    

def generate_sample_abb() -> "AVL":
    tree = AVL()
    print(tree.insert(8))
    print(tree.insert(9))
    print(tree.insert(7))
    print(tree.insert(4))
    print(tree.insert(12))
    print(tree.insert(1))
    print(tree.insert(2))
    print(tree.insert(5))
    print(tree.insert(3))
    print(tree.insert(6))
    print(tree.insert(10))
    print(tree.insert(15))
    print(tree.insert(0))
    print(tree.insert(20))
    print(tree.insert(6))
    

    return tree
T = generate_sample_abb()
T.Recorrido_por_Niveles()
#T.delete(10)
#T.delete(8)
#T.pad(15)
#T.abu(15)
#T.tio(3)
T.graphTree()





