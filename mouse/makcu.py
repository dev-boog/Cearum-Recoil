import time
import threading
from makcu import create_controller, MouseButton


class makcu_controller:
    controller = None
    _button_states = {"LMB": False, "RMB": False, "MMB": False, "M4": False, "M5": False}
    _connection_lock = threading.Lock()  # Add thread safety
    _is_connected = False

    RECOIL_SCALER = 1.0  

    @staticmethod
    def set_recoil_scaler(scaler: float):
        makcu_controller.RECOIL_SCALER = scaler

    @staticmethod
    def is_connected():
        """Check if controller is connected"""
        with makcu_controller._connection_lock:
            return makcu_controller._is_connected and makcu_controller.controller is not None

    @staticmethod
    def connect():
        with makcu_controller._connection_lock:
            if makcu_controller.controller is None:
                try:
                    makcu_controller.controller = create_controller(debug=False, auto_reconnect=True)
                    
                    def on_button_event(button: MouseButton, pressed: bool):
                        if button == MouseButton.LEFT:
                            makcu_controller._button_states["LMB"] = pressed
                        elif button == MouseButton.RIGHT:
                            makcu_controller._button_states["RMB"] = pressed
                        elif button == MouseButton.MIDDLE:
                            makcu_controller._button_states["MMB"] = pressed
                        elif button == MouseButton.MOUSE4:
                            makcu_controller._button_states["M4"] = pressed
                        elif button == MouseButton.MOUSE5:
                            makcu_controller._button_states["M5"] = pressed

                    makcu_controller.controller.set_button_callback(on_button_event)
                    makcu_controller.controller.enable_button_monitoring(True)
                    makcu_controller._is_connected = True

                except Exception as e:
                    print(f"Connection error: {e}")
                    makcu_controller._is_connected = False
                    return None

            return makcu_controller.controller

    @staticmethod
    def StartButtonListener():
        """Start button monitoring - kept for compatibility"""
        makcu_controller.connect()

    @staticmethod
    def click_button(button_name: str):
        if not makcu_controller.is_connected():
            return False
            
        mck = makcu_controller.controller
        if mck:
            try:
                if button_name == "LMB":
                    mck.click(MouseButton.LEFT)
                elif button_name == "RMB":
                    mck.click(MouseButton.RIGHT)
                elif button_name == "MMB":
                    mck.click(MouseButton.MIDDLE)
                elif button_name == "M4":
                    mck.click(MouseButton.MOUSE4)
                elif button_name == "M5":
                    mck.click(MouseButton.MOUSE5)
                return True
            except Exception as e:
                print(f"Click error: {e}")
                makcu_controller._is_connected = False
                return False
        return False

    @staticmethod
    def simple_move_mouse(x, y):
        if not makcu_controller.is_connected():
            return False
            
        mck = makcu_controller.controller
        if mck:
            try:
                scaled_x = int(x * makcu_controller.RECOIL_SCALER)
                scaled_y = int(y * makcu_controller.RECOIL_SCALER)
                mck.move(scaled_x, scaled_y)
                return True
            except Exception as e:
                print(f"Move error: {e}")
                makcu_controller._is_connected = False
                return False
        return False

    @staticmethod
    def move_mouse_smoothly(dx, dy, steps=20, duration=0.05):
        if not makcu_controller.is_connected():
            return False
            
        dx *= makcu_controller.RECOIL_SCALER
        dy *= makcu_controller.RECOIL_SCALER

        def ease_out_quad(t):
            return t * (2 - t)

        mck = makcu_controller.controller
        if not mck or (dx == 0 and dy == 0):
            return False

        try:
            accumulated_x, accumulated_y = 0.0, 0.0
            float_remainder_x, float_remainder_y = 0.0, 0.0
            step_delay = duration / steps

            for i in range(steps):
                t = (i + 1) / steps
                eased_t = ease_out_quad(t)

                target_step_x = dx * eased_t
                target_step_y = dy * eased_t

                move_this_step_x = target_step_x - accumulated_x
                move_this_step_y = target_step_y - accumulated_y

                accumulated_x += move_this_step_x
                accumulated_y += move_this_step_y

                move_x = int(accumulated_x + float_remainder_x)
                move_y = int(accumulated_y + float_remainder_y)

                float_remainder_x += accumulated_x - move_x
                float_remainder_y += accumulated_y - move_y

                if move_x != 0 or move_y != 0:
                    mck.move(move_x, move_y)

                time.sleep(step_delay)
            return True
        except Exception as e:
            print(f"Smooth move error: {e}")
            makcu_controller._is_connected = False
            return False

    @staticmethod
    def get_button_state(button):
        return makcu_controller._button_states.get(button, False)

    @staticmethod
    def disconnect():
        with makcu_controller._connection_lock:
            if makcu_controller.controller:
                try:
                    makcu_controller.controller.disconnect()
                except:
                    pass
                makcu_controller.controller = None
                makcu_controller._is_connected = False