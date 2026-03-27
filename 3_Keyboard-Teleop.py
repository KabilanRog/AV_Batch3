from pal.products.qcar import QCar
from pynput import keyboard
 
# --- Control state ---
throttle = 0.0
steering = 0.0
 
THROTTLE_STEP = 0.3   # Increment per keypress (-2.0 to 2.0 range)
STEERING_STEP = 0.2   # Increment per keypress (-0.5 to 0.5 range)
 
THROTTLE_MAX =  2.0
THROTTLE_MIN = -2.0
STEERING_MAX =  0.5
STEERING_MIN = -0.5
 
def on_press(key):
    global throttle, steering
    try:
        if key == keyboard.Key.up:
            throttle = min(throttle + THROTTLE_STEP, THROTTLE_MAX)
        elif key == keyboard.Key.down:
            throttle = max(throttle - THROTTLE_STEP, THROTTLE_MIN)
        elif key == keyboard.Key.right:
            steering = min(steering + STEERING_STEP, STEERING_MAX)
        elif key == keyboard.Key.left:
            steering = max(steering - STEERING_STEP, STEERING_MIN)
        elif key == keyboard.Key.space:
            # Emergency stop
            throttle = 0.0
            steering = 0.0
            print("\n[SPACE] Emergency stop triggered.")
    except AttributeError:
        pass  # Ignore non-special keys
 
def on_release(key):
    global throttle, steering
    # Gradually reset to neutral on key release
    if key in (keyboard.Key.up, keyboard.Key.down):
        throttle = 0.0
    elif key in (keyboard.Key.left, keyboard.Key.right):
        steering = 0.0
 
# --- Start keyboard listener (non-blocking, runs in background thread) ---
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
 
myCar = QCar(readMode=1, frequency=10)
 
print("Arrow Key Control Active:")
print("  ↑ / ↓  : Throttle forward / backward")
print("  ← / →  : Steer left / right")
print("  SPACE  : Emergency stop")
print("  CTRL+C : Quit\n")
 
try:
    while True:
        myCar.write(throttle, steering)
        myCar.read()
 
        print(
            f"Throttle: {throttle:+.2f} | Steering: {steering:+.2f} | "
            f"Battery: {myCar.batteryVoltage:.2f} V | "
            f"Motor Current: {myCar.motorCurrent:.2f} A | "
            f"Tach: {myCar.motorTach:.2f}",
            end="\r"  # Overwrite the same line for clean output
        )
 
except KeyboardInterrupt:
    print("\n\nProgram stopped by user (CTRL+C).")
 
finally:
    listener.stop()
    myCar.write(0.0, 0.0)
    print("Motors stopped. Safe to disconnect.")
