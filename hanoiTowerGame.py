import pygame
import time


class Hanoi_tower():
    def __init__(self):
        # Window settings 
        self.screen = pygame.display.set_mode([900, 350])
        pygame.display.set_caption('Hanoi Tower')
        # button to run hanoi tower solving code  
        self.solve_button = pygame.Rect(10, 10, 30, 30)
        
        self.game_data_init()
        
        running = True
        while running:
            self.draw_game()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        self.pos = event.pos # update cursour pos
                        # if clicked solve_button 
                        if (10 < event.pos[0] < 40):
                            if ( 10 < event.pos[1] < 40):
                                if len(self.r1["rod"]) != 0:    
                                    self.hanoi(len(self.r1["rod"]), self.r1, self.r2, self.r3)
                                    
                        # if clicked on last disk of tower
                        for i, r in enumerate([self.r1, self.r2, self.r3]):
                            if ((self.rod_start_x*(i+0.5))-(self.rod_start_x)/2 < event.pos[0] < (self.rod_start_x*(i+0.5))+(self.rod_start_x)/2):
                                if ((self.disks*self.disk_height) - (len(r["rod"])-1)*self.disk_height) < event.pos[1] <((self.disks*self.disk_height) - (len(r["rod"])-2)*self.disk_height):
                                    self.to_move .append(r);   
                                    self.now_moving = True 
                                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.pos = event.pos # update cursour pos
                        # if clicked in range of rod, append rod to "to move"
                        for i, r in enumerate([self.r1, self.r2, self.r3]):
                            if ((self.rod_start_x*(i+0.5))-(self.rod_start_x)/2 < event.pos[0] < (self.rod_start_x*(i+0.5))+(self.rod_start_x)/2):
                                self.to_move .append(r);
                        try:
                            mid = self.r1 if (self.to_move[0] != self.r1 and self.to_move[1] != self.r1) else self.r2
                            mid = self.r3 if (self.to_move[0] != self.r3 and self.to_move[1] != self.r3) else mid
                            self.move(self.to_move[0], mid, self.to_move [1])
                            self.to_move = []
                        except:
                            self.to_move  = []
                        self.now_moving = False
                        
                elif event.type == pygame.MOUSEMOTION:
                    # if mouse moving, update pos
                    if self.to_move != []:
                        self.pos = event.pos 
     
        pygame.quit()

    def game_data_init(self): 
        # rods 
        # number used for sorting, array for drawing and solving
        self.r1 = {"n":1, "rod":[7, 6, 5, 4, 3, 2, 1]}
        self.r2 = {"n":2, "rod":[]}
        self.r3 = {"n":3, "rod":[]}
        # for drag and drop and contols (move disk from rod to rod)
        self.to_move = []
        self.now_moving = False
        self.pos = (0, 0) # cursour current pos
        # data for disk drawing 
        self.disk_width_multiplyer = 35;
        self.disk_height = 40
        self.rod_start_x = 300
        self.rod_start_y = 100
        self.disk_round_deg = 50
        self.disks = 7
    
    def drag_disk(self, rod, pos):
        disk_size = rod["rod"][-1] * self.disk_width_multiplyer
        disk = pygame.Rect(pygame.Rect(0, 0, disk_size, self.disk_height))
        disk.move_ip(self.pos[0]-(disk_size)/2, pos[1]-(self.disk_height)/2)            
        pygame.draw.rect(self.screen, (100, 0, 255), disk, 0, self.disk_round_deg)
    
    def draw_game(self):
        self.screen.fill((255, 255, 255))
        self.draw_solve_button()
        self.draw_rods()
        self.draw_disks()
        # if drag, draw disk at cursour 
        if self.now_moving == True:
            self.drag_disk(self.to_move[0], self.pos)
        pygame.display.flip()
        
    def draw_disks(self):
        for number, rod in enumerate([self.r1["rod"], self.r2["rod"], self.r3["rod"]]):
            x = self.rod_start_x * (number+0.5)
            for i, disk in enumerate(rod):
                disk_size = rod[i] * self.disk_width_multiplyer
                disk = pygame.Rect(pygame.Rect(0, 0, disk_size, self.disk_height))
                disk.move_ip(x-(disk_size)/2, self.rod_start_y+180 - i*self.disk_height)         
                #draw disk
                pygame.draw.rect(self.screen, ((i*36)%255, (i*36)%255, (100 - i * 8)%255), disk, 0, self.disk_round_deg)
                # draw border
                #pygame.draw.rect(self.screen, ((100 - i * 8)%255, (100 - i * 8)%255, (i*36)%255), disk, 1, self.disk_round_deg)
    
    def draw_rods(self):
        for i in range(3):
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(pygame.Rect(self.rod_start_x*(i+0.5)-5, self.rod_start_y-40, 10, 255)), 1, 50)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(pygame.Rect(self.rod_start_x*(i+0.5)-135, self.rod_start_y+220, 270, 20)), 1, 50)    
        
    def draw_solve_button(self):
        pygame.draw.rect(self.screen, (50, 200, 50), self.solve_button);

    # sort rods   
    def sort(self, rods):
        for i in range(2):
            for j in range(0, 3-i-1):
                if  rods[j]["n"] > rods[j+1]["n"]: 
                    rods[j], rods[j + 1] = rods[j + 1], rods[j]
        return rods

    # Save rods in right order (to draw correctly)
    def save(self, start, mid, end):
        array = self.sort([start, mid, end])
        self.r1 = array[0]
        self.r2 = array[1]
        self.r3 = array[2]

    # Move disk from start rod to end rod 
    def move(self, start, mid, end, wait=None):
        if wait: # display steps
            self.draw_game()
            time.sleep(0.1)
        try: # check if end rod is empty or disk from start < disk from end
            if end["rod"] == [] or (end["rod"][-1] > start["rod"][-1]):
                end["rod"].append(start["rod"].pop(-1)) # move rod
                self.save(start, mid, end) # save rods in right order 
        except: # works when start rod is empty
            pass
    
    # Solve hanoi tower
    def hanoi(self, n, start, mid, end):
        if n == 1:
            self.move(start, mid, end)
        else:
            self.hanoi(n - 1, start, end, mid)
            self.move(start, mid, end, True)
            self.hanoi(n - 1, mid, start, end)

Hanoi_tower()