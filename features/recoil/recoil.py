from menu.menu import MenuApp as menu
from mouse.makcu import makcu_controller
from menu.recoil_menu import RecoilMenu
import time

class recoil:
    @staticmethod
    def run_recoil(app: RecoilMenu):
        shot_count = 0
        lmb_was_pressed = False
        last_toggle_state = False  # Track toggle state to prevent rapid toggling
        
        while True:
            try:
                # Check connection first - if not connected, wait longer
                if not makcu_controller.is_connected():
                    print("Recoil thread: Not connected")
                    shot_count = 0
                    lmb_was_pressed = False
                    time.sleep(0.5)  # Wait longer when disconnected
                    continue
                
                # Handle toggle keybind with debouncing
                toggle_key = app.get_toggle_keybind()
                if toggle_key != "NONE":
                    toggle_key_pressed = makcu_controller.get_button_state(toggle_key)
                    if toggle_key_pressed and not last_toggle_state:
                        app.enable_checkbox.toggle()
                        time.sleep(0.3)  # Debounce delay
                    last_toggle_state = toggle_key_pressed
                
                # If not enabled, reset and wait
                if not app.get_is_enabled():
                    shot_count = 0
                    lmb_was_pressed = False
                    time.sleep(0.05)
                    continue
                
                # Get vectors once per loop iteration
                vectors = app.vectors  # Use cached vectors from RecoilMenu
                
                # Check LMB state
                lmb_pressed = makcu_controller.get_button_state("LMB")
                
                if not lmb_pressed:
                    shot_count = 0
                    lmb_was_pressed = False
                    time.sleep(0.02)  # Slightly longer sleep when not firing
                    continue
                
                # Reset shot count on new press
                if not lmb_was_pressed:
                    shot_count = 0
                    lmb_was_pressed = True
                
                # Process recoil compensation if vectors exist
                if vectors:
                    # Check if right button is required
                    if app.requires_right_button() and not makcu_controller.get_button_state("RMB"):
                        time.sleep(0.02)
                        continue
                    
                    # Handle shot count and looping
                    if shot_count >= len(vectors):
                        if app.get_is_recoil_looped():
                            shot_count = 0
                        else:
                            time.sleep(0.02)
                            continue
                    
                    # Get vector data
                    x, y, delay = vectors[shot_count]
                    
                    # Apply recoil compensation
                    start_time = time.perf_counter()
                    
                    success = makcu_controller.move_mouse_smoothly(
                        x * app.get_x_control(),
                        y * app.get_y_control()
                    )
                    
                    if not success:
                        print("Recoil thread: Move failed, connection may be lost")
                        time.sleep(0.1)
                        continue
                    
                    # Calculate remaining delay
                    elapsed = time.perf_counter() - start_time
                    remaining_delay = delay - elapsed
                    
                    if remaining_delay > 0:
                        time.sleep(remaining_delay)
                    
                    shot_count += 1
                else:
                    # No vectors loaded
                    time.sleep(0.02)
                    
            except Exception as e:
                print(f"Recoil thread error: {e}")
                import traceback
                traceback.print_exc()  # Print full error for debugging
                shot_count = 0
                lmb_was_pressed = False
                time.sleep(0.5)  # Longer sleep on error