import numpy as np
import sys

'''
part 1 : board 
'''
black,white,empty,guard = "x","o",".","*"

## board
column_number = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26"]
row_number = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

## initial the board

def board_size():
    n_str = input("enter board size(5<=x<=26): ")
    return n_str

def is_size_valid(n_str):

    valid = True
    try :

        n = int(n_str)
        if n > 26 :
            return False
        if n < 5:
            return False
    except:
        return False
    return valid


def original_board(n):
    N = n+2
    B = [empty]*(n+2)*(n+2)
    for i in range((n+2)*(n+2)):
        if i <= n+2-1:
            B[i] = guard
        if i%N == 0:
            B[i] = guard
        if i%N == N-1 :
            B[i] = guard
        if i >= N*(N-1) :
            B[i] = guard
    return B

# print the board
def show_board(B,n,column_number,row_number):
    if n>10 :
        line_0 = ""
        line_1 = ""
        for i in range(n):
            if i < 10:
                line_0 += "  "
                line_1 += " " + column_number[ i ]
            if i >= 10:
                line_0 += " " + str(int((i-i%10)/10))
                line_1 += " " + column_number[ i ][ 1 ]
        print(" " + line_0)
        print(" " + line_1)
    else:
        line_0 = " "
        for i in range(n) :
            line_0 += " " + column_number[ i ]
        print(line_0)

    for i in range(n):
        line_i = ""
        for j in range(n):
            line_i += B[(i+1)*(n+2)+(j+1)] + " "
        print(row_number[i] + " " + line_i)

## get input position & is the position valid
def is_position_valid(row_number,n,legal_move):

    position = input("Enter the position you want to go: (e.g. a4) ")
    try:
        N = n+2
        if n<= 10:
            if len(position) != 2:
                return False
            if position[0] not in row_number[:n]:
                return False
            if int(position[1]) >= n:
                return False
        else:
            if len(position) > 3:
                return False
            if position[0] not in row_number[:n]:
                return False
            if len(position)==3 and int(position[1]) >= 3:
                return False
            if len(position)==3 and int(position[2]) >= n%10:
                return False

        if len(position) == 3 :
            pos = N * (row_number.index(position[ 0 ]) + 1) + int(position[ 1 ]) * 10 + int(position[ 2 ]) + 1
        else :
            pos = N * (row_number.index(position[ 0 ]) +1 ) + int(position[ 1 ]) + 1

        if pos not in legal_move:
            return False

        return pos

    except:
        return False




## updata the board
def updata_board(B,turn,pos):
    if turn%2 == 0 : ## black's turn turn: start from 0 and increase one/turn
        B[pos] = black
    else :
        B[pos] = white
    return B


'''
Part 2 : find the connections & legal move
'''
## all black/white's positions
def B_pos(B,N):
    Black = []
    for j in range(N*N):
      if B[j] == black :
        Black.append(j)
    return Black
def W_pos(B,N):
    White = []
    for j in range(N*N):
      if B[j] == white :
        White.append(j)
    return White

## legal move
def legal_moves(B,N):
    L = []
    for j in range(N*N):
      if B[j] == empty :
        L.append(j)
    return L

## connection: 4 directions(report) ; check the opposit first ; ignor the isolated points
## direction 1 --->
def connection_direction1(pos,position_list):
    connected_indices = [pos]
    count = 1
    if (pos - 1) not in position_list :
        i = 1
        while pos+i in position_list:
            count += 1
            connected_indices.append(pos + i)
            i += 1
        if i != 1:
            return [count,tuple(connected_indices)]

## direction 2 goning down
def connection_direction2(pos,position_list,N) :
    connected_indices = [pos]
    count = 1
    if (pos-N) not in position_list :
        i = 1
        while pos + i*N in position_list:
            count += 1
            connected_indices.append(pos + i*N )
            i += 1
        if i != 1 :
            return [ count,tuple(connected_indices)]
## direction3 left top to right bottom
def connection_direction3(pos,position_list,N) :
    connected_indices = [pos]
    count = 1
    if (pos-N-1) not in position_list :
        i = 1
        while pos + i*(N+1) in position_list:
            count += 1
            connected_indices.append(pos + i*(N + 1) )
            i += 1
        if i != 1 :
            return [ count, tuple(connected_indices)]
## direction 4 : right top to left bottom
def connection_direction4(pos,position_list,N) :
    connected_indices = [pos]
    count = 1
    if (pos-N+1) not in position_list :
        i = 1
        while pos + i*(N-1) in position_list:
            count += 1
            connected_indices.append(pos + i*(N-1) )
            i += 1
        if i != 1 :
            return [ count,tuple(connected_indices)]

## connection_dictionary
def conn_dic(position_list,N):
    connection_dictionarty = {}
    for pos in position_list:
        connection1 = connection_direction1(pos,position_list)
        connection2 = connection_direction2(pos,position_list,N)
        connection3 = connection_direction3(pos,position_list,N)
        connection4 = connection_direction4(pos,position_list,N)
        if connection1 != None:
            connection_dictionarty.update({connection1[1]:connection1[0]})
        if connection2 != None :
            connection_dictionarty.update({connection2[1]:connection2[0]})
        if connection3 != None:
            connection_dictionarty.update({connection3[1]:connection3[0]})
        if connection4 != None :
            connection_dictionarty.update({connection4[1] : connection4[ 0 ]})
        connection_dictionarty.update({pos:1})
    return connection_dictionarty

'''
Part 3 score
'''
## xxxx : 4000
## xxx : 3000
## oxxx : 2700
## xx : 2500
## oxx : 2000
## x : 600
## ox : 350

## score except x & ox
def score_dictionary():
    SD = {}
    SD.update({5:100000000000})
    SD.update({4.5:100000000000})
    SD.update({4:1000000})
    SD.update({3.5:6000})
    SD.update({3:6000})
    SD.update({2.5:2500})
    SD.update({2:2500})
    SD.update({1.5:500})
    SD.update({1:500})
    SD.update({0.5:250})
    return SD
def score_B(connection_dictionarty,N,legal_move):
    socre_board = [0] * (N*N)
    score_dic = score_dictionary()
    for x in list(connection_dictionarty.keys()):
        if connection_dictionarty.get(x) == 1:
            pos = x

            ## direction 1

            start_empty = pos - 1
            end_empty = pos + 1

            if start_empty in legal_move and end_empty in legal_move :
                socre_board[ start_empty ] += score_dic.get(1)
                socre_board[ end_empty ] += score_dic.get(1)
            elif start_empty in legal_move and end_empty not in legal_move :
                socre_board[ start_empty ] += score_dic.get(0.5)
            elif start_empty not in legal_move and end_empty in legal_move :
                socre_board[ end_empty ] += score_dic.get(0.5)

            ## direction 2
            start_empty = pos - N
            end_empty = pos + N
            if start_empty in legal_move and end_empty in legal_move :
                socre_board[ start_empty ] += score_dic.get(1)
                socre_board[ end_empty ] += score_dic.get(1)
            elif start_empty in legal_move and end_empty not in legal_move :
                socre_board[ start_empty ] += score_dic.get(0.5)
            elif start_empty not in legal_move and end_empty in legal_move :
                socre_board[ end_empty ] += score_dic.get(0.5)

            ## direction 3
            start_empty = pos - N -1
            end_empty = pos + N + 1

            if start_empty in legal_move and end_empty in legal_move :
                socre_board[ start_empty ] += score_dic.get(1)
                socre_board[ end_empty ] += score_dic.get(1)
            elif start_empty in legal_move and end_empty not in legal_move :
                socre_board[ start_empty ] += score_dic.get(0.5)
            elif start_empty not in legal_move and end_empty in legal_move :
                socre_board[ end_empty ] += score_dic.get(0.5)

            ## direction 4

            start_empty = pos - N + 1
            end_empty = pos + N - 1
            if start_empty in legal_move and end_empty in legal_move :
                socre_board[ start_empty ] += score_dic.get(1)
                socre_board[ end_empty ] += score_dic.get(1)
            elif start_empty in legal_move and end_empty not in legal_move :
                socre_board[ start_empty ] += score_dic.get(0.5)
            elif start_empty not in legal_move and end_empty in legal_move :
                socre_board[ end_empty ] += score_dic.get(0.5)

        else :    ## connection > 1
            connected_num = connection_dictionarty.get(x)
            connection_list = list(x)
            direction = connection_list[1] - connection_list[0]
            start_empty = connection_list[0] - direction
            end_empty = connection_list[-1] + direction

            if start_empty in legal_move and end_empty in legal_move:
                socre_board[start_empty] += score_dic.get(connected_num)
                socre_board[end_empty ] += score_dic.get(connected_num)
            elif start_empty in legal_move and end_empty not in legal_move:
                socre_board[start_empty] += score_dic.get(connected_num-0.5)
            elif start_empty not in legal_move and end_empty in legal_move:
                socre_board[end_empty] += score_dic.get(connected_num-0.5)
    return socre_board

## isolated pts
'''
part 4 : computer position
'''
def cmpt_move(connection_dictionarty_B,connection_dictionary_W,N,legal_move):
    score_board = [0] *N*N
    score_board_B = score_B(connection_dictionarty_B,N,legal_move)
    score_board_W = score_B(connection_dictionary_W,N,legal_move)
    for i in range (N*N):
            score_board[i] = score_board_W[i]*0.7 + score_board_B[i]
    max_score = max(score_board)
    max_pos = score_board.index(max_score)
    return [max_pos,max_score,score_board_B,score_board_W]

'''
part 5 by search
'''

def potenial_move(position_list,legal_move,N):
    potential_list = []
    c_1 = []
    direction = [1,N,N+1,N-1]
    for i in position_list:
        for j in direction:
            if i+j in legal_move and i+j not in potential_list:
                potential_list.append(i+j)
                c_1.append(i+j)
            if i-j in legal_move and i-j not in potential_list:
                potential_list.append(i-j)
                c_1.append(i-j)
    for k in c_1:
        for a in direction:
            if k+a in legal_move and k+a not in potential_list:
                potential_list.append(k+a)
            if k-a in legal_move and k-a not in potential_list:
                potential_list.append(k-a)
                c_1.append(k-a)

    return potential_list

def search(B,position_list_b,position_list_w,legal_move,N):
    search_list_b = potenial_move(position_list_b,legal_move,N)
    search_list_w = potenial_move(position_list_w, legal_move, N)
    max_score = 0
    pos = -1
    for k in range(len(search_list_b)):
        board = [empty] *N*N
        for i in range(N*N):
            board[i] = B[i]
        x = search_list_b[k]
        updata_board(board,0,x)
        position_list = B_pos(board, N)
        connection_dictionary = conn_dic(position_list, N)
        connection_list = list(connection_dictionary.keys())
        if 5 in connection_dictionary.values() :
            return x

        position_list_w = W_pos(board, N)
        connection_dictionary_w = conn_dic(position_list_w, N)
        list_ = cmpt_move(connection_dictionary,connection_dictionary_w,N,legal_move)
        score = list_[1]
        if score > max_score :
            max_score = score
            pos = x
        if max_score <= 10000 :
            for conn_1 in connection_list :
                lis_1 = [ ]
                if connection_dictionary[ conn_1 ] >= 3.5 :
                    for i in range(len(conn_1)) :
                        lis_1.append(conn_1[ i ])
                    if x in lis_1 :
                        for conn_2 in connection_list :
                            lis_2 = []
                            if connection_dictionary[ conn_2 ] >= 3 :
                                for j in range(len(conn_2)) :
                                    lis_2.append(conn_2[j])
                                if lis_1 != lis_2:
                                    if x in lis_2:
                                        pos = x
    for a in range(len(search_list_w)):
        board = [empty] *N*N
        for i in range(N*N):
            board[i] = B[i]
        y = search_list_w[a]
        updata_board(board,1,y)
        position_list = B_pos(board, N)
        connection_dictionary = conn_dic(position_list, N)
        position_list_w = W_pos(board, N)
        connection_dictionary_w = conn_dic(position_list_w, N)
        connection_list = list(connection_dictionary_w.keys())
        if 5 in connection_dictionary_w.values():
            return y
        if 4 in connection_dictionary_w.values() and max_score <= 10000:
            return y
        if 4.5 in connection_dictionary_w.values() and max_score <= 10000:
            return y

        for conn_1 in connection_list :
            lis_1 = [ ]
            if connection_dictionary_w[ conn_1 ] >= 3 :
                for i in range(len(conn_1)) :
                    lis_1.append(conn_1[ i ])
                if y in lis_1 :
                    for conn_2 in connection_list:
                        lis_2 = [ ]
                        if connection_dictionary_w[ conn_2 ] >= 3 :
                            for j in range(len(conn_2)) :
                                lis_2.append(conn_2[j])
                            if conn_2 != conn_1 and y in lis_2 :
                                if max_score <= 15000:
                                    return y
    list_ = cmpt_move(connection_dictionary,connection_dictionary_w,N,legal_move)[3]
    max_s = max(list_)
    if max_s > max_score :
        return y

    return pos


'''
part 8 TODO : 
       ABminmax (not works yet)
'''
def get_value(B,N):
    score = [0] *N*N
    legal_move = legal_moves(B, N)

    position_list_b = B_pos(B, N)
    connection_dictionary_b = conn_dic(position_list_b, N)
    score_board_b = score_B(connection_dictionary_b, N, legal_move)

    position_list_w = W_pos(B, N)
    connection_dictionary_w = conn_dic(position_list_w, N)
    score_board_w = score_B(connection_dictionary_w,N,legal_move)

    for i in range(N*N) :
        score[i] = score_board_b[ i ] - score_board_w[i] * 0.7
    return score

def minmax(B,N,depth,turn):

    legal_move = legal_moves(B, N)

    position_list_b = B_pos(B, N)
    connection_dictionary_b = conn_dic(position_list_b, N)

    position_list_w = W_pos(B, N)
    connection_dictionary_w = conn_dic(position_list_b, N)

    position_list = position_list_b + position_list_w
    finish_ = check_win(connection_dictionary_b, connection_dictionary_w)
    potential_list = potenial_move(position_list, legal_move, N)

    if finish_ or depth==0: ## leaf nodes
        if turn%2 == 0:
            return min(get_value(B,N)),B
        else:
            return max(get_value(B,N)),B

    if turn % 2 != 0 :## max the value of its children
        value_list = []
        board_list = []
        for move in potential_list:
            board = [ empty ] * N * N
            for i in range(N * N) :
                board[ i ] = B[ i ]
            updata_board(board, turn, move)
            board_list.append(board)
            value,_ = minmax(board,N,depth-1,turn+1)
            value_list.append(value)
        index = value_list.index(min(value_list))
        min_board = board_list[index]
        return min(value_list),min_board

    else:
        value_list = [ ]
        board_list = [ ]
        for move in potential_list :
            board = [ empty ] * N * N
            for i in range(N * N) :
                board[ i ] = B[ i ]
            updata_board(board, turn, move)
            board_list.append(board)
            value,_ = minmax(board, N, depth - 1, turn + 1)
            value_list.append(value)
        index = value_list.index(max(value_list))
        max_board = board_list[ index ]
        return max(value_list),max_board
'''
def ABminmax(B,N,depth,alpha,beta,turn,dic={}):

    legal_move = legal_moves(B, N)

    position_list_b = B_pos(B,N)
    connection_dictionary_b = conn_dic(position_list_b, N)

    position_list_w = W_pos(B, N)
    connection_dictionary_w = conn_dic(position_list_b, N)

    position_list = position_list_b + position_list_w
    finish = check_win(connection_dictionary_b, connection_dictionary_w)
    potential_list = potenial_move(position_list,legal_move,N)

    if finish or depth==0: ## leaf nodes
        return get_value(B,N,turn)

    for move in potential_list:

        board = [ empty ] * N * N
        for i in range(N * N) :
            board[ i ] = B[ i ]
        updata_board(board,turn,move)

        value = ABminmax(board,depth-1,alpha,beta,turn+1,dic)

        if turn%2 == 0:
            if value > alpha:
                alpha = value
            return alpha
        else:
            if value < beta :
                beta = value
            return beta
        dic.updata({alpha:move})
    return dic[alpha]
'''



'''
part 6 check winner & play again
'''
def check_win(connection_dictionary_b,connection_dictionary_w):

    if 5 in connection_dictionary_b.values():
        return True
    if 5 in connection_dictionary_w.values():
        return True


def play_again():
    play_again_str = 'xxxxxxx'

    while play_again_str != 'y' and play_again_str != 'n' :
        play_again_str = input("play again? [y/n]: ")
    if play_again_str == 'y' :
        return True
    else :
        return False






'''
Part 7: the game
'''

play = True


while play:

    method_1 = False
    method_2 = False
    method_3 = False

    ## level
    x = "cdscas"
    while x != "1" and x != "2" and x != "3" :
        x = input("choose the level of the computer( 1(very easy) /2(recommed)/ 3(may take forever)): ")
        if x == "1" :
            method_1 = True
        if x == "2" :
            method_2 = True
        if x == "3" :
            method_3 = True

    print()
    n_str = board_size()
    valid = is_size_valid(n_str)
    while not valid:
        n_str = board_size()
        valid = is_size_valid(n_str)
    n = int(n_str)
    N = n+2
    finish = False
    B = original_board(n)

    print()
    show_board(B,n,column_number,row_number)

    ## who go first
    print()
    turn_str = 0
    while turn_str != "0" and turn_str != "1":
        turn_str = input("if you want to go first enter 0, otherwise enter 1:  ")
    turn  = int(turn_str)
    print()

    while finish != True:

        Legal_move = legal_moves(B,N)

        Position_list = B_pos(B,N)
        Connection_dictionary = conn_dic(Position_list,N)
        Position_list_w = W_pos(B, N)
        Connection_dictionary_w = conn_dic(Position_list_w,N)

        finish = check_win(Connection_dictionary, Connection_dictionary_w)

        if Legal_move == []:
            print()
            print("tie!")
            finish = True

        if finish == True :
            if 5 in Connection_dictionary.values():
                print("You win!")
            if 5 in Connection_dictionary_w.values():
                print("Computer win!")
            print()
            show_board(B, n, column_number, row_number)
            print()
            play = play_again()

        else :

            if turn % 2 == 0:
                pos = False
                while pos == False:
                    pos = is_position_valid(row_number,n,Legal_move)
                print()
                updata_board(B, turn, pos)

            else:
                if len(Legal_move) == n*n:
                    pos = (N//2) *N + N//2
                else:
                    if method_1:
                        pos = cmpt_move(Connection_dictionary,Connection_dictionary_w,N,Legal_move)[0]
                    if method_2:
                        pos =search(B,Position_list,Position_list_w,Legal_move,N)
                    if method_3:
                        depth = 3
                        _,board = minmax(B,N,depth,turn)
                        for i in range(N*N):
                            if B[i] != board[i]:
                                pos = i

                C = column_number[pos%N - 1]
                R = row_number[int((pos-pos%N)/N -1)]
                updata_board(B,turn,pos)
                show_board(B, n, column_number, row_number)
                print()
                print("computer's move", R + C)

            turn += 1

