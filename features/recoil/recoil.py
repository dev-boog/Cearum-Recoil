from menu.menu import MenuApp as menu
from mouse.makcu import makcu_controller
from menu.settings_menu import SettingsMenu
from menu.recoil_menu import RecoilMenu
import time
import random

class recoil:     
    CS2_BASE_SENSITIVITY = 1.25 
    
    @staticmethod
    def jitter(value, max_offset):
        return value + random.uniform(-max_offset, max_offset)
    
    @staticmethod
    def sens_scalar(app: RecoilMenu, settings: SettingsMenu):
        scalar_mode = settings.get_game_scalar()

        if scalar_mode == "CS2":
            user_sensitivity = settings.get_cs2_sensitivity()
            return recoil.CS2_BASE_SENSITIVITY / user_sensitivity

        return app.get_recoil_scalar()
    
    @staticmethod
    def run_recoil(app: RecoilMenu, settings: SettingsMenu):
        shot_count = 0
        total_y_movement = 0  
        lmb_was_pressed = False
        last_toggle_state = False 
        last_cycle_state = False
        
        while True:
            toggle_key = RecoilMenu.get_toggle_keybind(app) 
            if toggle_key != "NONE":
                toggle_key_pressed = makcu_controller.get_button_state(toggle_key)
                if toggle_key_pressed and not last_toggle_state:
                    app.enable_checkbox.toggle()
                    time.sleep(0.5)
                last_toggle_state = toggle_key_pressed
            
            cycle_key = RecoilMenu.get_cycle_bind(app) 
            if cycle_key != "NONE":
                cycle_key_pressed = makcu_controller.get_button_state(cycle_key)
                if cycle_key_pressed and not last_cycle_state:
                    RecoilMenu.cycle_script(app)
                    time.sleep(0.5)
                last_cycle_state = cycle_key_pressed
                
            if not RecoilMenu.get_is_enabled(app):
                shot_count = 0
                total_y_movement = 0
                lmb_was_pressed = False
                time.sleep(0.05)
                continue
            
            recoil_pattern = app.vectors
            lmb_pressed = makcu_controller.get_button_state("LMB")
            
            if not lmb_pressed and lmb_was_pressed and total_y_movement != 0:
                if RecoilMenu.get_return_crosshair_enabled(app) == True:
                    makcu_controller.move_mouse_smoothly(0, -total_y_movement, 20, RecoilMenu.get_return_speed(app))
                total_y_movement = 0
                shot_count = 0
                lmb_was_pressed = False
                time.sleep(0.02)
                continue
            
            if not lmb_pressed:
                shot_count = 0
                total_y_movement = 0
                lmb_was_pressed = False
                time.sleep(0.02)
                continue
                
            if not lmb_was_pressed:
                shot_count = 0
                total_y_movement = 0
                lmb_was_pressed = True
            
            if recoil_pattern:
                if app.requires_right_button() and not makcu_controller.get_button_state("RMB"):
                    time.sleep(0.02)
                    continue
                    
                if shot_count >= len(recoil_pattern):
                    if app.get_is_recoil_looped():
                        shot_count = 0
                    else:
                        time.sleep(0.02)
                        continue
                        
                x, y, delay = recoil_pattern[shot_count] 
                
                if RecoilMenu.get_is_randomisation_enabled(app) == True:
                    x = recoil.jitter(x, RecoilMenu.get_randomisation_strength(app))
                    y = recoil.jitter(y, RecoilMenu.get_randomisation_strength(app))
                
                scalar = recoil.sens_scalar(app, settings)
                
                actual_x = x * RecoilMenu.get_x_control(app) * scalar
                actual_y = y * RecoilMenu.get_y_control(app) * scalar
                
                start_time = time.perf_counter()
                makcu_controller.move_mouse_smoothly(actual_x, actual_y)
                
                total_y_movement += actual_y
                
                elapsed = time.perf_counter() - start_time
                remaining_delay = delay - elapsed
                if remaining_delay > 0:
                    time.sleep(remaining_delay)
                    
                shot_count += 1
            else:
                time.sleep(0.02)