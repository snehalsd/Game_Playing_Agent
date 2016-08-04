#!/usr/bin/python
import sys
import copy

maximum=float("-inf")
row=float("-inf")
col=float("-inf")
raid=False
my_opp=''
next_state_position=[-1,-1]

column_tag = ('A','B','C','D','E')
row_tag = ('1','2','3','4','5')

myfile=open(sys.argv[-1],'r')
out=myfile.readlines()
game_play= int(out[0])
if(game_play==4):
    my_player=out[1][0]
    player_one_algo=int(out[2])
    player_one_depth=int(out[3])
    my_opp=out[4][0]
    player_two_algo=int(out[5])
    player_two_depth=int(out[6])
    for p in range(7, 12):
        y=map(int ,out[p].split(' '))
        out[p]=y
    for z in range(12,17):
        temp=list(out[z])
        temp=temp[0:5]
        out[z]=temp
else:
    my_player=out[1][0]
    if(my_player == 'X'):
        my_opp='O'
    elif(my_player == 'O'):
        my_opp='X'
    cutoff_depth=int(out[2])
    for p in range(3, 8):
        y=map(int ,out[p].split(' '))
        out[p]=y
    for z in range(8,13):
        temp=list(out[z])
        temp=temp[0:5]
        out[z]=temp
    
def check_end_of_game(current_state):
    for i in range(0,5):
        for j in range(0,5):
            if(current_state[i][j]=='*'):
                return False
    return True

def calculate(current_state):
    sum_player=0
    sum_opp=0
    eval_val=0
    for a in range(0, 5):
        for b in range(0, 5):
            if(current_state[a][b] == my_player):
                if(game_play<>4):
                    sum_player+=out[a+3][b]
                else:
                    sum_player+=out[a+7][b]
            elif(current_state[a][b] == my_opp):
                if(game_play<>4):
                    sum_opp+=out[a+3][b]
                else:
                    sum_opp+=out[a+7][b]
    eval_val=sum_player - sum_opp 
    return eval_val

def write_output(current_output_file_handler,current_state):
    for a in range(0, 5):
        for b in range(0, 5):
            current_output_file_handler.write(current_state[a][b])
        current_output_file_handler.write("\n")
        
def write_in_log(record,algo):
    write_log.write(str(record[0])+","+str(record[1])+",")
    if(record[2] == float("inf")):
        write_log.write("Infinity")
    elif(record[2] == float("-inf")):
        write_log.write("-Infinity")
    else:
        write_log.write(str(record[2]))
    if(algo==3):
        write_log.write(",")
        if(record[3] == float("-inf")):
            write_log.write("-Infinity")
        elif(record[3] == float("inf")):
            write_log.write("Infinity")
        else:
            write_log.write(str(record[3]))
            
        write_log.write(",")
        if(record[4] == float("-inf")):
            write_log.write("-Infinity")
        elif(record[4] == float("inf")):
            write_log.write("Infinity")
        else:
            write_log.write(str(record[4]))    
    write_log.write("\n")

def get_raid_values(current_state,row,col,current_player,current_opp):
    if((row+1)<=4 and current_state[row+1][col]==current_opp):
            current_state[row+1][col]=current_player
    if((col+1)<=4 and current_state[row][col+1]==current_opp):
            current_state[row][col+1]=current_player
    if((col-1)>=0 and current_state[row][col-1]==current_opp):
            current_state[row][col-1]=current_player
    if((row-1)>=0 and current_state[row-1][col]==current_opp):
            current_state[row-1][col]=current_player
    
    return current_state
            
def player_check(current_state,row,col,current_player,current_opp):
    if((row-1 >= 0 and current_state[row-1][col] == current_player) or (col-1 >= 0 and current_state[row][col-1] == current_player) or (row+1 <= 4 and current_state[row+1][col] == current_player) or (col+1 <= 4 and current_state[row][col+1] == current_player)):
        current_state = get_raid_values(current_state,row,col, current_player, current_opp)
    return current_state
    
def greedy_bfs(current_state,current_player,current_opp):
    global maximum
    global row
    global col
    global raid
    row=-1
    col=-1
    if(game_play==4):
        position=7
    else:
        position=3
    
    for a in range(0, 5):
        for b in range(0, 5):
            value=0
            exp1=False
            exp2=False
            exp3=False
            exp4=False
            if(current_state[a][b]=='*'):
                if(a==0):
                    exp1=True
                    if(current_state[a+1][b]<>current_player):
                        exp2=True
                if(a==4):
                    exp2=True
                    if(current_state[a-1][b]<>current_player):
                        exp1=True   
                if(b==0):
                    exp3=True
                    if(current_state[a][b+1]<>current_player):
                        exp4=True
                if(b==4):
                    exp4=True
                    if(current_state[a][b-1]<>current_player):
                        exp3=True
                if(a>0 and a<4):
                    if(current_state[a-1][b]<>current_player):
                        exp1=True
                    if(current_state[a+1][b]<>current_player):
                        exp2=True
                if(b>0 and b<4):
                    if(current_state[a][b+1]<>current_player):
                        exp4=True
                    if(current_state[a][b-1]<>current_player):
                        exp3=True
                value=out[a+position][b]
                if(exp1 and exp2 and exp3 and exp4 and value>maximum):
                    maximum=value
                    raid=False
                    row=a
                    col=b
                else:
                    if(not(exp1)):
                        if((a+1)<=4 and current_state[a+1][b]==current_opp):
                            value+=out[a+position+1][b]
                        if((b+1)<=4 and current_state[a][b+1]==current_opp):
                            value+=out[a+position][b+1]
                        if((b-1)>=0 and current_state[a][b-1]==current_opp):
                            value+=out[a+position][b-1]        
                    if(not(exp2)):
                        if((a-1)>=0 and current_state[a-1][b]==current_opp):
                            value+=out[a+position-1][b]
                        if((b+1)<=4 and current_state[a][b+1]==current_opp):
                            value+=out[a+position][b+1]
                        if((b-1)>=0 and current_state[a][b-1]==current_opp):
                            value+=out[a+position][b-1]   
                    if(not(exp3)):
                        if((a+1)<=4 and current_state[a+1][b]==current_opp):
                            value+=out[a+position+1][b]
                        if((b+1)<=4 and current_state[a][b+1]==current_opp):
                            value+=out[a+position][b+1]
                        if((a-1)>=0 and current_state[a-1][b]==current_opp):
                            value+=out[a+position-1][b]          
                    if(not(exp4)):
                        if((a+1)<=4 and current_state[a+1][b]==current_opp):
                            value+=out[a+position+1][b]
                        if((a-1)>=0 and current_state[a-1][b]==current_opp):
                            value+=out[a+position-1][b]
                        if((b-1)>=0 and current_state[a][b-1]==current_opp):
                            value+=out[a+position][b-1] 
                    if(value>maximum):
                        maximum=value
                        raid=True
                        row=a
                        col=b
    
    if(row>=0 and col>=0):    
        current_state[row][col]=current_player
        if(raid):
            current_state=get_raid_values(current_state,row,col,current_player,current_opp)
             
def game_minimax(current_state,cutoff_depth,current_player,current_opp,record):
    depth_values=[]
    if(cutoff_depth==0 or check_end_of_game(current_state)):
        record[2]=calculate(current_state)
        if(game_play<>4):
            write_in_log(record,game_play)
        return record[2]     
    else:
        if(current_player==my_player):
            record[2]=float("-inf")
            depth_values.append(float("-inf"))
        else:
            record[2]=float("inf")
            depth_values.append(float("inf"))
        if(game_play<>4):
            write_in_log(record, game_play)
    for a in range(0,5):
        for b in range(0,5):
            if(current_state[a][b] == '*'):
                temp_node=record[0]
                temp_value=record[2]
                record[0]=column_tag[b]+row_tag[a]
                cutoff_depth -= 1
                new_state = copy.deepcopy(current_state)
                new_state[a][b] = current_player
                new_state = player_check(new_state, a, b, current_player,current_opp)
                record[1]+=1
                returned_value=game_minimax(new_state,cutoff_depth,current_opp, current_player, record)
                depth_values.append(returned_value)
                if(current_player==my_player):
                    if(record[2] > temp_value and record[1] == 1 ):
                        next_state_position[0] = a
                        next_state_position[1] = b
                    record[2]=max(record[2],temp_value)
                else:
                    record[2]=min(record[2],temp_value)
                record[1]-=1
                record[0]=temp_node
                if(game_play<>4):
                    write_in_log(record, game_play)
                cutoff_depth+=1
                
    if(current_player == my_opp):
        record[2]=min(depth_values)
        return record[2]
    else:
        record[2]=max(depth_values)
        return record[2]

def game_alphabeta(cutoff_depth, current_state, current_player, current_opponent, node, depth, value, alpha, beta):
    v = maxalphabeta(cutoff_depth, current_state, current_player, current_opponent, node, depth, value, alpha, beta)

def maxalphabeta(cutoff_depth, current_state, current_player, current_opp, node, depth, value, alpha, beta):
    if(cutoff_depth == 0 or check_end_of_game(current_state)):
        if(game_play<>4):
            write_in_log([node, depth, calculate(current_state), alpha, beta], game_play)
        return calculate(current_state)
    v = float("-inf")
    if(game_play<>4):
        write_in_log([node, depth, v, alpha, beta], game_play)
    for a in range(0,5):
        for b in range(0,5):
            if(current_state[a][b] == '*'):
                new_state = copy.deepcopy(current_state)
                new_state[a][b] = current_player
                new_state = player_check(new_state, a, b, current_player, current_opp)
                temp=minalphabeta(cutoff_depth - 1, new_state, current_opp, current_player, column_tag[b]+row_tag[a], depth + 1, v, alpha, beta)
                if(temp>v and depth == 0):
                    next_state_position[0] = a
                    next_state_position[1] = b
                v=max(v,temp)
                if(v >= beta):
                    if(game_play<>4):
                        write_in_log([node, depth, v, alpha, beta], game_play)
                    return v
                alpha = max(alpha, v)
                if(game_play<>4):
                    write_in_log([node, depth, v, alpha, beta], game_play)
    return v
    
def minalphabeta(cutoff_depth, current_state, current_player, current_opp, node, depth, value, alpha, beta):
    if(cutoff_depth == 0 or check_end_of_game(current_state)):
        if(game_play<>4):
            write_in_log([node, depth, calculate(current_state), alpha, beta], game_play)
        return calculate(current_state)
    v = float("inf")
    if(game_play<>4):
        write_in_log([node, depth, v, alpha, beta], game_play)
    for a in range(0,5):
        for b in range(0,5):
            if(current_state[a][b] == '*'):
                new_state = copy.deepcopy(current_state)
                new_state[a][b] = current_player
                new_state = player_check(new_state, a, b, current_player, current_opp)
                v = min(v, maxalphabeta(cutoff_depth - 1, new_state, current_opp, current_player, column_tag[b]+row_tag[a], depth + 1, v, alpha, beta))
                if(v <= alpha):
                    if(game_play<>4):
                        write_in_log([node, depth, v, alpha, beta], game_play)
                    return v
                beta = min(beta, v)
                if(game_play<>4):
                    write_in_log([node, depth, v, alpha, beta],game_play)
    return v    

def printing():
    next_state=open("next_state.txt","w+")
    write_output(next_state,out[8:13])
    next_state.close()

def game_simulation():
    while(not check_end_of_game(out[12:17])):
        
        if(player_one_algo==1):
            greedy_bfs(out[12:17],my_player,my_opp)
        elif(player_one_algo==2):
            node = "root"
            depth = 0
            value = float("-inf")
            record = [node,depth,value]
            game_minimax(out[12:17],player_one_depth,my_player,my_opp,record)
            out[next_state_position[0]+12][next_state_position[1]] = my_player
            out[12:17] = player_check(out[12:17], next_state_position[0], next_state_position[1], my_player, my_opp)
        else:
            game_alphabeta(player_one_depth, out[12:17], my_player, my_opp, "root", 0, float("-inf"), float("-inf"), float("inf"))
            out[next_state_position[0]+12][next_state_position[1]] = my_player
            out[12:17] = player_check(out[12:17], next_state_position[0], next_state_position[1], my_player, my_opp)
       
        write_output(trace_state,out[12:17])
        
        if(not check_end_of_game(out[12:17])):
          
            global my_player
            global my_opp
            my_player,my_opp=my_opp,my_player
         
            
            if(player_two_algo==1):
                greedy_bfs(out[12:17],my_player,my_opp)
            elif(player_two_algo==2):
                node = "root"
                depth = 0
                value = float("-inf")
                record = [node,depth,value]
                game_minimax(out[12:17],player_two_depth,my_player,my_opp,record)
                out[next_state_position[0]+12][next_state_position[1]] = my_player
                out[12:17] = player_check(out[12:17], next_state_position[0], next_state_position[1], my_player, my_opp)
            else:
                game_alphabeta(player_two_depth, out[12:17], my_player, my_opp, "root", 0, float("-inf"), float("-inf"), float("inf"))
                out[next_state_position[0]+12][next_state_position[1]] = my_player
                out[12:17] = player_check(out[12:17], next_state_position[0], next_state_position[1], my_player, my_opp)
                
                
                
            write_output(trace_state,out[12:17])
            my_player,my_opp=my_opp,my_player
           
        
if(game_play==1):
    greedy_bfs(out[8:13],my_player,my_opp)
    printing()
elif(game_play==2):
    write_log=open("traverse_log.txt","w+")
    write_log.write("Node,Depth,Value\n")
    begin_node="root"
    depth=0
    value=float("-inf")
    record=[begin_node,depth,value]
    game_minimax(out[8:13],cutoff_depth,my_player, my_opp,record)
    out[next_state_position[0]+8][next_state_position[1]] = my_player
    out[8:13] = player_check(out[8:13], next_state_position[0], next_state_position[1], my_player, my_opp)
    printing()

elif(game_play==3):
    write_log = open("traverse_log.txt","w+")
    write_log.write("Node,Depth,Value,Alpha,Beta\n")
    game_alphabeta(cutoff_depth, out[8:13], my_player, my_opp, "root", 0, float("-inf"), float("-inf"), float("inf"))
    print next_state_position[0],next_state_position[1]
    out[next_state_position[0]+8][next_state_position[1]] = my_player
    out[8:13] = player_check(out[8:13], next_state_position[0], next_state_position[1], my_player, my_opp)
    printing()

else:
    trace_state=open("trace_state","w+")
    game_simulation()
    trace_state.close()
        
            
