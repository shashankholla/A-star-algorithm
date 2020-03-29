import pygame
import math
path = []
end = -1

update = False

def eD(sX, sY, dX, dY):
    return math.sqrt((pow((sX - dX),2)+ pow((sY - dY),2)))                            



class Cell:
    def __init__(self, x,y):
        self.visited = False
        self.obstacle = False
        self.isPath = False
        self.isSource = False
        self.isDest = False
        self.g = 999999
        self.l = 999999
        self.parent = None
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "(x:{},y:{}, parent:{}, l:{},g:{}, v:{})\n".format(self.x, self.y, self.parent, self.l, self.g, self.visited)

def solve(cells, source, dest, hcells, wcells, border):
    global end
    for cell in cells:
        cell.g = 999999
        cell.l = 999999
        cell.parent = None
        cell.isPath = False
        cell.visited = False
        

    sourceCell = cells[source]
    destCell = cells[dest]
    
    sourceCell.g = eD(sourceCell.x, sourceCell.y, destCell.x, destCell.y)
    sourceCell.l = 0
    
    queue = [cells[source]]
    
    
    
    while len(queue) != 0:
        
        queue = sorted(queue, key=lambda x : x.g)
        #print(queue)
        
        if((queue[0].y*wcells+queue[0].x) == dest):
            #print("Done")
            break
        
        while(len(queue) != 0 and queue[0].visited):
            #print("Removing queue[0]", queue[0])
            queue.pop(0)
        
        if(len(queue) == 0):
            break
        thisCell = queue[0]
        thisCell.visited = True
        
        x = [0, 0, 1, -1]
        y = [1, -1, 0, 0]
        for i in range(4):
            if thisCell.x + x[i] < wcells and thisCell.x + x[i] >= 0 :
                    if thisCell.y + y[i] < hcells and thisCell.y + y[i] >= 0 :
                        nX = thisCell.x + x[i]
                        nY = thisCell.y + y[i]
                        neighbourCell = cells[nY*hcells + nX]
                        
                        if not neighbourCell.visited and not neighbourCell.obstacle:
                            queue.append(neighbourCell)
                            #print("Appending", neighbourCell)
                            if( eD(thisCell.x,thisCell.y,neighbourCell.x,neighbourCell.y) + thisCell.l < neighbourCell.l ):
                                neighbourCell.l =  eD(thisCell.x,thisCell.y,neighbourCell.x,neighbourCell.y) + thisCell.l
                                neighbourCell.g = neighbourCell.l + eD(neighbourCell.x,neighbourCell.y, cells[dest].x, cells[dest].y)
                                neighbourCell.parent = thisCell.y*wcells + thisCell.x
                            #    print("Updating:", neighbourCell.g)
        
    end = dest
                            
        
    



def redraw(screen, cells, h, w, border, cell_size, myfont):
 global end,update
 screen.fill(background)
 x = 0
 y = 0
 for i in range(h):
    y += border
    for j in range(w):
        x += border
        cell = cells[i*h + j]
        color = (200,60,255)
        if cell.visited:
            color = (0,0,255)
        if cell.isPath:
            color = (0,100,100)
        if cell.obstacle:
            color = (125,125,125)
        if cell.isSource:
            color = (125,0,0)
        if cell.isDest:
            color = (0,125,0)    
        
        
        pygame.draw.rect(screen, color, pygame.Rect(x,y,cell_size, cell_size),0 )
        pygame.display.update()
        x += border
    y += border    
    x = 0   
    pathInfo = ''
    if(cells[end].parent == None and update):
        pathInfo = "No path"

    while(cells[end].parent != None and end != source):
        cells[end].isPath = True
        temp = cells[end].parent
         
        pygame.draw.line(screen, (255,255,255),((cells[end].x+1)*2*border - (border/2),(cells[end].y+1)*2*border-(border/2)),((cells[temp].x+1)*2*border- (border/2),(cells[temp].y+1)*2*border- (border/2)))
        
        end = temp
    update = False
    ws, hs = pygame.display.get_surface().get_size()

    textsurface = myfont.render('Source: Shift+Click;', True, (255,255,255))
    screen.blit(textsurface,(0,hs-100))
    
    textsurface = myfont.render('Dest: Alt+Click;', True, (255,255,255))
    screen.blit(textsurface,(0,hs-75))
    
    textsurface = myfont.render('Obstacle: Ctrl+Click;', True, (255,255,255))
    screen.blit(textsurface,(0,hs-50))
    textsurface = myfont.render(pathInfo, True, (255,255,255))
    screen.blit(textsurface,(0,hs-25))


if __name__ == "__main__":
    
    border = 20
    (wcells, hcells) = (10,10)
    (w, h) = (border*2*(wcells+1), border*2*(hcells+1)+75)

    background = (0,0,0)
    screen = pygame.display.set_mode((w,h))
    screen.fill(background)
    pygame.display.set_caption("A start")
    pygame.display.flip()
    pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
    myfont = pygame.font.SysFont('Consolas', 20)

    cell_size = border
    (x,y) = (0,0)
    cells = []

    for i in range(hcells):
        for j in range(wcells):
            cells.append(Cell(j,i))
        x = 0   
    redraw(screen, cells, hcells, wcells, border,cell_size, myfont)

 
    loop = True
    mouse = False
    cbutton = False
    sbutton = False
    abutton = False
    source = -1
    dest = -1


    while loop:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                loop = False
                break
            if(event.type == pygame.MOUSEBUTTONDOWN):
                update = True   
                mouse = True
                pos = pygame.mouse.get_pos()
                if((pos[0]%(2*border) > border) and (pos[1]%(2*border) > border)):
                    (xclick,yclick) = (pos[0] // (2*border),pos[1] // (2*border))
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LCTRL):
                    cbutton = True
                if(event.key == pygame.K_LSHIFT):
                    sbutton = True   
                if(event.key == pygame.K_LALT):
                    abutton = True                    
            elif(event.type == pygame.KEYUP):
                cbutton = False
                sbutton = False
                abutton = False
            elif(event.type == pygame.MOUSEBUTTONUP):
                mouse = False
            if(mouse and cbutton): 
                cells[yclick*wcells + xclick].obstacle = not cells[yclick*wcells + xclick].obstacle
                
            if(mouse and sbutton): 
                if (yclick*wcells + xclick) == source:
                    source = -1
                    cells[yclick*wcells + xclick].isSource = False
                else:
                    if source != -1:
                        cells[source].isSource = False
                    source = yclick*wcells + xclick
                    cells[yclick*wcells + xclick].isDest = False
                    cells[yclick*wcells + xclick].isSource = True
                
                
            if(mouse and abutton): 
                if (yclick*wcells + xclick) == dest:
                    dest = -1
                    cells[yclick*wcells + xclick].isDest = False
                else:
                    if dest != -1:
                        cells[dest].isDest = False
                    dest = yclick*wcells + xclick
                    cells[yclick*wcells + xclick].isDest = True
                    cells[yclick*wcells + xclick].isSource = False
        if(source != -1 and dest != -1 and update):
            solve(cells, source, dest, hcells, wcells,border)
        if(update):
            
            redraw(screen, cells, hcells, wcells, border,cell_size, myfont)