from PIL import Image
import shutil,cv2,os
from moviepy.editor import *



def frame_extract(video):
    '''
    Function to extract the frames of the video and then store it in a temporary temp_folder
    '''
    temp_folder = 'temp'
    try:
        os.mkdir(temp_folder)
    except OSError:
        remove(temp_folder)
        os.mkdir(temp_folder)

    vidcap = cv2.VideoCapture(str(video)) #creating the videocapture object
    count = 0

    while True:
        success, image = vidcap.read() #returns T/F whether frame is read correctly or not
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)#cv2.imwrite saves the image to temp_folder
        count += 1


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))



def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))






def encode_frame(frame_dir,text_to_hide):



    # open the text file

    text_to_hide_open = open(text_to_hide, "r")
    text_to_hide = repr(text_to_hide_open.read())

    # split text to max 255 char each

    text_to_hide_chopped =  split2len(text_to_hide,255) #returns a list of strings after breaking the given string by the specified separator.

    for text in text_to_hide_chopped:
        length = len(text)#
        chopped_text_index = text_to_hide_chopped.index(text)#gettinthe list index
        frame = Image.open(str(frame_dir) +"/" + str(chopped_text_index+1) + ".png")#opeaning the image  which is in the temp temp_folder

        if frame.mode != "RGB":
            print("Source frame must be in RGB format")
            return False

        # use copy of the file

        encoded = frame.copy()
        width, height = frame.size

        index = 0
        a = object
        for row in range(height):
            for col in range(width):
                r,g,b = frame.getpixel((col,row))

                # first value is length of the message per frame
                if row == 0 and col == 0 and index < length:
                    asc = length
                    if text_to_hide_chopped.index(text) == 0 :
                        total_encoded_frame = len(text_to_hide_chopped)
                    else:
                        total_encoded_frame = g
                elif index <= length:
                    asc = ord(text[index -1])#test is saved in the red component RGB of the frame
                    total_encoded_frame = g
                else:
                    asc = r
                    total_encoded_frame = g
                    '''asc represent the length of msg per frame
                    total encoded frame count the no of frame total_encoded_frame
                    '''
                encoded.putpixel((col,row),(asc,total_encoded_frame,b))
                index += 1
        if encoded:
            encoded.save(str(frame_dir)+"/"+str(chopped_text_index+1) + ".png",compress_level=0)

def merge_audio_to_video(video_file, audio_file, output_file):
    # Load the video and audio files
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)

    # Combine the audio from the video and the audio file
    # final_audio = CompositeAudioClip([video_clip.audio, audio_clip])

    # Set the audio of the video to the combined audio
    video_clip = video_clip.set_audio(audio_clip)

    # Write the final video with merged audio to a file
    video_clip.write_videofile(output_file, codec='libx264')

    # Close the video and audio clips
    video_clip.close()
    audio_clip.close()

def cpFile(source_file, destination_folder):
    try:
        shutil.copy(source_file, destination_folder)
        
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def extract_audio_from_video(video_file, output_audio_file):
    # Load the video file
    video = VideoFileClip(video_file)

    # Extract the audio from the video
    audio = video.audio

    # Save the audio to a new file
    audio.write_audiofile(output_audio_file)

    # Close the video and audio clips
    video.close()
    audio.close()

def merge_frames_to_video(frame_folder, output_video_file, fps=25):
    # Get a list of all image files in the frame folder
    frame_files = sorted([os.path.join(frame_folder, file) for file in os.listdir(frame_folder) if file.endswith('.jpg') or file.endswith('.png')])

    # Load the images and create the video clip
    video_clip = ImageSequenceClip(frame_files, fps=fps)

    # Write the video clip to a file
    video_clip.write_videofile(output_video_file, codec='png')  # You can change the codec to 'libx264' for an mp4 file or 'prores' for a .mov file

def read_txt(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def write_txt(content, output_filename):
    try:
        with open(output_filename, 'w') as file:
            file.write(content)
        print(f"Content written to '{output_filename}' successfully.")
    except Exception as e:
        print(f"Error: {e}")

def decode_frame(frame_dir,outputfile):

    #take the first frame to get width, height, and total encoded frame

    # first_frame = Image.open(str(frame_dir) + "/0.jpg")
    first_frame = Image.open(str(frame_dir)+ "/" + "0.png")#opening the image from the temp_folder
    r,g,b = first_frame.getpixel((0,0))#returns the r g b value @ (0,0) pixel
    total_encoded_frame = g
    msg = ""
    for i in range (1,total_encoded_frame+1):
        frame = Image.open(str(frame_dir) + "/" + str(i) + ".png")##opening the image from the temp_folder
        width, height = frame.size      #getting the dimensions of the image
        index = 0
        for row in range(height):
            for col in range(width):
                try :
                    r,g,b = frame.getpixel((col,row))
                except ValueError:

                    r, g, b, a = frame.getpixel((col, row))
                if row == 0 and col == 0:
                    length = r
                elif index <= length:
                    # put the decoded character into string
                    msg += chr(r)
                index +=1
    #remove the first and the last quote

    
    msg = msg[1:-1]
    recovered_txt = open("temp/"+outputfile+".txt", "wb")
    recovered_txt.write(str(msg).encode("utf-8"))
