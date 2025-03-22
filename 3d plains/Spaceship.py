from pyray import *

init_window(1280, 720, "Space")
cam = Camera3D([18, 16, 18], [0, 0, 0], [0, 1, 0], 60, 0) #Camera position, Camera direction, Camera's up direction, FOV, Type of camera (0 default)

x = 0
y = 0
z = 0

while not window_should_close():
    update_camera(cam, CAMERA_FREE)
    if is_key_pressed(KEY_P):
        disable_cursor()
    elif is_key_pressed(KEY_O):
        enable_cursor()
        
    begin_drawing()
    clear_background(BLACK)
    begin_mode_3d(cam)
    draw_grid(1500, 1) #slices, spacing
    
    if is_key_pressed(KEY_T):
        z += 5
    elif is_key_pressed(KEY_G):
        z -= 5
    elif is_key_pressed(KEY_F):
        x -= 5
    elif is_key_pressed(KEY_H):
        x += 5    
        
    if is_key_pressed(KEY_ENTER):
        draw_cube_v([x, y, z], [10, 10, 10], (255, 0, 0, 255))
        draw_cube_v([x, y, z], [10, 10, 10], (255, 0, 0, 255))

    end_mode_3d()
    end_drawing()
