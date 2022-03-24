from random import randint
from BoardClasses import Move
from BoardClasses import Board
from copy import deepcopy
import math


# Mengchen Xu ID:61281584
# Yang Tang ID: 53979886

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

	def __init__(self,col,row,p):
		self.col = col
		self.row = row
		self.p = p
		self.board = Board(col,row,p)
		self.board.initialize_game()
		self.color = ''
		self.opponent = {1:2,2:1}
		self.color = 2


	def calc_dis(self,x1:int,y1:int,x2:int,y2:int):
		return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
  

	def all_checkers(self,board):
		half_row=int((self.row)/2)
		w=0
		b=0
		wl=[]
		bl=[]
		for i in range(0,self.col):
			for j in range(0,half_row):
				checker = board.board[j][i]
				if checker.color == "B":
					bl.append((j,i))
					b+=5+j
					if checker.is_king:
						b+=10 +self.row
				elif checker.color == "W":
					wl.append((j,i))
					w+=7+j
					if checker.is_king:
						w+=10 +self.row
		for i in range(0,self.col):
			for j in range(half_row,self.row):
				checker = board.board[j][i]
				if checker.color == "W":
					wl.append((j,i))
					w+=5+j
					if checker.is_king:
						w+=10 +self.row
				elif checker.color == "B":
					bl.append((j,i))
					b+=7+j
					if checker.is_king:
						b+=10 +self.row
		return w,b,wl,bl


	def heuristic_function(self,board):
		dis=0
		w=self.all_checkers(board)[0]
		b=self.all_checkers(board)[1]
		moves1=board.get_all_possible_moves(1)
		moves2=board.get_all_possible_moves(2)
		if self.color==1:
			for i in range(len(moves1)):
				for j in range(0,len(moves1[i])):
					for u in self.all_checkers(board)[2]:
						dis+=self.calc_dis(moves1[i][j][0][0],moves1[i][j][0][1],u[0],u[1])
            
			return w - b - dis
		else:
			for i in range(len(moves2)):
				for j in range(0,len(moves2[i])):
					for u in self.all_checkers(board)[-1]:
						dis+=self.calc_dis(moves2[i][j][0][0],moves2[i][j][0][1],u[0],u[1])
			return b- w - dis



	def determine_Color(self):
		if self.color == 1:
			return [1,2]
		else:
			return [2,1]


	def minimaxValue(self,depth,maximizingPlayer,moves,board,color, alpha, beta):
		if color ==1 and maximizingPlayer:
			colos=[1,2]
		elif color ==2 and maximizingPlayer:
			colos=[2,1]
		elif color ==1 and not maximizingPlayer:
			colos=[2,1]
		else:
			colos=[1,2]
		if depth == 0:
			return self.heuristic_function(board)
		else:
			if maximizingPlayer:            
				ans = -1*math.inf
				for i in range(len(moves)):
					for j in range(0,len(moves[i])):
						move = moves[i][j]
						board.make_move(move,colos[0])
						ans = max(ans, self.minimaxValue(depth-1, False,board.get_all_possible_moves(colos[1]),board,colos[1], alpha, beta))
						board.undo()
						if ans > alpha:
							alpha = ans
						if beta <= alpha:
							break
				return ans
	
			else:	
				ans = math.inf
				for i in range(len(moves)):
					for j in range(0,len(moves[i])):
						move = moves[i][j]
						board.make_move(move,colos[1])
						ans = min(ans, self.minimaxValue(depth-1, True,board.get_all_possible_moves(colos[0]),board,colos[0], alpha, beta))
						board.undo()
						if ans < beta:
							beta=ans
						if beta <= alpha:
							break
				return ans




	def find(self,moves,depth):
		bestValue = 1000
		movei=-1
		movej=-1
		for i in range(len(moves)):
			for j in range(0,len(moves[i])): 

				move = moves[i][j]
				self.board.make_move(move, self.color) 
				if(self.color == 1):
					value = self.minimaxValue(depth,False,self.board.get_all_possible_moves(2),self.board,2, -99999, 99999) 

				else:
					value = self.minimaxValue(depth,False,self.board.get_all_possible_moves(1),self.board,1, -99999, 99999)
				self.board.undo()
				if (value < bestValue):
					movei=i
					movej=j
					bestValue = value
		return [movei,movej]
	


	def get_move(self,move):
		if len(move) != 0:
	
			self.board.make_move(move,self.opponent[self.color])
		else:
			self.color = 1
	
		moves = self.board.get_all_possible_moves(self.color)
	
		indexes = self.find(moves,3)
		move = moves[indexes[0]][indexes[1]]
		self.board.make_move(move,self.color)
		return move


    
        
        
        

        
