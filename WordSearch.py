# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:47:14 2022

@author: preth
"""

            
from tkinter import *

class TrieNode:

    def __init__(self, value):
        self.value = value
        self.children = []
        self.complete = None

    def add(self, child):
        self.children.append(child)

    def get_child(self, value):
        for child in self.children:
            if child.value == value:
                return child
        return None

    def __str__(self):
        return str(self.value)


class Trie:
    def __init__(self, l=None):
        self.root = TrieNode('')
        if l != None:
            self.add_to_trie(l)
    def add_to_trie(self, l): 
        for word in l:
            current_node = self.root
            for letter in list(word):
                next_node = current_node.get_child(letter)
                if next_node == None:
                    next_node = TrieNode(letter)
                    current_node.add(next_node)
                current_node = next_node
            current_node.complete = word

file = open("words.txt", 'r')
words = []
for word in file:
    if len(word) < 1:
        continue
    words.append(word[:-1])
trie = Trie()
trie.add_to_trie(words)

def solve_word_search(board, trie=trie):
    ans = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            ans.update(search_words(board, i, j, trie))
    return ans

def search_words(board, i, j, trie):

    ck1={"u":[-1,0],"d":[1,0],"l":[0,-1],"r":[0,1],"ul":[-1,-1],"ur":[1,0],"dl":[1,-1],"dr":[1,1]}
    ck2={(1,1):"ul",(1,0):"u",(1,-1):"ur",(0,1):"l",(0,-1):"r",(-1,1):"dl",(-1,0):"d",(-1,-1):"dr"}
    solutions = set()
    offset=None
    stack = []

    stack.append((i, j, trie.root, board, offset))
    while len(stack) > 0:
        curr_letter = stack.pop()
        curr_node = curr_letter[2]
        original=[curr_letter[0],curr_letter[1]]
        neighbors = find_neighbors(board, curr_letter[0], curr_letter[1])
        if(curr_letter[4]!=None):
            value=ck1[curr_letter[4]];
            final=(original[0]+value[0],original[1]+value[1])
            if (final in neighbors):
                neighbors=[[final[0],final[1]]]
            else:
                neighbors=[]

        for i in range (len(neighbors)):
            x = neighbors[i][0]
            y = neighbors[i][1]
            board_copy = copy_matrix(curr_letter[3])
            child = curr_node.get_child(board_copy[x][y])
            if not child:
                continue

            if child.complete:
                solutions.add(child.complete)
            board_copy[x][y] = None
            neighbour_list=[x,y]
            diff=(original[0]-neighbour_list[0],original[1]-neighbour_list[1])
            keys=list(ck2.keys())
            for i in keys:
                if(diff==i):
                    offset=ck2[i];
            stack.append((x, y, child, board_copy, offset))
    return solutions

def find_neighbors(mat, i, j):

    rows = len(mat)
    cols = len(mat[0])
    
    row_start = max(0, i-1)
    row_end = min(rows, i+2)

    col_start = max(0, j-1)
    col_end = min(cols, j+2)

    neighbors = []

    for x in range(row_start, row_end):
        for y in range(col_start, col_end):

            if x != i or y != j:
                neighbors.append((x, y))

    return neighbors

def copy_matrix(mat):
    copy = []
    for row in mat:
        row_copy = []
        for col in row:
            row_copy.append(col)
        copy.append(row_copy)
    return copy

def start_procedure(board):
    result = solve_word_search(board)
    newres=[]
    for i in result:
        newres.append(i+"\n")
    final=" ".join(newres)
    resLabel=Label (root,text=final)
    resLabel.pack()
    #print(result)
    
if __name__ == "__main__":
    root=Tk()
    root.title("WORD SEARCH")
    root.geometry("400x400")


    with open('matrix.txt') as f:
        lines = [line for line in f]
     
    lst=[]
    # removing the new line characters
    with open('matrix.txt') as f:
        lines = [line.rstrip() for line in f]
        for i in lines:
            lst.append(i.split())
    board=lst
    string=[]
    for i in lst:
        for j in i:
            string.append(str(j))
        string.append("\n")
    #print(string)
    grid=" ".join(string)
    l=Label(root,text=grid)
    l.place(anchor=NW)
    b1=Button(root,text="",command=start_procedure(board))
    b1.place(relx=0,x=-2,y=2,anchor=NE)
    root.mainloop()

   
