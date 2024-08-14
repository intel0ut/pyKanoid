import random
import pygame
import sys

game_dir="."

pygame.init()
pygame.mixer.init() # add this line
pygame.font.init()
random.seed(version=2)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200,800))
screen_rect=screen.get_rect()
pygame.display.set_caption("Pykanoid Re:Zero")
bgcolor=pygame.Color(10,10,10,255) # dark grey

def load_rsrc():
    rsrc={}
    try:
        rsrc['player_bar']=pygame.image.load(game_dir + "\\resources\\player_bar.png")
        rsrc['ball']=pygame.image.load(game_dir + "\\resources\\ball.png")
        rsrc['block_r']=pygame.image.load(game_dir + "\\resources\\block_r.png")
        rsrc['block_g']=pygame.image.load(game_dir + "\\resources\\block_g.png")
        rsrc['block_b']=pygame.image.load(game_dir + "\\resources\\block_b.png")
        rsrc['block_o']=pygame.image.load(game_dir + "\\resources\\block_o.png")
        rsrc['block_y']=pygame.image.load(game_dir + "\\resources\\block_y.png")
        rsrc['block_v']=pygame.image.load(game_dir + "\\resources\\block_v.png")
        rsrc['boing1']=pygame.mixer.Sound(game_dir + "\\resources\\sound\\boing2.ogg")
        rsrc['boing2']=pygame.mixer.Sound(game_dir + "\\resources\\sound\\boing1.ogg")
        # rsrc['music1']=pygame.mixer.music.load(game_dir + "\\resources\\sound\\Danijel Zambo - Chip Mode.ogg")
        # rsrc['music1']=pygame.mixer.music.load(game_dir + "\\resources\\sound\\Kevin MacLeod - Bit Shift.ogg")
        rsrc['music1']=pygame.mixer.music.load(game_dir + "\\resources\\sound\\Kevin MacLeod - Cyborg Ninja.ogg")
        rsrc['font1']=pygame.font.Font(game_dir + "\\resources\\fonts\\Forte.ttf", 42)

    except FileNotFoundError:
        rsrc=[]
        return False
    return rsrc

def detect_border_coll(scr,rect):
    x0_coll=x1_coll=y0_coll=y1_coll=False
    if rect.x <=0:
        x0_coll=True
    if rect.x + rect.width >= scr.width:
        x1_coll=True
    if rect.y <= scr.top:
        y0_coll=True
    if rect.y + rect.height >= scr.height:
        y1_coll=True
    return x0_coll,x1_coll,y0_coll,y1_coll

def draw_blocks(rsrc, max_lines, max_cols):
    blocks=[[0 for i in range(max_cols)] for j in range(max_lines)]
    block_rects=[[0 for i in range(max_cols)] for j in range(max_lines)]
    block_count=0
    for line in range(2,max_lines):
        for col in range(0,max_cols):
            if random.randint(0,100) >= 10:
                block=random.choice(('block_r','block_g','block_b','block_o','block_y','block_v'))
                blocks[line][col]=pygame.Surface.copy(rsrc[block])
                block_rects[line][col]=blocks[line][col].get_rect()
                block_rects[line][col].centerx=(col*60)+30
                block_rects[line][col].centery=int((line*25)+13)
                block_count+=1
            else:
                blocks[line][col]=None
                block_rects[line][col]=None
    return blocks, block_rects, block_count

def main():
    # start here
    rsrc=load_rsrc()
    if not rsrc:
        print("can't find resources!")
        pygame.font.quit()
        pygame.mixer.quit() # add this line
        pygame.quit()
        sys.exit(1)

    ## game variables
    score=0
    lifes=5
    game_over=False

    # player initial state
    rsrc['player_bar'].set_colorkey('#0a0a0a')
    player_bar_rect=rsrc['player_bar'].get_rect()
    pl_last_x=int(((screen_rect.width)/2))
    pl_last_y=int((screen_rect.height)-40)
    player_bar_rect.centerx=pl_last_x
    player_bar_rect.centery=pl_last_y
    pl_spd=8

    # ball initial state
    rsrc['ball'].set_colorkey('#0a0a0a')
    ball_rect=rsrc['ball'].get_rect()
    ball_last_x=int(((screen_rect.width)/2))
    ball_last_y=int((screen_rect.height)-68)
    ball_rect.centerx=ball_last_x
    ball_rect.centery=ball_last_y
    ball_spd=6
    bl_last_x=ball_spd # initial movement to the right
    bl_last_y=-ball_spd # and up 
    ball_moving=False

    # blocks inital state
    max_lines=15 # lines of blocks
    max_cols=20 # max blocks per line
    rsrc['block_r'].set_colorkey('#0a0a0a')
    rsrc['block_g'].set_colorkey('#0a0a0a')
    rsrc['block_b'].set_colorkey('#0a0a0a')
    rsrc['block_o'].set_colorkey('#0a0a0a')
    rsrc['block_y'].set_colorkey('#0a0a0a')
    rsrc['block_v'].set_colorkey('#0a0a0a')

    blocks, block_rects, block_count = draw_blocks(rsrc, max_lines, max_cols)

    # start music
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)

    while True:
        screen.fill(bgcolor)
        ### Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.font.quit()
                pygame.mixer.quit() # add this line
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.font.quit()
                    pygame.mixer.quit() # add this line
                    pygame.quit()
                    sys.exit()
                #player started game
                if event.key == pygame.K_SPACE and not ball_moving:
                    ball_moving=True
        # move player
        keys = pygame.key.get_pressed()
        pl_last_x=0
        pl_last_y=0
        if keys[pygame.K_LEFT]:
            pl_last_x=-pl_spd
        if keys[pygame.K_RIGHT]:
            pl_last_x=pl_spd

        ### Update screen
        # detect player borders
        x0_coll,x1_coll,y0_coll,y1_coll=detect_border_coll(screen_rect,player_bar_rect)
        if x0_coll:
            pl_last_x=pl_spd
        if x1_coll:
            pl_last_x=-pl_spd
        
        # if game_over:
        #     ball_moving=False

        # move player
        player_bar_rect=player_bar_rect.move(pl_last_x,pl_last_y)
        if not ball_moving:
            # move ball together with player if we have not started
            ball_rect=ball_rect.move(pl_last_x, 0)

        if ball_moving:
            # detect ball borders
            playable_rect=pygame.Rect.copy(screen_rect)
            playable_rect.top=screen_rect.top+((rsrc['block_r'].get_rect().height)*2)
            x0_coll,x1_coll,y0_coll,y1_coll=detect_border_coll(playable_rect,ball_rect)
            if x0_coll:
                bl_last_x=abs(bl_last_x)
            if x1_coll:
                bl_last_x=abs(bl_last_x)*-1
            if y0_coll: # hit top
                bl_last_y=ball_spd
            if y1_coll: # game over
                print('player lost!')
                lifes-=1
                if lifes<0:
                    game_over=True
                    blocks, block_rects, block_count = draw_blocks(rsrc, max_lines, max_cols)
                    lifes=5
                    score=0
                ball_rect.centerx=player_bar_rect.centerx
                ball_rect.centery=player_bar_rect.top-(ball_rect.height/2)
                bl_last_x=ball_spd # initial movement to the right
                bl_last_y=-ball_spd # and up 
                ball_moving=False
                ball_rect=ball_rect.move(bl_last_x, bl_last_y)

            # detect ball collision with player
            if ball_rect.colliderect(player_bar_rect):
                pygame.mixer.Sound.play(rsrc['boing1'])

                # exactly center of bar
                if ball_rect.centerx == player_bar_rect.centerx:
                    bl_last_x=0
                
                # extreme left
                if ball_rect.centerx <= (player_bar_rect.left+(player_bar_rect.width/4)):
                    bl_last_x=(abs(bl_last_x)+2)*-1 # invert movement
                
                #extreme right
                if ball_rect.centerx >= (player_bar_rect.left+(player_bar_rect.width/4)*3):
                    bl_last_x=abs(bl_last_x)+2 # invert movement
                
                if ball_rect.centerx != player_bar_rect.centerx and \
                   ball_rect.centerx >= (player_bar_rect.left+(player_bar_rect.width/4)) and \
                   ball_rect.centerx <= (player_bar_rect.left+(player_bar_rect.width/4)*3):
                    if bl_last_x < 0:
                        bl_last_x=-ball_spd
                    else:
                        bl_last_x=ball_spd
                bl_last_y=-ball_spd # and up
                
            
            # detect ball collision with blocks
            for line in range(2,max_lines):
                for col in range(0,max_cols):
                    if blocks[line][col] is not None:
                        if block_rects[line][col].colliderect(ball_rect):
                            pygame.mixer.Sound.play(rsrc['boing2'])

                            # ball hit bottom
                            if ball_rect.top >= block_rects[line][col].bottom+(ball_spd/2): 
                                bl_last_y=bl_last_y*-1 

                            # ball hit middle
                            elif ball_rect.top <  block_rects[line][col].bottom-(ball_spd) and \
                                 ball_rect.bottom >  block_rects[line][col].top-(ball_spd): 
                                # if ball hits block before center and is going to right, invert X 
                                if ball_rect.centerx <= block_rects[line][col].centerx and ball_spd >= 0:
                                    bl_last_x=bl_last_x*-1

                                # if ball hits block before center and is going to right, invert X 
                                if ball_rect.centerx >= block_rects[line][col].centerx and ball_spd <= 0:
                                    bl_last_x=bl_last_x*-1
                                # 
                                bl_last_y=bl_last_y*-1 # invert ball direction
                            
                            # ball hit top
                            else: 
                                bl_last_y=bl_last_y*-1 # invert ball direction
                            
                            blocks[line][col]=None # remove block
                            block_rects[line][col]=None
                            block_count-=1
                            score+=10
                            # player cleared level
                            if block_count==0:
                                blocks, block_rects, block_count = draw_blocks(rsrc, max_lines, max_cols)
                                ball_moving=False
                                ball_rect.centerx=player_bar_rect.centerx
                                ball_rect.centery=player_bar_rect.top-(ball_rect.height/2)
                                bl_last_x=ball_spd # initial movement to the right
                                bl_last_y=-ball_spd # and up 
                                ball_rect=ball_rect.move(bl_last_x, bl_last_y)

            # move ball
            ball_rect=ball_rect.move(bl_last_x, bl_last_y)

        ### Drawing
        # draw score bar
        scorebar=pygame.font.Font.render(rsrc['font1'],"Score: "+ str(score), True, "darkred", '#0a0a0a')
        scorebar_rect=scorebar.get_rect()
        scorebar_rect.top=0
        scorebar_rect.centerx=screen_rect.centerx
        screen.blit(scorebar, scorebar_rect)

        # draw lifes
        life_y=4
        for i in range(0,lifes):
            lifeS=pygame.Surface.copy(rsrc['ball'])
            life_rect=lifeS.get_rect()
            w=life_rect.width
            life_rect.centerx=screen_rect.width-(i*(w+10))-w
            life_rect.centery=life_y+20
            screen.blit(lifeS,life_rect)

        # blit blocks
        for line in range(2,max_lines):
            for col in range(0,max_cols):
                if blocks[line][col] is not None:
                    screen.blit(blocks[line][col], block_rects[line][col])
        
        # draw player and ball
        screen.blits(blit_sequence=((rsrc['player_bar'], player_bar_rect),(rsrc['ball'], ball_rect)))

        ## finish loop
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()