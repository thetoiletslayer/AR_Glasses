import pygame
import sys
import os
import datetime
pygame.init()
global rot_screen
rotate = 0
tmp_screen = pygame.display.set_mode((540, 960))
if rotate == 0:
    rot_screen = pygame.display.set_mode((540, 960))
    screen = pygame.display.set_mode((540, 960))
if rotate == 1:
    rot_screen = pygame.display.set_mode((960, 540))
    screen = pygame.display.set_mode((960, 540))
fontsize = 22
bgcolor = (0,0,0)
option = (0,255,0)
selected = (0,255,144)
unavailable = (128,128,128)
font = pygame.font.Font('font.ttf', fontsize)
select = 0
saveback = 0

#center text
#(271 - (.5 * space * len("text")))

#AS LONG AS NOTE1, NOTE2, ETC ARE IN /NOTES IT WILL NOT LOOK LIKE ITS SAVING CORRECTLY
#BECAUSE ITS SAVING AS SEPERATE FILE, TITLED FIRST WORD IN NOTES CONTENTS

def turn_screen():
    global rotate
    if rotate == 1:
        rot_screen = pygame.transform.rotate(pygame.transform.flip(tmp_screen, True, False), 90)
    if rotate == 0:
        rot_screen = tmp_screen
    screen.blit(rot_screen, (0,0))

def mainmenu():
    global space, tmp_screen, rot_screen
    space = font.size(' ')[0]  # The width of a space.
    global fontsize, select
    tmp_screen.fill(bgcolor)
    tword = "AR Glasses"
    title = font.render(tword, True, option)
    #title rect
    pygame.draw.rect(tmp_screen, option, (156, 47, 227, 30), 2)
    menu_options = ["Notepad", "Groceries", "Option 3", "Option 4"]
    tmp_screen.blit(title, (271 - (.5 * space * len(tword)), 50))
    for i in range(len(menu_options)):
        text = font.render(menu_options[i], True, option)
        tmp_screen.blit(text, (271 - (.5 * space * len(menu_options[i])), 200 + i * 50))
    highlight = font.render("«          »", True, option)
    tmp_screen.blit(highlight, (138, 198 + select * 50))
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    date = now.strftime("%Y-%m-%d")
    cur_time = font.render(time, True, option)
    cur_date = font.render(date, True, option)
    tmp_screen.blit(cur_time, (271 - (.5 * space * len(time)), 119))
    tmp_screen.blit(cur_date, (271 - (.5 * space * len(date)), 142))
    pygame.draw.rect(tmp_screen, option, (157, 117, 227, 51), 1)
    
    
def notedraw():
    global space, rot_screen, tmp_screen
    global note_sel
    tmp_screen.fill(bgcolor)
    notitle = "Notepad"
    title = font.render(notitle, True, option)
    tmp_screen.blit(title, (271 - (.5 * space * len(notitle)), 50))
    pygame.draw.rect(tmp_screen, option, (189, 47, 161, 30), 2)
    note_options = ["New", "Open", "Quit"]
    for i in range(len(note_options)):
        text = font.render(note_options[i], True, option)
        tmp_screen.blit(text, (271 - (.5 * space * len(note_options[i])), 100 + i * 50))
    highlight = font.render("«       »", True, option)
    tmp_screen.blit(highlight, (171, 98 + note_sel * 50))
    turn_screen()
    pygame.display.update()

def notepad():
    global space, newnote
    global note_sel, tmp_screen
    back = 0
    note_sel = 0
    while back != 1:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    note_sel -= 1
                    if note_sel < 0:
                        note_sel = 2
                if event.key == pygame.K_DOWN:
                    note_sel += 1
                    if note_sel > 2:
                        note_sel = 0
                if event.key == pygame.K_ESCAPE:
                    back = 1
                if event.key == pygame.K_RETURN:
                    if note_sel == 0:#new
                        newnote = 1
                        new_note()
                    elif note_sel == 1:#open
                        open_note()
                    elif note_sel == 2:#quit
                        back = 1
                        
                        
        notedraw()

def blit_text(surface, text, pos, font, color=pygame.Color(option)):
    global space
    global words, tmp_screen
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    max_width, max_height = surface.get_size()
    max_width -= 240
    max_height -= 100
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width - 120 >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def savenote():
    global new_back
    global words
    global space
    global saveback, tmp_screen
    save_sel = 0
    saveback = 0
    while saveback != 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        save_sel -= 1
                        if save_sel < 0:
                            save_sel = 3
                    if event.key == pygame.K_DOWN:
                        save_sel += 1
                        if save_sel > 3:
                            save_sel = 0
                    if event.key == pygame.K_ESCAPE:
                        saveback = 1
                    if event.key == pygame.K_RETURN:
                        if save_sel == 0:#save and quit
                            new_back = 1
                            f = open(f"notes/{words[0][0]}.txt", "w")
                            f.write(user_text)
                            saveback = 1
                        if save_sel == 1:#save and continue
                            f = open(f"notes/{words[0][0]}.txt", "w")
                            f.write(user_text)
                            saveback = 1
                        if save_sel == 2:#quit nosave
                            new_back = 1
                            saveback = 1
                        if save_sel == 3:#close menu
                            saveback = 1

        pygame.draw.rect(tmp_screen, bgcolor, pygame.Rect(120, 90, 300, 192))
        pygame.draw.rect(tmp_screen, option, pygame.Rect(120, 90, 300, 192), 2)
        save_options = ["Save + Quit", "Save", "Quit", "Close Menu"]
        for i in range(len(save_options)):
            text = font.render(save_options[i], True, option)
            tmp_screen.blit(text, (271 - (.5 * space * len(save_options[i])), 100 + i * 50))
        highlightl = font.render("«", True, option)
        highlightr = font.render("»", True, option)
        tmp_screen.blit(highlightl, (127, 98 + save_sel * 50))
        tmp_screen.blit(highlightr, (392, 98 + save_sel * 50))
        turn_screen()
        pygame.display.update()

def new_note():
    global new_back, newnote, user_text
    global saveback, rot_screen, tmp_screen
    new_back = 0
    
    tmp_screen.fill(bgcolor)
    global user_text
    if newnote == 1:
        user_text = ''
  
    # create rectangle 
    input_rect = pygame.Rect(114, 44, 312, 512)
    while new_back != 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
        
                    # Check for backspace 
                    if event.key == pygame.K_BACKSPACE: 
                        # get text input from 0 to -1 i.e. end. 
                        user_text = user_text[:-1] 
                    # Unicode standard is used for string 
                    # formation 
                    elif event.key == pygame.K_ESCAPE:
                        savenote()
                    else: 
                        user_text += event.unicode
        # draw rectangle and argument passed which should 
        # be on tmp_screen 
        tmp_screen.fill(bgcolor)
        pygame.draw.rect(tmp_screen, option, input_rect, 2) 
    
        blit_text(tmp_screen, user_text, (120, 50), font)
        turn_screen()
        pygame.display.update() 

def open_note():
    global user_text, newnote, rot_screen, tmp_screen
    directory_path = 'notes/'
    no_of_notes = len(os.listdir(directory_path))
    total = no_of_notes
    if total > 10:
        total = 10
    dir_list = os.listdir(directory_path)
    open_back = 0
    open_sel = 0
    scroll = 0
    while open_back != 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if open_sel == 0 and scroll > 0:
                            scroll -= 1
                        if open_sel > 0:
                            open_sel -= 1
                        if open_sel < 0:
                            open_sel = 0
                    if event.key == pygame.K_DOWN:
                        if open_sel == 9 and (i + scroll) < total:
                            scroll += 1
                        if open_sel < 9:
                            open_sel += 1
                        if open_sel > total - 1:
                            open_sel = total - 1
                    if event.key == pygame.K_RETURN:
                        with open(f"notes/{dir_list[open_sel + scroll]}", "r") as f:
                            user_text = f.read().replace('\n', '')
                        open_back = 1
                        newnote = 0
                        new_note()
                    if event.key == pygame.K_ESCAPE:
                        open_back = 1
        tmp_screen.fill(bgcolor)
        oword = "Open"
        title = font.render(oword, True, option)
        tmp_screen.blit(title, (271 - (.5 * space * len(oword)), 51))
        pygame.draw.rect(tmp_screen, option, (140, 42, 260, 39), 2)
        pygame.draw.rect(tmp_screen, bgcolor, pygame.Rect(140, 81, 260, 509))
        pygame.draw.rect(tmp_screen, option, pygame.Rect(140, 81, 260, 509), 1)
        dir_list = os.listdir(directory_path)
        for i in range(total):
            text = font.render(dir_list[i + scroll], True, option)
            tmp_screen.blit(text, (271 - (.5 * space * len(dir_list[i])), 100 + i * 50))
        highlightl = font.render("«", True, option)
        highlightr = font.render("»", True, option)
        tmp_screen.blit(highlightl, (147, 98 + open_sel * 50))
        tmp_screen.blit(highlightr, (372, 98 + open_sel * 50))
        turn_screen()
        pygame.display.update()

def groceries():
    global newlist, rot_screen, tmp_screen
    tmp_screen.fill(bgcolor)
    #add item
    #save list
    #quit
    #list items, can be scrolled/clicked to edit
    groback = 0
    gro_sel = 0
    while groback != 1:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    gro_sel -= 1
                    if gro_sel < 0:
                        gro_sel = 2
                if event.key == pygame.K_DOWN:
                    gro_sel += 1
                    if gro_sel > 2:
                        gro_sel = 0
                if event.key == pygame.K_ESCAPE:
                    groback = 1
                if event.key == pygame.K_RETURN:
                    if gro_sel == 0:#edit
                        newlist = 1
                        edit_list()
                    elif gro_sel == 1:#view
                        view_list()
                    elif gro_sel == 2:#quit
                        groback = 1
        tmp_screen.fill(bgcolor)
        grotitle = "Groceries"
        title = font.render(grotitle, True, option)
        tmp_screen.blit(title, (271 - (.5 * space * len(grotitle)), 50))
        pygame.draw.rect(tmp_screen, option, (167, 47, 205, 30), 2)
        groc_options = ["Edit", "View", "Quit"]
        for i in range(len(groc_options)):
            text = font.render(groc_options[i], True, option)
            tmp_screen.blit(text, (271 - (.5 * space * len(groc_options[i])), 100 + i * 50))
        highlight = font.render("«       »", True, option)
        tmp_screen.blit(highlight, (171, 98 + gro_sel * 50))
        turn_screen()
        pygame.display.update()

def edit_list():
    #list items, scrollable
    from categories import aisles
    global gro_list, srtlist, rot_screen, tmp_screen
    from grolist import gro_list
    global geditback, item_tot
    global input_rect, item_text, newlist, newitem
    if newlist == 1:
        newlist = 0
        item_text = ''
    cat = 0
    scroll = 0
    spacing = 62
    geditback = 0
    gedit_sel = 0
    while geditback != 1:
        item_tot = min(10, len(gro_list))#displayed items max 10
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if gedit_sel == 3 and scroll > 0:
                        scroll -= 1
                    else:
                        gedit_sel -= 1
                    if gedit_sel < 0:
                        gedit_sel = 0
                if event.key == pygame.K_DOWN:
                    if gedit_sel < 2 + item_tot:
                        gedit_sel += 1
                    elif gedit_sel > 2 + item_tot:
                        gedit_sel = 0
                        scroll = 0
                    elif gedit_sel == 2 + item_tot:
                        scroll += 1
                    if gedit_sel + scroll > len(gro_list) + 2:
                        scroll -= 1
                if event.key == pygame.K_LEFT:
                    cat -= 1
                    if cat < 0:
                        cat = len(aisles) - 1
                if event.key == pygame.K_RIGHT:
                    cat += 1
                    if cat > len(aisles) - 1:
                        cat = 0
                if event.key == pygame.K_ESCAPE:
                    savelist()
                if event.key == pygame.K_RETURN:
                    if gedit_sel == 0:#Item name
                        newitem = 1
                        if item_text != '':
                            newitem = 0
                        item_name()
                    elif gedit_sel == 2:#add item
                        templist = [item_text, aisles[cat][1]]
                        srtlist.append(templist)
                        gro_list = sorted(srtlist, key=lambda x: x[1])
                        item_text = ''
                        cat = 0
                        gedit_sel = 0
                        
        tmp_screen.fill(bgcolor)
        gedititle = "Edit List"
        title = font.render(gedititle, True, option)
        tmp_screen.blit(title, (271 - (.5 * space * len(gedititle)), 50))
        #title box
        pygame.draw.rect(tmp_screen, option, (167, 47, 205, 30), 2)
        
        
        itname = font.render("Item Name", True, option)
        tmp_screen.blit(itname, (271 - (.5 * space * 9), 100))
        caname = font.render("Category", True, option)
        tmp_screen.blit(caname, (273 - (.5 * space * 8), 162))
        #list box
        pygame.draw.rect(tmp_screen, option, (110, 269, 320, 314), 1)
        if gro_list != []:
            for i in range(item_tot):
                text = font.render(gro_list[i + scroll][0], True, option)
                tmp_screen.blit(text, (273 - (.5 * space * len(gro_list[i + scroll][0])), 270 + i * 32))
        highlightl = font.render("«", True, option)
        highlightr = font.render("»", True, option)
        listfix = 0
        if gedit_sel == 0:#item name
            spacing = 62
            hwide = 126
            listfix = -2
        if gedit_sel == 1:#category
            spacing = 62
            hwide = .5 * space * (len(aisles[cat][0]) + 2)
        if gedit_sel == 2:#add item
            spacing = 47
            hwide = 108
            listfix = 0
        if gedit_sel > 2:
            listfix = 42
            spacing = 32
            hwide = (len(gro_list[gedit_sel + scroll - 3][0]) + 2) * (.5 * space)
        #   items start displaying at 90 + i * 32
        tmp_screen.blit(highlightl, (260 - hwide, 130 + listfix + gedit_sel * spacing))
        tmp_screen.blit(highlightr, (262 + hwide, 130 + listfix + gedit_sel * spacing))
        categ = font.render(aisles[cat][0], True, option)
        cx = (272 - (.5 * space * len(aisles[cat][0])))
        tmp_screen.blit(categ, (cx, 194))
        add_btn = font.render("Add Item", True, option)
        tmp_screen.blit(add_btn, (273 - .5 * space * 8, 226))
        #category box
        pygame.draw.rect(tmp_screen, option, (cx - 3, 193, len(aisles[cat][0]) * space + 3, 26), 1)
        #add item box
        pygame.draw.rect(tmp_screen, option, (182, 225, 180, 26), 1)
        #rectangle definition for bg and item name
        input_rect = pygame.Rect(160, 130, 223, 26)
        #bg color for item name box 
        pygame.draw.rect(tmp_screen, bgcolor, input_rect)
        #item name box
        pygame.draw.rect(tmp_screen, option, input_rect, 1)
        iname = font.render(item_text, True, option)
        tmp_screen.blit(iname, (163, 131))
        turn_screen()
        pygame.display.update()
        
#131, 193, 214
def item_name():
    global newitem, rot_screen, tmp_screen
    global input_rect, item_text
    if newitem == 1:
        item_text = ''
    name_back = 0
    while name_back != 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
        
                    # Check for backspace 
                    if event.key == pygame.K_BACKSPACE: 
                        # get text input from 0 to -1 i.e. end. 
                        item_text = item_text[:-1]
                    # Unicode standard is used for string 
                    # formation 
                    elif event.key == pygame.K_RETURN:
                        name_back = 1
                    else: 
                        if len(item_text) < 10:
                            item_text += event.unicode
         
        pygame.draw.rect(tmp_screen, bgcolor, input_rect)
        pygame.draw.rect(tmp_screen, option, input_rect, 1)
        cursor = font.render("_", True, option)
        tmp_screen.blit(cursor, (163 + space * len(item_text), 131))
        blit_text(tmp_screen, item_text, (163, 131), font)
        turn_screen()
        pygame.display.update() 

def savelist():
    global gro_list, srtlist
    global words, item_tot
    global space, rot_screen, tmp_screen
    global gsaveback, geditback
    gsave_sel = 0
    gsaveback = 0
    while gsaveback != 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        gsave_sel -= 1
                        if gsave_sel < 0:
                            gsave_sel = 4
                    if event.key == pygame.K_DOWN:
                        gsave_sel += 1
                        if gsave_sel > 4:
                            gsave_sel = 0
                    if event.key == pygame.K_ESCAPE:
                        gsaveback = 1
                    if event.key == pygame.K_RETURN:
                        if gsave_sel == 0:#save and quit
                            f = open(f"grolist.py", "w")
                            f.write("gro_list = [")
                            f.write("\n")
                            track = 0
                            for l in gro_list:
                                f.write(str(l))
                                if track < len(gro_list) - 1:
                                    f.write(",")
                                f.write("\n")
                                track += 1
                            f.write("]")
                            f.close()
                            gsaveback = 1
                            geditback = 1
                        if gsave_sel == 1:#save and continue
                            f = open(f"grolist.py", "w")
                            f.write("gro_list = [")
                            f.write("\n")
                            track = 0
                            for l in gro_list:
                                f.write(str(l))
                                if track < len(gro_list) - 1:
                                    f.write(",")
                                f.write("\n")
                                track += 1
                            f.write("]")
                            f.close()
                            gsaveback = 1
                        if gsave_sel == 2:#clear list
                            gro_list = []
                            srtlist = []
                            item_tot = 0
                            gsaveback = 1
                        if gsave_sel == 3:#quit nosave
                            geditback = 1
                            gsaveback = 1
                        if gsave_sel == 4:#close menu
                            gsaveback = 1

        pygame.draw.rect(tmp_screen, bgcolor, pygame.Rect(118, 90, 303, 244))
        pygame.draw.rect(tmp_screen, option, pygame.Rect(118, 90, 303, 244), 2)
        save_options = ["Save + Quit", "Save", "New", "Quit", "Back"]
        for i in range(len(save_options)):
            text = font.render(save_options[i], True, option)
            tmp_screen.blit(text, (271 - (.5 * space * len(save_options[i])), 100 + i * 50))
        highlightl = font.render("«", True, option)
        highlightr = font.render("»", True, option)
        tmp_screen.blit(highlightl, (122, 98 + gsave_sel * 50))
        tmp_screen.blit(highlightr, (397, 98 + gsave_sel * 50))
        turn_screen()
        pygame.display.update()

def view_list():
    global gro_list
    from grolist import gro_list
    global viewback, rot_screen, tmp_screen
    viewback = 0
    view_sel = 0
    scroll = 0
    global product

    while viewback != 1:
        item_tot = min(10, len(gro_list))#displayed items max 10
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        finishlist()
                    if event.key == pygame.K_UP:
                        if view_sel == 0 and scroll >0:
                            scroll -= 1
                        else:
                            view_sel -= 1
                        if view_sel < 0:
                            view_sel = 0
                    if event.key == pygame.K_DOWN:
                        if view_sel < 9:
                            view_sel += 1
                        elif view_sel == 9 and scroll < len(gro_list) - 10:
                            scroll += 1
                    if event.key == pygame.K_RETURN:
                        product = view_sel + scroll
                        item_select()
        
        tmp_screen.fill(bgcolor)
        highlightl = font.render("«", True, option)
        highlightr = font.render("»", True, option)
        hwide = (len(gro_list[view_sel + scroll][0]) + 4) * (.5 * space)
        tmp_screen.blit(highlightl, (257 - hwide, 29 + view_sel * 32))
        tmp_screen.blit(highlightr, (263 + hwide, 29 + view_sel * 32))

        if gro_list != []:
            for i in range(item_tot):
                itemwords = gro_list[i + scroll][0] + "  " + str(gro_list[i + scroll][1])
                text = font.render(itemwords, True, option)
                tmp_screen.blit(text, (271 - (.5 * space * len(itemwords)), 32 + i * 32))
        turn_screen()
        pygame.display.update()

def item_select():
    global item_back
    item_back = 0
    item_sel = 0
    global product, rot_screen, tmp_screen
    global gro_list
    while item_back != 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        item_sel -= 1
                        if item_sel < 0:
                            item_sel = 1
                    if event.key == pygame.K_DOWN:
                        item_sel += 1
                        if item_sel > 1:
                            item_sel = 0
                    if event.key == pygame.K_ESCAPE:
                        item_back = 1
                    if event.key == pygame.K_RETURN:
                        if item_sel == 0:
                            del gro_list[product]
                            item_back = 1
                        if item_sel == 1:#save and quit
                            item_back = 1

        pygame.draw.rect(tmp_screen, bgcolor, pygame.Rect(140, 90, 260, 241))
        pygame.draw.rect(tmp_screen, option, pygame.Rect(140, 90, 260, 241), 2)
        item_options = ["In Cart", "Cancel"]
        for i in range(len(item_options)):
            text = font.render(item_options[i], True, option)
            tmp_screen.blit(text, (172 + (.5 * space * (11 - len(item_options[i]))), 100 + i * 50))
        highlightl = font.render("«", True, option)
        highlightr = font.render("»", True, option)
        tmp_screen.blit(highlightl, (150, 98 + item_sel * 50))
        tmp_screen.blit(highlightr, (374, 98 + item_sel * 50))
        turn_screen()
        pygame.display.update()

def finishlist():
    fin_back = 0
    fin_sel = 0
    global viewback, rot_screen, tmp_screen
    global product
    global gro_list
    while fin_back != 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        fin_sel -= 1
                        if fin_sel < 0:
                            fin_sel = 2
                    if event.key == pygame.K_DOWN:
                        fin_sel += 1
                        if fin_sel > 2:
                            fin_sel = 0
                    if event.key == pygame.K_ESCAPE:
                        fin_back = 1
                    if event.key == pygame.K_RETURN:
                        if fin_sel == 0:#finish shopping and save list
                            f = open(f"grolist.py", "w")
                            f.write("gro_list = [")
                            f.write("\n")
                            track = 0
                            for l in gro_list:
                                f.write(str(l))
                                if track < len(gro_list) - 1:
                                    f.write(",")
                                f.write("\n")
                                track += 1
                            f.write("]")
                            f.close()
                            fin_back = 1
                            viewback = 1
                        if fin_sel == 1:
                            fin_back = 1
                            viewback = 1
                        if fin_sel == 2:#cancel
                            fin_back = 1

        pygame.draw.rect(tmp_screen, bgcolor, pygame.Rect(120, 90, 300, 141))
        pygame.draw.rect(tmp_screen, option, pygame.Rect(120, 90, 300, 141), 2)
        item_options = ["Finish List", "Quit", "Cancel"]
        for i in range(len(item_options)):
            text = font.render(item_options[i], True, option)
            tmp_screen.blit(text, (271 - (.5 * space * len(item_options[i])), 100 + i * 50))
        highlightl = font.render("«", True, option)
        highlightr = font.render("»", True, option)
        tmp_screen.blit(highlightl, (125, 98 + fin_sel * 50))
        tmp_screen.blit(highlightr, (394, 98 + fin_sel * 50))
        turn_screen()
        pygame.display.update()

def option3():
    pass

def option4():
    pass

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                select -= 1
                if select < 0:
                    select = 3
            if event.key == pygame.K_DOWN:
                select += 1
                if select > 3:
                    select = 0
            if event.key == pygame.K_RETURN:
                if select == 0:
                    notepad()
                elif select == 1:
                    select = 0
                    groceries()
                elif select == 2:
                    select = 0
                    option3()
                elif select == 3:
                    select = 0
                    option4()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    mainmenu()
    turn_screen()
    pygame.display.update()