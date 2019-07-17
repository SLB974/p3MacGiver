"""
Constants for "Helping MacGyver to Escape" game
"""

sprite_size = 40
sprite_number = 15
board_width = 200
surface_width = sprite_size * sprite_number + board_width
surface_height = sprite_number * sprite_size

structure_file = "ressources/maze.txt"
items_list = [
    ["Needle", 0, 0, "ressources/needle.png"],
    ["Ether", 0, 0, "ressources/ether.png"],
    ["Tub", 0, 0, "ressources/tub.png"],
]

window_title = "Helping MacGyver to Escape"
window_icon = "ressources/MacGyver.png"

macgyver_pic = "ressources/Macgyver.png"
guardian_pic = "ressources/guardian.png"
floor_pic = "ressources/floor.jpg"
wall_pic = "ressources/wall.png"
right_panel = "ressources/cadre_infos.jpg"

got_item_sound = "ressources/got_item.wav"
win_sound = "ressources/you_won.wav"
lost_sound = "ressources/you_lost.wav"

text1 = "YOU"
text2 = "WON"
text3 = "LOST"
