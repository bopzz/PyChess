from tkinter import *


root = Tk()
root.title("Chess")
root.geometry("900x600")

game_Board = Canvas(root, width=600, height=600, bg="#EBE8BE")
game_Board.grid(row=0, column=0, rowspan=60)

width_symbol = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
height_symbol = ['8', '7', '6', '5', '4', '3', '2', '1']
board_Color = ["#B5E1B2", "#84B661"]

def board_Display():

    for i in range(8):
        game_Board.create_text(10, 55+i*70, text=height_symbol[i])
        game_Board.create_text(55+i*70, 590, text=width_symbol[i])
        for j in range(8):
            game_Board.create_rectangle(20+i*70, 20+j*70, 20+(i+1)*70, 20+(j+1)*70, fill=((i*8+j-i)%2==0) and board_Color[0] or board_Color[1], outline="")

board_Display()


highlight_Color = ["#F5E1B2", "#F4B661"]
box_Highlight = []


blank = {"chess_piece": "", "color": "", "image": ""}
pieces_Pos = {
    "white": {
        "pawn": [],
        "rook": [],
        "knight": [],
        "bishop": [],
        "queen": [],
        "king": []
    },
    "black": {
        "pawn": [],
        "rook": [],
        "knight": [],
        "bishop": [],
        "queen": [],
        "king": []
    }
}
pieces_Img = {
    "white": {
        "pawn": 0,
        "rook": 0,
        "knight": 0,
        "bishop": 0,
        "queen": 0,
        "king": 0
    },
    "black": {
        "pawn": 0,
        "rook": 0,
        "knight": 0,
        "bishop": 0,
        "queen": 0,
        "king": 0
    }
}
WHITE = "white"
BLACK = "black"
board_State = []
board_All_state = []
player_Side = WHITE

def setup_chess_Pieces():

    global board_State, pieces_Pos, pieces_Img, player_Side, blank


    for i in range(8):
        temp = [];
        for j in range(8):
            temp.append(blank.copy());
        board_State.append(temp)

    for i in range(8):
        board_State[(player_Side==WHITE and 1 or 6)][i]["chess_piece"], board_State[(player_Side==WHITE and 1 or 6)][i]["color"] = ("pawn", BLACK)
        board_State[(player_Side==BLACK and 1 or 6)][i]["chess_piece"], board_State[(player_Side==BLACK and 1 or 6)][i]["color"] = ("pawn", WHITE)
        pieces_Pos[BLACK]["pawn"].append(((player_Side==WHITE and 1 or 6), i))
        pieces_Pos[WHITE]["pawn"].append(((player_Side==BLACK and 1 or 6), i))

    order = ["rook", "knight", "bishop", (player_Side==WHITE and "queen" or "king"), (player_Side==BLACK and "queen" or "king"), "bishop", "knight", "rook"]
    for i in range(8):
        board_State[(0 if player_Side==WHITE else 7)][i]["chess_piece"], board_State[(0 if player_Side==WHITE else 7)][i]["color"] = (order[i], BLACK)
        board_State[(0 if player_Side==BLACK else 7)][i]["chess_piece"], board_State[(0 if player_Side==BLACK else 7)][i]["color"] = (order[i], WHITE)
        pieces_Pos[BLACK][order[i]].append(((0 if player_Side==WHITE else 7), i))
        pieces_Pos[WHITE][order[i]].append(((0 if player_Side==BLACK else 7), i))

    ascending = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    color = [BLACK, WHITE]
    for i in range(2):
        for j in range(6):
            pieces_Img[color[i]][ascending[j]] = PhotoImage(file="./chess_pic/"+color[i]+"_"+ascending[j]+".png")

    for i in range(8):
        for j in range(8):
            if not board_State[i][j]["chess_piece"]=="":
                img = pieces_Img[board_State[i][j]["color"]][board_State[i][j]["chess_piece"]]
                board_State[i][j]["image"] = game_Board.create_image(30+j*70, 30+i*70, anchor=NW, image=img)

setup_chess_Pieces()


move_List = []

def list_Create():

    global move_List

    for i in range(1, 7):
        move_List.append([])

    for i in range(1, 7, 3):
        for j in range(27):
            if j==0:
                move_List[i-1].append(Label(root, text="", width=2, relief=SUNKEN))
            else:
                move_List[i-1].append(Label(root, text=(i==4 and 26 or 0)+j, width=2, relief=SUNKEN))
            move_List[i-1][j].grid(row=j, column=i)

    for i in range(2, 4):
        for j in range(27):
            if j==0:
                move_List[i-1].append(Label(root, text=(i==2 and WHITE or BLACK).capitalize(), width=8, relief=SUNKEN))
            else:
                move_List[i-1].append(Label(root, text="", width=8, relief=SUNKEN))
            move_List[i-1][j].grid(row=j, column=i)

    for i in range(5, 7):
        for j in range(27):
            if j==0:
                move_List[i-1].append(Label(root, text=(i==5 and WHITE or BLACK).capitalize(), width=8, relief=SUNKEN))
            else:
                move_List[i-1].append(Label(root, text="", width=8, relief=SUNKEN))
            move_List[i-1][j].grid(row=j, column=i)

list_Create()


def alert(winner):

    window = Toplevel()
    window.title("GAME ENDS")
    window.attributes("-toolwindow", 1)
    window.focus_set()
    window.grab_set()

    sentence = Label(window)
    btn = Button(window, text="  OK!  ", command=lambda: window.destroy())
    if winner!="draw":
        sentence["text"] = "     " + winner.capitalize() + " wins!     "
    else:
        sentence["text"] = "     Stalemate!     "

    sentence.pack(side=TOP)
    btn.pack(side=BOTTOM)
    root.wait_window(window)




player_Turn = WHITE
Draw = False
turn_Num = 1

def next_Move():

    global player_Turn, turn_Num, Draw

    if player_Turn == WHITE:
        player_Turn = BLACK
    else:
        player_Turn = WHITE
        turn_Num+=1
        if turn_Num == 53:
            Draw = True
            alert("draw")




available_Move = []
available_Show = []

def find_Check():

    global available_Move, board_State, player_Turn, pieces_Pos, player_Side

    y = pieces_Pos[player_Turn]["king"][0][0]
    x = pieces_Pos[player_Turn]["king"][0][1]
    all_check = []

    for i in range(y+1, 8):
        if board_State[i][x]["chess_piece"] != "":
            if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                all_check.append((i-y, 0))
            break

    for i in range(y-1, -1, -1):
        if board_State[i][x]["chess_piece"] != "":
            if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                all_check.append((i-y, 0))
            break

    for i in range(x+1, 8):
        if board_State[y][i]["chess_piece"] != "":
            if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                all_check.append((0, i-x))
            break
    
    for i in range(x-1, -1, -1):
        if board_State[y][i]["chess_piece"] != "":
            if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                all_check.append((0, i-x))
            break

    for i in range(1, min(8-x, y+1)):
        if board_State[y-i][x+i]["chess_piece"] != "":
            if board_State[y-i][x+i]["color"] != player_Turn:
                if board_State[y-i][x+i]["chess_piece"] == "queen" or board_State[y-i][x+i]["chess_piece"] == "bishop" or (i==1 and board_State[y-i][x+i]["chess_piece"] == "pawn" and player_Turn==player_Side):
                    all_check.append((-i, i))
            break

    for i in range(1, min(x+1, 8-y)):
        if board_State[y+i][x-i]["chess_piece"] != "":
            if board_State[y+i][x-i]["color"] != player_Turn:
                if board_State[y+i][x-i]["chess_piece"] == "queen" or board_State[y+i][x-i]["chess_piece"] == "bishop" or (i==1 and board_State[y+i][x-i]["chess_piece"] == "pawn" and player_Turn!=player_Side):
                    all_check.append((i, -i))
            break

    for i in range(1, min(x+1, y+1)):
        if board_State[y-i][x-i]["chess_piece"] != "":
            if board_State[y-i][x-i]["color"] != player_Turn:
                if board_State[y-i][x-i]["chess_piece"] == "queen" or board_State[y-i][x-i]["chess_piece"] == "bishop" or (i==1 and board_State[y-i][x-i]["chess_piece"] == "pawn" and player_Turn==player_Side):
                    all_check.append((-i, -i))
            break

    for i in range(1, min(8-x, 8-y)):
        if board_State[y+i][x+i]["chess_piece"] != "":
            if board_State[y+i][x+i]["color"] != player_Turn:
                if board_State[y+i][x+i]["chess_piece"] == "queen" or board_State[y+i][x+i]["chess_piece"] == "bishop" or (i==1 and board_State[y+i][x+i]["chess_piece"] == "pawn" and player_Turn!=player_Side):
                    all_check.append((i, i))
            break

    for i in range(8):
        coordY = ((int(i/4)) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
        coordX = ((not int(i/4)) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
        if y+coordY>-1 and y+coordY<8 and x+coordX>-1 and x+coordX<8:
            if board_State[y+coordY][x+coordX]["chess_piece"] == "knight" and board_State[y+coordY][x+coordX]["color"]!=board_State[y][x]["color"]:
                all_check.append((coordY, coordX))

    if len(all_check)==0:
        return -1
    else:
        return all_check




check_Dist = -1
moved_State = {
    "white": {
        "0-0": True,
        "0-0-0": True
    },
    "black": {
        "0-0": True,
        "0-0-0": True
    }
}

def move_Set(y, x):

    global available_Move, board_State, player_Turn, pieces_Pos, player_Side

    chess_Cardinals = [(1, 0),(0, 1),(-1, 0),(0, -1)]
    chess_Diagonals = [(1, 1),(-1, 1),(1, -1),(-1, -1)]

    if board_State[y][x]["chess_piece"] == "pawn":

        if board_State[y][x]["color"] != player_Side:
            if board_State[y+1][x]["chess_piece"] == "":
                available_Move.append((y+1, x))
                if y == 1 and board_State[y+2][x]["chess_piece"] == "":
                    available_Move.append((y+2, x))
            if x<7 and board_State[y+1][x+1]["chess_piece"]!="" and board_State[y+1][x+1]["color"] == player_Side:
                available_Move.append((y+1, x+1))
            if x>0 and board_State[y+1][x-1]["chess_piece"]!="" and board_State[y+1][x-1]["color"] == player_Side: 
                available_Move.append((y+1, x-1))

        else:                                        # board_State[y][x]["color"] == player_Side
            if board_State[y-1][x]["chess_piece"] == "":
                available_Move.append((y-1, x))
                if y == 6 and board_State[y-2][x]["chess_piece"] == "":
                    available_Move.append((y-2, x))
            if x<7 and board_State[y-1][x+1]["chess_piece"] != "" and board_State[y-1][x+1]["color"] != player_Side:
                available_Move.append((y-1, x+1))
            if x>0 and board_State[y-1][x-1]["chess_piece"] != "" and board_State[y-1][x-1]["color"] != player_Side: 
                available_Move.append((y-1, x-1))

    elif board_State[y][x]["chess_piece"] == "rook":

        for i in range(4):
            moveY, moveX = chess_Cardinals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))

    elif board_State[y][x]["chess_piece"] == "knight":
        
        for i in range(8):
            moveY = ((int(i/4)) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
            moveX = ((not int(i/4)) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
            if y+moveY>-1 and y+moveY<8 and x+moveX>-1 and x+moveX<8:
                if board_State[y+moveY][x+moveX]["color"]!=board_State[y][x]["color"]:
                    available_Move.append((y+moveY, x+moveX))

    elif board_State[y][x]["chess_piece"] == "bishop":

        for i in range(4):
            moveY, moveX = chess_Diagonals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))

    elif board_State[y][x]["chess_piece"] == "queen":

        for i in range(4):
            moveY, moveX = chess_Cardinals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))

        for i in range(4):
            moveY, moveX = chess_Diagonals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))

    elif board_State[y][x]["chess_piece"] == "king":

        for i in range(4):
            moveY, moveX = chess_Cardinals[i]
            if x+moveX>-1 and x+moveX<8 and y+moveY>-1 and y+moveY<8 and board_State[y+moveY][x+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((y+moveY, x+moveX))

        for i in range(4):
            moveY, moveX = chess_Diagonals[i]
            if x+moveX>-1 and x+moveX<8 and y+moveY>-1 and y+moveY<8 and board_State[y+moveY][x+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((y+moveY, x+moveX))

        if find_Check() == -1:
            if moved_State[player_Turn][("0-0" if player_Side==WHITE else "0-0-0")]:
                blocked = False
                for i in range((5 if player_Side==WHITE else 4), 7):
                    if board_State[y][i]["chess_piece"] != "":
                        blocked = True
                        break
                if not blocked:
                    available_Move.append((y, x+2))

            if moved_State[player_Turn][("0-0-0" if player_Side==WHITE else "0-0")]:
                blocked = False
                for i in range(1, (4 if player_Side==WHITE else 3)):
                    if board_State[y][i]["chess_piece"] != "":
                        blocked = True
                        break
                if not blocked:
                    available_Move.append((y, x-2))

def anti_Check(y, x):

    global board_State, available_Move, player_Turn, pieces_Pos, check_Dist

    pos = pieces_Pos[player_Turn]["king"][0]

    if check_Dist != -1:

        if board_State[y][x]["chess_piece"] == "king":
            return

        elif len(check_Dist)>1:
            available_Move = []
            return
        
        temp = check_Dist.copy()
        check_Dist = check_Dist[0]

        if check_Dist[0] == 0:
            if check_Dist[1] < 0:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][0] != pos[0] or available_Move[i][1]-pos[1] < check_Dist[1] or available_Move[i][1] > pos[1]:
                        available_Move.pop(i)

            else:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][0] != pos[0] or available_Move[i][1]-pos[1] > check_Dist[1] or available_Move[i][1] < pos[1]:
                        available_Move.pop(i)

        elif check_Dist[1] == 0:
            if check_Dist[0] < 0:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][1] != pos[1] or available_Move[i][0]-pos[0] < check_Dist[0] or available_Move[i][0] > pos[0]:
                        available_Move.pop(i)

            else:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][1] != pos[1] or available_Move[i][0]-pos[0] > check_Dist[0] or available_Move[i][0] < pos[0]:
                        available_Move.pop(i)

        elif abs(check_Dist[0]) == abs(check_Dist[1]):
            if check_Dist[0]*check_Dist[1] < 0:
                if check_Dist[0] < 0:
                    for i in range(len(available_Move)-1, -1, -1):
                        if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) >= 0 or available_Move[i][0]-pos[0] < check_Dist[0] or available_Move[i][0] > pos[0]:
                            available_Move.pop(i)

                else:                       # check_Dist[0] > 0
                    for i in range(len(available_Move)-1, -1, -1):
                        if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) >= 0 or available_Move[i][0]-pos[0] > check_Dist[0] or available_Move[i][0] < pos[0]:
                            available_Move.pop(i)

            else:                           # check_Dist[0]*check_Dist[1] > 0
                if check_Dist[0] < 0:
                    for i in range(len(available_Move)-1, -1, -1):
                        if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) <= 0 or available_Move[i][0]-pos[0] < check_Dist[0] or available_Move[i][0] > pos[0]:
                            available_Move.pop(i)

                else:
                    for i in range(len(available_Move)-1, -1, -1):
                        if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) <= 0 or available_Move[i][0]-pos[0] > check_Dist[0] or available_Move[i][0] < pos[0]:
                            available_Move.pop(i)

        else:
            for i in range(len(available_Move)-1, -1, -1):
                if available_Move[i][0] != pos[0]+check_Dist[0] or available_Move[i][1] != pos[1]+check_Dist[1]:
                    available_Move.pop(i)
        
        check_Dist = temp.copy()

def commit_Suicide(y, x):

    global pieces_Img, available_Move, player_Turn, pieces_Pos, blank

    blocking = False
    diffY = y - pieces_Pos[player_Turn]["king"][0][0]
    diffX = x - pieces_Pos[player_Turn]["king"][0][1]

    if diffY == 0 and diffX == 0:
        
        for i in range(len(available_Move)-1, -1, -1):
            
            move = available_Move[i]
            temp = blank.copy()
            pos = pieces_Pos[player_Turn]["king"][0]

            if abs(move[1]-x)==2:

                board_State[move[0]][move[1]-int((move[1]-x)/2)] = board_State[pos[0]][pos[1]].copy()
                board_State[pos[0]][pos[1]] = blank.copy()

                pieces_Pos[player_Turn]["king"][0] = (move[0], move[1]-int((move[1]-x)/2))

                coord_Check = find_Check()

                if coord_Check == -1:

                    board_State[move[0]][move[1]] = board_State[move[0]][move[1]-int((move[1]-x)/2)].copy()
                    board_State[move[0]][move[1]-int((move[1]-x)/2)] = blank.copy()

                    pieces_Pos[player_Turn]["king"][0] = move

                    coord_Check = find_Check()

                    pieces_Pos[player_Turn]["king"][0] = pos

                    board_State[pos[0]][pos[1]] = board_State[move[0]][move[1]].copy()
                    board_State[move[0]][move[1]] = blank.copy()

                else:

                    pieces_Pos[player_Turn]["king"][0] = pos

                    board_State[pos[0]][pos[1]] = board_State[move[0]][move[1]-int((move[1]-x)/2)].copy()
                    board_State[move[0]][move[1]-int((move[1]-x)/2)] = blank.copy()

            else:

                if board_State[move[0]][move[1]]["chess_piece"] != "":
                    game_Board.coords(board_State[move[0]][move[1]]["image"], -70, -70)
                    temp = board_State[move[0]][move[1]].copy()

                board_State[move[0]][move[1]] = board_State[pos[0]][pos[1]].copy()
                board_State[pos[0]][pos[1]] = blank.copy()

                pieces_Pos[player_Turn]["king"][0] = move

                coord_Check = find_Check()

                pieces_Pos[player_Turn]["king"][0] = pos

                board_State[pos[0]][pos[1]] = board_State[move[0]][move[1]].copy()
                board_State[move[0]][move[1]] = temp.copy()

                if board_State[move[0]][move[1]]["chess_piece"] != "":
                    game_Board.coords(board_State[move[0]][move[1]]["image"], move[1]*70+30, move[0]*70+30)
                
            if coord_Check != -1:
                available_Move.pop(i)

    elif diffY == 0:

        if diffX < 0:
            for i in range(x+1, pieces_Pos[player_Turn]["king"][0][1]):
                if board_State[y][i]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(x-1,-1,-1):
                    if board_State[y][i]["chess_piece"] != "":
                        if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][0] != y:
                                    available_Move.pop(move)
                        break

        elif diffX > 0:
            for i in range(x-1, pieces_Pos[player_Turn]["king"][0][1], -1):
                if board_State[y][i]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(x+1,8):
                    if board_State[y][i]["chess_piece"] != "":
                        if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][0] != y:
                                    available_Move.pop(move)
                        break

    elif diffX == 0:

        if diffY < 0:
            for i in range(y+1, pieces_Pos[player_Turn]["king"][0][0]):
                if board_State[i][x]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(y-1,-1,-1):
                    if board_State[i][x]["chess_piece"] != "":
                        if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][1] != x:
                                    available_Move.pop(move)
                        break

        elif diffY > 0:
            for i in range(y-1, pieces_Pos[player_Turn]["king"][0][0], -1):
                if board_State[i][x]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(y+1,8):
                    if board_State[i][x]["chess_piece"] != "":
                        if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][1] != x:
                                    available_Move.pop(move)
                        break

    elif abs(diffY) == abs(diffX):

        if diffX*diffY < 0:

            if diffY < 0:
                for i in range(1, diffX):
                    if board_State[y+i][x-i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(8-x, y+1)):
                        if board_State[y-i][x+i]["chess_piece"] != "":
                            if board_State[y-i][x+i]["color"] != player_Turn and (board_State[y-i][x+i]["chess_piece"] == "queen" or board_State[y-i][x+i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) >= 0:
                                        available_Move.pop(move)
                            break

            else:
                for i in range(1, -diffX):
                    if board_State[y-i][x+i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(x+1, 8-y)):
                        if board_State[y+i][x-i]["chess_piece"] != "":
                            if board_State[y+i][x-i]["color"] != player_Turn and (board_State[y+i][x-i]["chess_piece"] == "queen" or board_State[y+i][x-i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) >= 0:
                                        available_Move.pop(move)
                            break

        elif diffX*diffY > 0:

            if diffY < 0:
                for i in range(1, -diffX):
                    if board_State[y+i][x+i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(x+1, y+1)):
                        if board_State[y-i][x-i]["chess_piece"] != "":
                            if board_State[y-i][x-i]["color"] != player_Turn and (board_State[y-i][x-i]["chess_piece"] == "queen" or board_State[y-i][x-i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) <= 0:
                                        available_Move.pop(move)
                            break

            else:
                for i in range(1, diffX):
                    if board_State[y-i][x-i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(8-x, 8-y)):
                        if board_State[y+i][x+i]["chess_piece"] != "":
                            if board_State[y+i][x+i]["color"] != player_Turn and (board_State[y+i][x+i]["chess_piece"] == "queen" or board_State[y+i][x+i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) <= 0:
                                        available_Move.pop(move)
                            break

def find_Moves(y, x):

    move_Set(y, x)
    anti_Check(y, x)
    commit_Suicide(y, x)






def check_Or_checkmate():

    global available_Move, pieces_Pos, player_Turn, check_Dist

    ascending = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    moves = []

    for i in range(6):
        coord_arr = pieces_Pos[player_Turn][ascending[i]]
        for j in range(len(coord_arr)):
            find_Moves(coord_arr[j][0], coord_arr[j][1])
            moves.append(available_Move)
            del_Move()

    for move in moves:
        if len(move) > 0:
            return False

    return True

def disable(y, x):
    
    global board_State, player_Turn, moved_State, player_Side

    BoW = 0 if player_Turn==player_Side else 7
    if moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0"]:
        if y==BoW and x==7:
            moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0"] = False

    if moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0-0"]:
        if y==BoW and x==0:
            moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0-0"] = False




def print_Moves(eaten, chess_piece, coord_from, coord_to, special):

    global player_Turn, turn_Num

    called = {
        "pawn": "",
        "knight": "N",
        "rook": "R",
        "bishop": "B",
        "queen": "Q",
        "king": "K"
    }

    row = turn_Num if turn_Num<=26 else turn_Num-26
    column = (1 if player_Turn==WHITE else 2) + (0 if turn_Num<=26 else 3)
    if special=="0-0" or special=="0-0-0":
        move_List[column][row]["text"] = special
    elif eaten:
        full = ""
        if called[chess_piece]=="":
            full += coord_from[0]
        else:
            full += called[chess_piece]
        full += "x" + coord_to + special
        move_List[column][row]["text"] = full
    else:
        move_List[column][row]["text"] = called[chess_piece] + coord_to + special
    return (row, column)




def display_Move():

    global available_Move, available_Show

    for i in range(len(available_Move)):
        avail_X = available_Move[i][1]
        avail_Y = available_Move[i][0]
        available_Show.append(game_Board.create_oval(45+avail_X*70, 45+avail_Y*70, 65+avail_X*70, 65+avail_Y*70, fill="#A9A9A9", outline=""))

def del_Move():

    global available_Move, available_Show

    for i in range(len(available_Show)-1, -1, -1):
        game_Board.delete(available_Show[i])
    available_Move = []
    available_Show = []




checkMate = False
pickup = False
col, row = (0, 0)

def coord_pickup(e):

    global pieces_Img, player_Turn, board_State, pickup, col, row, checkMate, Draw

    row, col = (int((e.y-20)/70), int((e.x-20)/70))
    if (not checkMate) and (not Draw):
        if row>=0 and row<8 and col>=0 and col<8:
            if board_State[row][col]["chess_piece"]!="" and board_State[row][col]["color"]==player_Turn:
                find_Moves(row, col)
                display_Move()
                game_Board.delete(board_State[row][col]["image"])
                img = pieces_Img[board_State[row][col]["color"]][board_State[row][col]["chess_piece"]]
                board_State[row][col]["image"] = game_Board.create_image(e.x, e.y, image=img)
                pickup = True

def move(e):
    
    global board_State, pickup, col, row

    if pickup:
        game_Board.coords(board_State[row][col]["image"], e.x, e.y)

def coord_drop(e):

    global player_Turn, board_State, available_Move, pieces_Pos, pickup, col, row, check_Dist, checkMate, moved_State, blank, pieces_Img, move_List, width_symbol, height_symbol, board_All_state, box_Highlight, highlight_Color

    if pickup:
        new_imgx = int((e.x-20)/70)
        new_imgy = int((e.y-20)/70)
        if new_imgx>=0 and new_imgx<8 and new_imgy>=0 and new_imgy<8 and (new_imgx!=col or new_imgy!=row) and (new_imgy, new_imgx) in available_Move:

            eaten = False
            special = ""
            board_Change = [{
                "coord": (row, col), "piece": board_State[row][col]["chess_piece"], "color": board_State[row][col]["color"], "castle": { BLACK: moved_State[BLACK].copy(), WHITE: moved_State[WHITE].copy()}
            }, {
                "coord": (new_imgy, new_imgx), "piece": board_State[new_imgy][new_imgx]["chess_piece"], "color": board_State[new_imgy][new_imgx]["color"], "castle": { BLACK: moved_State[BLACK].copy(), WHITE: moved_State[WHITE].copy()}
            }]

            while len(box_Highlight)>0:
                game_Board.delete(box_Highlight[len(box_Highlight)-1])
                box_Highlight.pop(len(box_Highlight)-1)

            box_Highlight.append(game_Board.create_rectangle(20+col*70, 20+row*70, 20+(col+1)*70, 20+(row+1)*70, fill=((col*8+row-col)%2==0) and highlight_Color[0] or highlight_Color[1], outline=""))
            box_Highlight.append(game_Board.create_rectangle(20+new_imgx*70, 20+new_imgy*70, 20+(new_imgx+1)*70, 20+(new_imgy+1)*70, fill=((new_imgx*8+new_imgy-new_imgx)%2==0) and highlight_Color[0] or highlight_Color[1], outline=""))

            if board_State[new_imgy][new_imgx]["chess_piece"] != "":
                eaten = True
                disable(new_imgy, new_imgx)
                game_Board.delete(board_State[new_imgy][new_imgx]["image"])
                pieces_Pos[board_State[new_imgy][new_imgx]["color"]][board_State[new_imgy][new_imgx]["chess_piece"]].remove((new_imgy, new_imgx))

            if moved_State[player_Turn]["0-0"]:

                rook_Side = (player_Side==WHITE) and 7 or 0

                if board_State[row][col]["chess_piece"] == "rook" and col==rook_Side:
                    moved_State[player_Turn]["0-0"] = False

                elif board_State[row][col]["chess_piece"] == "king":
                    if (new_imgx-col==2 and player_Side==WHITE) or (new_imgx-col==-2 and player_Side==BLACK):
                        special = "0-0"
                        BoW = (player_Turn==player_Side) and 7 or 0
                        new_rook_Side = new_imgx - int((new_imgx-col)/abs(new_imgx-col))
                        box_Highlight.append(game_Board.create_rectangle(20+rook_Side*70, 20+BoW*70, 20+(rook_Side+1)*70, 20+(BoW+1)*70, fill=((rook_Side*8+BoW-rook_Side)%2==0) and highlight_Color[0] or highlight_Color[1], outline=""))
                        box_Highlight.append(game_Board.create_rectangle(20+new_rook_Side*70, 20+BoW*70, 20+(new_rook_Side+1)*70, 20+(BoW+1)*70, fill=((new_rook_Side*8+BoW-new_rook_Side)%2==0) and highlight_Color[0] or highlight_Color[1], outline=""))
                        game_Board.delete(board_State[BoW][rook_Side]["image"])
                        img = pieces_Img[board_State[BoW][rook_Side]["color"]][board_State[BoW][rook_Side]["chess_piece"]]
                        board_State[BoW][rook_Side]["image"] = game_Board.create_image(rook_Side*70+30, BoW*70+30, anchor=NW, image=img)
                        board_State[BoW][new_rook_Side] = board_State[BoW][rook_Side].copy()
                        board_State[BoW][rook_Side] = blank.copy()
                        board_Change.append({
                            "coord": (BoW, rook_Side), "piece": "rook", "color": player_Turn, "castle": { BLACK: moved_State[BLACK].copy(), WHITE: moved_State[WHITE].copy()}
                        })
                        board_Change.append({
                            "coord": (BoW, new_rook_Side), "piece": "", "color": "", "castle": { BLACK: moved_State[BLACK].copy(), WHITE: moved_State[WHITE].copy()}
                        })
                        pieces_Pos[player_Turn]["rook"].remove((BoW, rook_Side))
                        pieces_Pos[player_Turn]["rook"].append((BoW, new_rook_Side))
                        game_Board.coords(board_State[BoW][new_rook_Side]["image"], new_rook_Side*70+30, BoW*70+30)
                    moved_State[player_Turn]["0-0"] = False

            if moved_State[player_Turn]["0-0-0"]:

                rook_Side = (player_Side==BLACK) and 7 or 0

                if board_State[row][col]["chess_piece"] == "rook" and col==rook_Side:
                    moved_State[player_Turn]["0-0-0"] = False

                elif board_State[row][col]["chess_piece"] == "king":
                    if (new_imgx-col==2 and player_Side==BLACK) or (new_imgx-col==-2 and player_Side==WHITE):
                        special = "0-0-0"
                        BoW = (player_Turn==player_Side) and 7 or 0
                        new_rook_Side = new_imgx - int((new_imgx-col)/abs(new_imgx-col))
                        box_Highlight.append(game_Board.create_rectangle(20+rook_Side*70, 20+BoW*70, 20+(rook_Side+1)*70, 20+(BoW+1)*70, fill=((rook_Side*8+BoW-rook_Side)%2==0) and highlight_Color[0] or highlight_Color[1], outline=""))
                        box_Highlight.append(game_Board.create_rectangle(20+new_rook_Side*70, 20+BoW*70, 20+(new_rook_Side+1)*70, 20+(BoW+1)*70, fill=((new_rook_Side*8+BoW-new_rook_Side)%2==0) and highlight_Color[0] or highlight_Color[1], outline=""))
                        game_Board.delete(board_State[BoW][rook_Side]["image"])
                        img = pieces_Img[board_State[BoW][rook_Side]["color"]][board_State[BoW][rook_Side]["chess_piece"]]
                        board_State[BoW][rook_Side]["image"] = game_Board.create_image(rook_Side*70+30, BoW*70+30, anchor=NW, image=img)
                        board_State[BoW][new_rook_Side] = board_State[BoW][rook_Side].copy()
                        board_State[BoW][rook_Side] = blank.copy()
                        board_Change.append({
                            "coord": (BoW, rook_Side), "piece": "rook", "color": player_Turn, "castle": { BLACK: moved_State[BLACK].copy(), WHITE: moved_State[WHITE].copy()}
                        })
                        board_Change.append({
                            "coord": (BoW, new_rook_Side), "piece": "", "color": "", "castle": { BLACK: moved_State[BLACK].copy(), WHITE: moved_State[WHITE].copy()}
                        })
                        pieces_Pos[player_Turn]["rook"].remove((BoW, rook_Side))
                        pieces_Pos[player_Turn]["rook"].append((BoW, new_rook_Side))
                        game_Board.coords(board_State[BoW][new_rook_Side]["image"], new_rook_Side*70+30, BoW*70+30)
                    moved_State[player_Turn]["0-0-0"] = False

            chess_piece = board_State[row][col]["chess_piece"]

            game_Board.delete(board_State[row][col]["image"])
            img = pieces_Img[board_State[row][col]["color"]][board_State[row][col]["chess_piece"]]
            board_State[row][col]["image"] = game_Board.create_image(row*70+30, col*70+30, anchor=NW, image=img)
            board_State[new_imgy][new_imgx] = board_State[row][col].copy()
            board_State[row][col] = blank.copy()
            pieces_Pos[player_Turn][board_State[new_imgy][new_imgx]["chess_piece"]].remove((row, col))

            if board_State[new_imgy][new_imgx]["chess_piece"] == "pawn":
                if (player_Turn==player_Side and new_imgy==0) or (player_Turn!=player_Side and new_imgy==7):

                    ask = Toplevel()
                    ask.attributes("-toolwindow", 1)
                    ask.title("Promote to")
                    ask.focus_set()
                    ask.grab_set()

                    def change(piece):
                        board_State[new_imgy][new_imgx]["chess_piece"] = piece
                        game_Board.delete(board_State[new_imgy][new_imgx]["image"])
                        img = pieces_Img[board_State[new_imgy][new_imgx]["color"]][board_State[new_imgy][new_imgx]["chess_piece"]]
                        board_State[new_imgy][new_imgx]["image"] = game_Board.create_image(new_imgx*70+30, new_imgy*70+30, anchor=NW, image=img)
                        root.focus_set()
                        ask.protocol("WM_DELETE_WINDOW", lambda: ask.destroy())

                    ask.protocol("WM_DELETE_WINDOW", lambda:0)
                    rook = Button(ask, image=pieces_Img[player_Turn]["rook"], command=lambda : change("rook"))
                    knight = Button(ask, image=pieces_Img[player_Turn]["knight"], command=lambda : change("knight"))
                    bishop = Button(ask, image=pieces_Img[player_Turn]["bishop"], command=lambda : change("bishop"))
                    queen = Button(ask, image=pieces_Img[player_Turn]["queen"], command=lambda : change("queen"))
                    rook.pack(side=LEFT)
                    knight.pack(side=LEFT)
                    bishop.pack(side=LEFT)
                    queen.pack(side=LEFT)
                    root.wait_window(ask)
                    special = "=R" if board_State[new_imgy][new_imgx]["chess_piece"]=="rook" else "=N" if board_State[new_imgy][new_imgx]["chess_piece"]=="knight" else "=B" if board_State[new_imgy][new_imgx]["chess_piece"]=="bishop" else "=Q"

            pieces_Pos[player_Turn][board_State[new_imgy][new_imgx]["chess_piece"]].append((new_imgy, new_imgx))
            coord = print_Moves(eaten, chess_piece, width_symbol[col]+height_symbol[row], width_symbol[new_imgx]+height_symbol[new_imgy], special)
            board_All_state.append((board_Change.copy(), coord))

            next_Move()
            check_Dist = find_Check()
            if check_Dist != -1:
                del_Move()
                checkMate = check_Or_checkmate()
                if checkMate:
                    move_List[coord[1]][coord[0]]["text"] += "#"
                    game_Board.coords(board_State[new_imgy][new_imgx]["image"], new_imgx*70+30, new_imgy*70+30)
                    game_Board.itemconfig(board_State[new_imgy][new_imgx]["image"], anchor=NW)
                    pickup = False
                    alert(WHITE if player_Turn==BLACK else BLACK)
                    return
                elif len(check_Dist)==1:
                    move_List[coord[1]][coord[0]]["text"] += "+"
                else:
                    move_List[coord[1]][coord[0]]["text"] += "++"

            else:
                del_Move()
                staleMate = check_Or_checkmate()
                if staleMate:
                    game_Board.coords(board_State[new_imgy][new_imgx]["image"], new_imgx*70+30, new_imgy*70+30)
                    game_Board.itemconfig(board_State[new_imgy][new_imgx]["image"], anchor=NW)
                    pickup = False
                    Draw = True
                    alert("draw")
                    return

        else:
            new_imgx = col
            new_imgy = row
        del_Move()
        game_Board.coords(board_State[new_imgy][new_imgx]["image"], new_imgx*70+30, new_imgy*70+30)
        game_Board.itemconfig(board_State[new_imgy][new_imgx]["image"], anchor=NW)
        pickup = False




game_Board.bind("<Button-1>", coord_pickup)
game_Board.bind("<B1-Motion>", move)
game_Board.bind("<ButtonRelease-1>", coord_drop)




def new_Game():

    window = Toplevel()
    window.title("")
    window.attributes("-toolwindow", 1)
    window.focus_set()
    window.grab_set()

    sentence = Label(window, text="Which color you want to reset to?")
    White_btn = Button(window, text="White", command=lambda: rewind(WHITE))
    Black_btn = Button(window, text="Black", command=lambda: rewind(BLACK))

    def rewind(color):

        global board_State, pieces_Pos, player_Turn, move_List, checkMate, Draw, turn_Num, check_Dist, moved_State, board_All_state, player_Side

        player_Side = color
        pieces_Pos = {
            "white": {
                "pawn": [],
                "rook": [],
                "knight": [],
                "bishop": [],
                "queen": [],
                "king": []
            },
            "black": {
                "pawn": [],
                "rook": [],
                "knight": [],
                "bishop": [],
                "queen": [],
                "king": []
            }
        }
        for i in range(8):
            for j in range(8):
                game_Board.delete(board_State[i][j]["image"])
        board_State = []
        board_All_state = []
        while len(box_Highlight)>0:
            game_Board.delete(box_Highlight[len(box_Highlight)-1])
            box_Highlight.pop(len(box_Highlight)-1)
        setup_chess_Pieces()
        for i in range(1, 3):
            for j in range(1, 27):
                move_List[i][j]["text"] = ""
        for i in range(4, 6):
            for j in range(1, 27):
                move_List[i][j]["text"] = ""
        Draw = False
        turn_Num = 1
        player_Turn = WHITE
        check_Dist = -1
        moved_State = {
            "white": {
                "0-0": True,
                "0-0-0": True
            },
            "black": {
                "0-0": True,
                "0-0-0": True
            }
        }
        checkMate = False
        window.destroy()

    sentence.pack(side=TOP)
    Black_btn.pack(side=BOTTOM)
    White_btn.pack(side=BOTTOM)
    root.wait_window(window)



def Undo():

    global board_State, player_Turn, turn_Num, board_All_state, move_List, pieces_Pos, checkMate, Draw, check_Dist, moved_State, box_Highlight, highlight_Color

    checkMate = False
    Draw = False
    if turn_Num==1 and player_Turn==WHITE:
        return

    Changes = board_All_state[len(board_All_state)-1]
    length = len(Changes[0])
    for i in range(length):
        y, x = Changes[0][i]["coord"]
        if board_State[y][x]["chess_piece"]:
            game_Board.delete(board_State[y][x]["image"])
        board_State[y][x] = {
            "chess_piece": Changes[0][i]["piece"], "color": Changes[0][i]["color"], "image": ""
        }
        if Changes[0][i]["piece"] != "":
            img = pieces_Img[Changes[0][i]["color"]][Changes[0][i]["piece"]]
            board_State[y][x]["image"] = game_Board.create_image(30+x*70, 30+y*70, anchor=NW, image=img)
    while len(box_Highlight)>0:
        game_Board.delete(box_Highlight[len(box_Highlight)-1])
        box_Highlight.pop(len(box_Highlight)-1)
    move_List[Changes[1][1]][Changes[1][0]]["text"] = ""
    board_All_state.pop(len(board_All_state)-1)

    pieces_Pos = {
        "white": {
            "pawn": [],
            "rook": [],
            "knight": [],
            "bishop": [],
            "queen": [],
            "king": []
        },
        "black": {
            "pawn": [],
            "rook": [],
            "knight": [],
            "bishop": [],
            "queen": [],
            "king": []
        }
    }
    for i in range(8):
        for j in range(8):
            if board_State[i][j]["chess_piece"]!="":
                pieces_Pos[board_State[i][j]["color"]][board_State[i][j]["chess_piece"]].append((i, j))

    if player_Turn==WHITE:
        player_Turn = BLACK
        turn_Num-=1
    else:
        player_Turn = WHITE

    Changes = board_All_state[len(board_All_state)-1]
    length = len(Changes[0])
    moved_State[player_Turn] = Changes[0][0]["castle"][player_Turn].copy()
    for i in range(length):
        y, x = Changes[0][i]["coord"]
        box_Highlight.append(game_Board.create_rectangle(20+x*70, 20+y*70, 20+(x+1)*70, 20+(y+1)*70, fill=((x*8+y-x)%2==0) and highlight_Color[0] or highlight_Color[1], outline=""))
        if board_State[y][x]["chess_piece"]:
            game_Board.delete(board_State[y][x]["image"])
            img = pieces_Img[board_State[y][x]["color"]][board_State[y][x]["chess_piece"]]
            board_State[y][x]["image"] = game_Board.create_image(30+x*70, 30+y*70, anchor=NW, image=img)

    check_Dist = find_Check()




menuBar = Menu(root)
menuBar.add_command(label="New Game", command=lambda: new_Game())
menuBar.add_command(label="Undo", command=lambda: Undo())
root.config(menu=menuBar)




root.mainloop()