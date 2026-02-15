import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout
from enemy import Enemy
from support import import_folder
from weapon import Weapon
from ui import UI

class Level:
    def __init__(self): 
        #get display surface
        self.display_surface=pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites=YSortCameraGroup()
        self.obstacle_sprites=pygame.sprite.Group()

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()


        #sprite setup
        self.create_map()

        #user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv'),
            'objects': import_csv_layout('../map/map_Object.csv'),
            'sign': import_csv_layout('../map/map_Sign.csv')
        }
        graphics = {
            'objects': import_folder('../graphics/objects')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x=col_index * TILESIZE
                        y=row_index* TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        
                        if style == 'entities':
                            if col== '394':
                                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destory_attack)
                            if col == '391':
                                monster_name = 'spirit'
                                Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites, self.damage_player)
                        if style == 'objects':
                            self.image = pygame.image.load('../graphics/objects/08.png').convert_alpha()
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'object',self.image)
                        if style == 'sign':
                            self.image = pygame.image.load('../graphics/objects/sign.png').convert_alpha()
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'sign',self.image)

    def create_attack(self):
        self.current_attack=Weapon(self.player, [self.visible_sprites,self.attack_sprites])

    def destory_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack= None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn particles

    def run(self):
        #draw and update the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.half_width=self.display_surface.get_size()[0]//2
        self.half_height=self.display_surface.get_size()[1]//2
        self.offset=pygame.math.Vector2()

        #creating the floor
        self.floor_surf= pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect= self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self,player):

        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos= self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        enemy_sprites= [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)


