import os
import moviepy.video.io.ImageSequenceClip
image_folder='Results/Map_Frames/'
fps=8

# load the images
image_files = [os.path.join(image_folder,img)
               for img in os.listdir(image_folder)
               if img.endswith(".png")]

# sort based on frame number
image_files = sorted(image_files, key=lambda x: int(x.split('_')[2].split('.png')[0]))

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('Results/UCDP_time.mp4')