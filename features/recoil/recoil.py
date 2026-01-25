from menu.menu import MenuApp as menu
from mouse.makcu import makcu_controller
from menu.recoil_menu import RecoilMenu
import time

class recoil:
    @staticmethod
    def run_recoil(app: RecoilMenu):
        shot_count = 0
        lmb_was_pressed = False

        while True:
            try:
                toggle_key = app.get_toggle_keybind()
                toggle_key_pressed = makcu_controller.get_button_state(toggle_key)

                if toggle_key_pressed:
                    app.enable_checkbox.toggle()
                    time.sleep(0.3)


                if not app.get_is_enabled():
                    shot_count = 0
                    lmb_was_pressed = False
                    time.sleep(0.05)
                    continue

                vectors = app.get_mouse_vectors()
                lmb_pressed = makcu_controller.get_button_state("LMB")

                if not lmb_pressed:
                    shot_count = 0
                    lmb_was_pressed = False
                    time.sleep(0.01)
                    continue

                if not lmb_was_pressed:
                    shot_count = 0
                    lmb_was_pressed = True

                if vectors:
                    if app.requires_right_button() and not makcu_controller.get_button_state("RMB"):
                        time.sleep(0.01)
                        continue

                    if shot_count >= len(vectors):
                        if app.get_is_recoil_looped():
                            shot_count = 0
                        else:
                            time.sleep(0.01)
                            continue

                    x, y, delay = vectors[shot_count]

                    start_time = time.perf_counter()
                    makcu_controller.move_mouse_smoothly(
                        x * app.get_x_control(),
                        y * app.get_y_control()
                    )

                    elapsed = time.perf_counter() - start_time
                    if delay > elapsed:
                        time.sleep(delay - elapsed)

                    shot_count += 1
                else:
                    time.sleep(0.01)

            except Exception as e:
                print(f"Recoil thread error: {e}")
                time.sleep(0.1)
