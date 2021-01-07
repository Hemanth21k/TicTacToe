import copy
class Game:
    
    def utilcheck(self,arr,winK):
        x=arr[0]
        tempx=0
        tempy=0
        for i in range(len(arr)-winK+1):
            x=arr[i]                                       
            for j in range(i,i+winK):
                if arr[j] == x:                        
                    if arr[j] == 'X':
                        tempx=tempx+1
                        if tempx == winK:
                            return -1
                    elif arr[j] == 'O':
                        tempy=tempy+1
                        if tempy == winK:
                            return 1
                else:
                    tempx = 0
                    tempy = 0
        return 0

    def utility(self,state,winK):
        board = copy.deepcopy(state)
        for i in range(len(board)):
            temp = self.utilcheck(board[i],winK)
            if temp != 0:
                return temp
        
        leftdiag = []
        rightdiag = []
        for i in range(len(board)):
            col = []
            for j in range(len(board)):
                col.append(board[j][i])
                if i == j:
                    leftdiag.append(board[i][j])
                    rightdiag.append(board[i][len(board)-j-1])
            temp=self.utilcheck(col,winK)
            if temp != 0:
                return temp
        temp = self.utilcheck(leftdiag,winK)
        if temp != 0:
            return temp
        temp = self.utilcheck(rightdiag,winK)
        if temp != 0:
            return temp
        wk=winK
        while wk<len(board):    
            l1=[]
            l2=[]
            l3=[]
            l4=[]
            count = 0
            for i in range(len(board)-wk):
                for j in range(wk):
                    count +=1
            count = count - wk
            for i in range(len(board)-wk):
                for j in range(wk):
                    if count != 0:
                        count-=1
                        continue
                    l1.append(board[i+j+1][j])
                    l2.append(board[j][i+j+1])
                    l3.append(board[len(board)-i-j-2][j])
                    l4.append(board[i+j+1][len(board)-j-1])
            temp=self.utilcheck(l1,winK)
            if temp != 0:
                return temp
            temp=self.utilcheck(l2,winK)
            if temp != 0:
                return temp
            temp=self.utilcheck(l3,winK)
            if temp != 0:
                return temp
            temp=self.utilcheck(l4,winK)
            if temp != 0:
                return temp
            wk=wk+1
        for i in range(len(board)):
            for j in range(len(board)):
                # There's an empty field, we continue the game
                if (state[i][j] is None):
                    return None
        return 0
    def actions(self,state,maxturn):
        actions = []
        board = copy.deepcopy(state)
        for i in range(len(state)):
            for j in range(len(state)):
                if board[i][j] is None:
                    temp = copy.deepcopy(board)
                    if maxturn:
                        actions.append((1,i,j))
                    else:
                        actions.append((0,i,j))            
        return actions
    def result(self,state,action):
        board = copy.deepcopy(state)
        if action[0] == 0:
            board[action[1]][action[2]] = 'X'
        if action[0] == 1:
            board[action[1]][action[2]] = 'O'
        return board
    def check(self,arr,winK):
        total_val=0
        for i in range(len(arr)-winK+1):
            val=0                                       
            for j in range(i,i+winK):
                if arr[j] == 'X':
                    if val >=1:
                        val = 0
                    elif val <= -1:
                        val = val * 10
                    else:
                        val=-1
                elif arr[j] == 'O':
                    if val <= -1:
                        val = 0
                    elif val >=1:
                        val = val * 10
                    else:
                         val=1
            total_val=total_val+val
        return total_val
    

    def tictactoeHeuristic(self,state,winK):
        board = copy.deepcopy(state)
        val = 0

        for i in range(len(state)):
            val = val + self.check(board[i],winK)
        for i in range(len(state)):
            l = []
            for j in range(len(state)):
                l.append(board[j][i])
            val = val + self.check(l,winK)

            
        l=[]
        l1=[]
        for i in range(len(board)):
            for j in range(len(board)):
                if i == j :
                    l.append(board[i][j])
                    l1.append(board[i][len(board)-1-j])
        
        val = val + self.check(l,winK)
        val = val + self.check(l1,winK)
        wk=winK
        while wk<len(board):    
            l1=[]
            l2=[]
            l3=[]
            l4=[]
            count = 0
            for i in range(len(board)-wk):
                for j in range(wk):
                    count +=1
            count = count - wk
            for i in range(len(board)-wk):
                for j in range(wk):
                    if count != 0:
                        count-=1
                        continue
                    l1.append(board[i+j+1][j])
                    l2.append(board[j][i+j+1])
                    l3.append(board[len(board)-i-j-2][j])
                    l4.append(board[i+j+1][len(board)-j-1])
            val = val + self.check(l1,winK)
            val = val + self.check(l2,winK)
            val = val + self.check(l3,winK)
            val = val + self.check(l4,winK)
            wk=wk+1
        return val
    
    def MinMax(self,state,maxturn,winK):
        result = self.utility(state,winK)
        if result is not None:
            return (result,[None,None,None])
        if maxturn:
            max_val=-10000
            px=None
            py=None
            board = state
            for action in self.actions(board,1):
                val,temp = self.MinMax(self.result(board,action),0,winK)
                if val > max_val:
                    max_val = val
                    px = action[1]
                    py = action[2]
            
            return (max_val,[1,px,py])
        else:
            min_val=10000
            px=None
            py=None
            board = state
            for action in self.actions(board,0):
                val,temp = self.MinMax(self.result(board,action),1,winK)
                if val < min_val:
                    min_val = val
                    px = action[1]
                    py = action[2]
            
            return (min_val,[0,px,py])
        
    def AlphaBetaPruning(self,state,maxturn,alpha,beta,winK):
        result = self.utility(state,winK)
        if result is not None:
            return (result,[None,None,None])
        if maxturn:
            max_val=-10000
            px=None
            py=None
            board = state
            for action in self.actions(board,1):
                val,temp = self.AlphaBetaPruning(self.result(board,action),0,alpha,beta,winK)
                if val > max_val:
                    max_val = val
                    px = action[1]
                    py = action[2]
                if max_val > alpha:
                    alpha = max_val
                if alpha >= beta:
                    return (max_val,[1,px,py])
                    
            return (max_val,[1,px,py])

        else:
            min_val=10000
            px=None
            py=None
            board = state
            for action in self.actions(board,0):
                val,temp = self.AlphaBetaPruning(self.result(board,action),1,alpha,beta,winK)
                if val < min_val:
                    min_val = val
                    px = action[1]
                    py = action[2]
                if min_val < beta :
                    beta = min_val
                if alpha >= beta:
                    return (min_val,[0,px,py])
            return (min_val,[0,px,py])
        
    def MinMax_depth(self,state,maxturn,depth,winK):
        result = self.utility(state,winK)
        if depth == 0 or result is not None:
            return (self.tictactoeHeuristic(state,winK),[None,None,None])
        if maxturn:
            max_val=-10000
            px=None
            py=None
            board = state
            for action in self.actions(board,1):
                val,temp = self.MinMax_depth(self.result(board,action),0,depth-1,winK)
                if val > max_val:
                    max_val = val
                    px = action[1]
                    py = action[2]
            
            return (max_val,[1,px,py])
        else:
            min_val=10000
            px=None
            py=None
            board = state
            for action in self.actions(board,0):
                val,temp = self.MinMax_depth(self.result(board,action),1,depth-1,winK)
                if val < min_val:
                    min_val = val
                    px = action[1]
                    py = action[2]
            
            return (min_val,[0,px,py])
    def MinMax_DepthplusAlphaBeta(self,state,maxturn,alpha,beta,depth,winK):
        result = self.utility(state,winK)
        if depth == 0 or result is not None:
            return (self.tictactoeHeuristic(state,winK),[None,None,None])
        if maxturn:
            max_val=-10000
            px=None
            py=None
            board = state
            for action in self.actions(board,1):
                val,temp = self.MinMax_DepthplusAlphaBeta(self.result(board,action),0,alpha,beta,depth-1,winK)
                if val > max_val:
                    max_val = val
                    px = action[1]
                    py = action[2]
                if max_val > alpha:
                    alpha = max_val
                if alpha >= beta:
                    return (max_val,[1,px,py])
            return (max_val,[1,px,py])
        else:
            min_val=10000
            px=None
            py=None
            board = state
            for action in self.actions(board,0):
                val,temp = self.MinMax_DepthplusAlphaBeta(self.result(board,action),1,alpha,beta,depth-1,winK)
                if val < min_val:
                    min_val = val
                    px = action[1]
                    py = action[2]
                if min_val < beta:
                    beta = min_val
                if alpha >= beta:
                    return (min_val,[0,px,py])
            
            return (min_val,[0,px,py])
    