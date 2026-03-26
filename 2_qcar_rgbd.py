import cv2
from pal.products.qcar import QCarRealSense, IS_PHYSICAL_QCAR

myCam = QCarRealSense(mode='RGB, Depth')

try:
    while True:
        
        myCam.read_RGB() # Read RGB
        cv2.imshow('My RGB', myCam.imageBufferRGB)

        myCam.read_depth() # Read depth
        depth_img = myCam.imageBufferDepthPX
        cv2.imshow('My Depth', depth_img)
        shape_depth = depth_img.shape

        # Needed for OpenCV window updates
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nProgram stopped by user (pressed Q).")
            break

except KeyboardInterrupt:
    print("\nProgram stopped by user (CTRL+C).")

print(shape_depth)

cv2.destroyAllWindows()
