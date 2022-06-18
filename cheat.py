from math import atan

import pygame.math
import easygui as g
class Cheat:
    @staticmethod
    def set_hook_dir(hook, pos):
        # confirm hook is controllable and the pos is valid
        if not hook.out and pos[1] > hook.pos[1]:
            hook.th = atan((pos[0]-hook.pos[0])/(pos[1]-hook.pos[1]))
    @staticmethod
    def able_feature(game,feature_name,status):
        if status == 1:
            if feature_name == "hook_ray":
               game.hook.enable_ray = True
        if status == 0:
            if feature_name == "hook_ray":
               game.hook.enable_ray = False
    @staticmethod
    def set_val(game,target,new_val):
        pass
    @staticmethod
    def activate(game)->str:
        order = g.enterbox(msg='Enter something.', title=' ', default='', strip=True, image=None, root=None)
        orders = order.split(" ")
        print(orders)
        if orders[0] == "use":
            if orders[1] == "power":
                game.player.power*=2
                return
        if (idx:=(["disable","enable"].index(orders[0]))) in [0,1] :
            Cheat.able_feature(game,orders[1],idx)
        
        
        
