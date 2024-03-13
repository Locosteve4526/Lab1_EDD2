#import graphviz
from typing import Any, List, Optional, Tuple,Literal
from pprint import pprint

FactorE = Literal[-2, -1, 0, 1, 2]
class Node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.altura=1
        self.FE=0
        
        

class Tree:

    def __init__(self, root: "Node" = None) -> None:
        self.root = root
    

class AVL(Tree):


    def __init__(self, root: "Node" = None) -> None:
        super().__init__(root)

    def FacEqui(self,node:"Node") -> int:
        if node is None :
            return 0
        node.FE=self.altura(node.right)-self.altura(node.left)
        return node.FE
    
    

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
            
    @staticmethod
    def SL(node: "Node")-> "Node":
        aux=node.right
        node.right=aux.left
        aux.left=node
        return aux
    @staticmethod
    def SR( node: "Node")->"Node":
        aux=node.left
        node.left=aux.right
        aux.right=node
        return aux
        
    def DRL(self,node: "Node"):
        node.right=self.SR(node.right)
        return self.SL(node)
    
    def DLR(self,node: "Node"):
        node.left=self.SL(node.left)
        return self.SR(node)

       
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
    
    def autobalance(self, node: "Node") -> "Node":
        if node is None:
            return None

        node.left = self.autobalance(node.left)
        node.right=self.autobalance(node.right)
        self.altura(node)
        self.FacEqui(node)
        

        if node.FE == -2:
            if node.left.FE < 0:
                print("Balancing node:", node.data)
                print("Before balancing:")
                self.print_tree(node)
                node = self.SR(node)
                self.FacEqui(node.right)
                print("Se hizo un simple righ")
            elif node.left.FE > 0:
                print("Balancing node:", node.data)
                print("Before balancing:")
                self.print_tree(node)
                node = self.DLR(node)
                self.FacEqui(node.right)
                self.FacEqui(node.left)
                print("Se realizo un double left right")
        elif node.FE == 2:
            if node.right.FE > 0:
                print("Balancing node:", node.data)
                print("Before balancing:")
                self.print_tree(node)
                node = self.SL(node)
                self.FacEqui(node.left)
                print("Se realizo un simple left")
            elif node.right.FE < 0:
                print("Balancing node:", node.data)
                print("Before balancing:")
                self.print_tree(node)
                node = self.DRL(node)
                self.FacEqui(node.right)
                self.FacEqui(node.left)
                print("Se realizo un double right left")
                
        
        self.altura(node)
        self.FacEqui(node)
        return node


    def print_tree(self, node: "Node", level=0, prefix="Root:") -> None:
        if node is not None:
            print(" " * (level * 4) + prefix, node.data, f"(FE: {node.FE}, Altura: {node.altura})")
            self.print_tree(node.left, level + 1, prefix="L:")
            self.print_tree(node.right, level + 1, prefix="R:")


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
                self.print_tree(self.root)
                return True
            return False

    def delete(self, elem: Any, mode: bool = True) -> bool:
        p, pad = self.search(elem)
        if p is not None:
            if p.left is None and p.right is None:
                if p == pad.left:
                    pad.left = None
                else:
                    pad.right = None
                del p
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
            else:
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
T.postorder()


