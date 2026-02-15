WIDTH= 1280
HEIGHT= 720
FPS= 30
TILESIZE= 64

#ui
BAR_HEIGHT=20
HEALTH_BAR_WIDTH=200
ITEM_BOX_SIZE=80
UI_FONT= '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

#general colors
WATER_COLOR= '#71ddee'
UI_BG_COLOR= '#222222'
UI_BORDER_COLOR= '#111111'
TEXT_COLOR= '#EEEEEE'

#ui colors
HEALTH_COLOR= 'red'
UI_BORDER_COLOR_ACTIVE= 'gold'

#weapons
weapon_data = {'sword' : {'cooldown':100, 'damage':15, 'graphic':'../graphics/weapons/sword/full.png'}}

#enemy
monster_data={
    'spirit':{'health':100, 'damage':8, 'attack_type': 'thunder', 'speed':4, 'resistance':3, 'attack_radius':60, 'notice_radius': 350}
}