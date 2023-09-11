import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from threading import *
import os
import time
import decimal
from decimal import Decimal
import subprocess
import re
import importlib
from tkinter import Tk, Label
import io
from tkinter import font
import pkgutil
import pyautogui
import glob

padding = 30
dossier=os.getcwd()
file_cookie = ""
extensions = ['.part', '.ytdl']
for fichier in os.listdir(dossier):
    for extension in extensions:
        if fichier.endswith(extension):
            chemin_fichier = os.path.join(dossier, fichier)
            os.remove(chemin_fichier)
try:
    subprocess.run("pip install --upgrade yt-dlp")
    if pkgutil.find_loader("PIL") is not None:
        pass
    else:
        subprocess.run("pip install Pillow")
    if pkgutil.find_loader("win10toast") is not None:
        pass
    else:
        subprocess.run("pip install win10toast")
    if pkgutil.find_loader("requests") is not None:
        pass
    else:
        subprocess.run("pip install requests")
    if pkgutil.find_loader("langcodes") is not None:
        pass
    else:
        subprocess.run("pip install langcodes")
    subprocess.run("pip install language-data")
except FileNotFoundError:
    print("You need to put your Python to the path")
    time.sleep(3)
    exit()
from langcodes import Language
from PIL import Image, ImageTk

import requests
import yt_dlp
def change_size():
    req_width = app.winfo_reqwidth()
    req_height = app.winfo_reqheight()
    req_width += padding
    req_height += padding
    app.minsize(req_width, req_height)
def load_url():
    global video_name, audio_languages, radio_frames, checkbox_lists, checkbox_frames, checkbox, checkbox_vars, checkbox_vars, subtitle_languages, name_subtitles, l_name2, l_space, l_name, l_image, radio2_frame2, radio2_frame, radio_frame2, radio_frame, checkbox_frame2, checkbox_frame, radio_var, radio2_var, url, sub_fr_var, sub_en_var, sub_ar_var, sub_zh_var, sub_de_var, sub_hi_var, sub_it_var, sub_ja_var, sub_ko_var, sub_pl_var, sub_pt_var, sub_ru_var, sub_es_var, sub_tr_var, sub_uk_var    
    p1['value'] = 0
    l6.config(text="")
    b5.config(state="disabled")
    b1.config(state="disabled")
    try:
        lerror.pack_forget()
    except:
        pass
    url = e1.get()
    try:
        if file_cookie != "":
            ydl_opts = {
                'noplaylist': True,
                'playlistend': 0,
                'listformats': True,
                'listformats': True,
                'writethumbnail': True,
                'quiet': True,
                'listsubtitles': True,
                'cookiefile': file_cookie,
                'noprogress': True,
                }
        else:
            ydl_opts = {
                'noplaylist': True,
                'playlistend': 0,
                'listformats': True,
                'writethumbnail': True,
                'listformats': True,
                'quiet': True,
                'listsubtitles': True,
                'noprogress': True,
                }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        ydl_opts=""
        site = info.get('extractor', '')
        custom_font = font.Font(weight="bold", size=16)
        l_name2 = ttk.Label(app, text=f'[ {site.upper()} ]', font=custom_font)
        l_name2.pack()
        custom_font = font.Font(weight="bold", size=16)
        video_name = info.get('title')
        l_name = ttk.Label(app, text=video_name, font=custom_font)
        l_name.pack()
        
        episode_thumbnail = info.get('thumbnail')
        try:
            response = requests.get(episode_thumbnail)
            image = Image.open(io.BytesIO(response.content))
            width, height = image.size
            max_width=600
            max_height=600
            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(image=image)
            l_image = ttk.Label(app, image=photo_image)
            l_image.image = photo_image
            l_image.pack()
        except:
            pass
        formats = info.get('formats', [])
        pattern = r'[\\/:\*\?"<>\|\x00-\x1f\x7f\(\)\'\\]'
        video_name = re.sub(pattern, '', video_name)
        video_name=video_name.replace(" ","_")
        video_name=video_name.replace(":","_").replace("|","_").replace("[","").replace("]","").replace("ō","")
        qualities = []
        audio_languages = []
        subtitle_languages = []
        for fmt in formats:
            ext = fmt.get('ext')
            resolution = fmt.get('resolution')
            format_id = fmt.get('format_id')            
            if ext and resolution and format_id:
                quality = f"{format_id} {ext} {resolution}"
                qualities.append(quality)        
        already_audio=[]
        audio_language_names=[]
        if 'formats' in info:
            for fmt in info['formats']:
                if 'language' in fmt and not fmt['language'] in already_audio:
                    audio_languages.append(fmt['language'])
                    already_audio.append(fmt['language'])
        audio_languages = [x for x in audio_languages if x is not None]
        audio_languages=list(set(audio_languages))
        counter=0
        for i in audio_languages:
            langue = Language.get(i)
            langue = langue.display_name()
            if langue[0:16] != "Unknown language":
                audio_language_names.append(langue)
            else:
                 del audio_languages[counter]
            counter+=1
        name_subtitles=[]
        if 'subtitles' in info:
            for lang in info['subtitles']:
                if lang != "live_chat":
                    subtitle_languages.append(lang)
            for i in subtitle_languages :
                try:
                    name_subtitles.append(info['subtitles'][i][0]['name'])
                except:
                    name_subtitles.append("")
        counter=0            
        for i in subtitle_languages:
            if name_subtitles[counter]=="":
                langue = Language.get(i)
                langue=str(langue.display_name())
                if langue[0:16] != "Unknown language":
                    name_subtitles[counter]=(langue)
                else:
                    del subtitle_languages[counter]
            counter+=1
        l9.pack_forget()
        e1.pack_forget()
        b1.pack_forget()
        b5.pack_forget()
        sub_lang=[]
        checkbox_frames=[]
        checkbox_vars=[]
        checkbox_lists=[]
        if len(subtitle_languages) > 0:
            l2.pack()
            for i in range(len(subtitle_languages)):
                if i % 5 == 0:
                    checkbox_frame = ttk.Frame(app)
                    checkbox_frame.pack()
                    checkbox_frames.append(checkbox_frame)
                checkbox_var = tk.BooleanVar(value=False)
                checkbox_vars.append(checkbox_var)
                checkbox_var.set(0)
                checkbox = ttk.Checkbutton(checkbox_frame, text=name_subtitles[i], variable=checkbox_var)
                checkbox_lists.append(checkbox)
                checkbox.pack(side=tk.LEFT)
        radio_frames=[]
        radio_vars=[]
        radio_list=[]
        radio_var = tk.StringVar(value="")
        if len(audio_languages) > 1:
            l2_2.pack()
            for i in range(len(audio_languages)):
                if i % 5 == 0:
                    radio_frame = ttk.Frame(app)
                    radio_frame.pack()
                    radio_frames.append(radio_frame)
                radio = ttk.Radiobutton(radio_frame, text=audio_language_names[i],value=audio_languages[i], variable=radio_var)
                radio_list.append(radio)
                radio.pack(side=tk.LEFT)
        l4.pack()
        highest_resolution = 0
        resolutions_max = {}
        resolutions = []
        resolutions_max = {}
        for element in qualities:
            match = re.search(r'([^ ]+)\s+(?:mp4|webm)\s+(\d+x\d+)', element)
            if match:
                number = match.group(1)
                resolution = match.group(2)
                width, height = resolution.split('x')
                width = int(width)
                height = int(height)
                if width not in resolutions_max or height > resolutions_max[width]['height']:
                    resolutions_max[width] = {'height': height, 'number': number}
        tableau_final = [f'{resolutions_max[width]["number"]} mp4 {width}x{resolutions_max[width]["height"]} ({resolutions_max[width]["height"]})' for width in sorted(resolutions_max.keys())]
        resolutions = []
        for element in tableau_final:
            match = re.search(r'(\d+x\d+)', element)
            if match:
                resolution = match.group(1)
                resolutions.append(resolution)
        qualities_text=resolutions
        resolutions = []
        for element in tableau_final:
            elements = element.split()
            match = re.search(r'\d+', element)
            if match:
                number = match.group()
                resolutions.append(number)
        qualities = resolutions        
        radio2_frame = ttk.Frame(app)
        radio2_frame.pack()
        radio2_var = tk.StringVar()
        if len(qualities) > 5:
            radio2_frame2 = ttk.Frame(app)
            radio2_frame2.pack()
        counter=0
        for resolution in qualities:
            resolution_text=qualities_text[counter]
            if counter < 6:
                radio_qualities = ttk.Radiobutton(radio2_frame, text=resolution_text, value=resolution_text, variable=radio2_var)
            else:
                radio_qualities = ttk.Radiobutton(radio2_frame2, text=resolution_text, value=resolution_text, variable=radio2_var)
            radio_qualities.pack(side="left", anchor="w")
            counter+=1
        b3.pack()
        b4.pack()
        b3.config(state="normal")
        b4.config(state="normal")
        p1.pack()
        l5.pack()
        l6.pack()
        l_space= ttk.Label(app, text="                     ")
        change_size()
    except yt_dlp.utils.DownloadError as e:
        e=str(e)[18:len(str(e))]
        line_length = 80
        lines = []
        current_line = ""
        for word in e.split():
            if len(current_line) + len(word) <= line_length:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        e="\n".join(lines)
        lerror.config(text=e, font=errfont)
        lerror.pack()
        app.update()
        b1.config(state="normal")
        b5.config(state="normal")
    except FileNotFoundError or UnicodeDecodeError as e:
        lerror.config(text=": Invalide Cokkies File :")
        lerror.pack()
        app.update()
        b1.config(state="normal")
        b5.config(state="normal")
    except Exception as e:
        lerror.config(text=e)
        lerror.pack()
        app.update()
        b1.config(state="normal")
        b5.config(state="normal")
def download_video():
    try:
        p1['value'] = 0
        l6.config(text="Starting download")
        b3.config(state="disabled")
        b4.config(state="disabled")
        url = e1.get()
        resolution = radio2_var.get()
        width, height = resolution.split("x")
        width=int(width)
        height=int(height)
        subs_lang=[]
        lang_verify=1
        if len(audio_languages) > 1:
            lang=radio_var.get()
            if lang=="":
                lang_verify=0
        else:
            lang_verify=0
        subs_lang = []
        for i in range(len(subtitle_languages)):
            checkbox_var = checkbox_vars[i].get()

            if checkbox_var:
                subs_lang.append(subtitle_languages[i]) 
        if len(subs_lang) != 0:
            subs_lang_verify= True
        else:
            subs_lang_verify = False
        if lang_verify == 1:
            formats=f"bestvideo[ext=mp4][width={width}][height={height}]+bestaudio[ext=m4a][language={lang}]/best[ext=mp4][width={width}][height={height}]"
        else:
            formats=f"bestvideo[ext=mp4][width={width}][height={height}]+bestaudio[ext=m4a]/best[ext=mp4][width={width}][height={height}]"
        
        video_name2=video_name+".tempmp4"
        subs_lang.append("-live_chat")
        if file_cookie != "":
            ydl_opts = {
                "embedsubs": True,
                'noplaylist': True,
                'cachedir': r'C:\Users\Célestin\Desktop\traduction\test\trad\cache',
                'postprocessors': [{
                        'key': 'FFmpegEmbedSubtitle',
                        'already_have_subtitle': False,
                }],
                'writesubtitles' : True,
                'verbose': True,
                'outtmpl' : f'\{video_name}\{video_name}.mp4',
                'subtitleslangs': subs_lang,
                'format': formats,
                'progress_hooks': [progress_hook],
                'playlistend': 1,
                'cookiefile': file_cookie,
                'no_color': True,
                'quiet': True,
                'noprogress': True,
                }
        else:
            ydl_opts = {
                'noplaylist': True,
                'cachedir': r'C:\Users\Célestin\Desktop\traduction\test\trad\cache',
                'postprocessors': [{
                        'key': 'FFmpegEmbedSubtitle',
                        'already_have_subtitle': False,
                }],
                'writesubtitles' : True,
                'outtmpl' : f'{video_name}\{video_name}.mp4',
                'subtitleslangs': subs_lang,
                'format': formats,
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_color': True,
                'playlistend': 1,
                'noprogress': True,
                }
    except:
        b3.config(state="normal")
        b4.config(state="normal")
        l6.config(text="")
    try: 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        ydl_opts=""
        """
	try:
            if len(subs_lang) > 1:
                subprocess.call(f'python subs_merge.py {video_name}')
                for f in glob.glob(f"{video_name}\*.ass") + glob.glob(f"{video_name}\*.vtt") + glob.glob(f"{video_name}\*.mp4"):
                    os.remove(f)
                video_name3=video_name.replace("_"," ")
                d=video_name.replace(" ","_")
                d2=d.replace("_"," ")
                filename=(video_name)
                filename_2=video_name.replace("_"," ")
                os.rename(f'{d}',f'{d2}')
                os.rename(fr'{d2}\{filename}.mkv',fr'{d2}\{filename_2}.mkv')
        except:
            pass
	"""
        b3.config(state="normal")
        b4.config(state="normal")
        l6.config(text="Downloading finished !")
    except Exception as e:
        b3.config(state="normal")
        b4.config(state="normal")
        l6.config(text="An ERROR occured")
def threading():
    t1=Thread(target=download_video)
    t1.start()
def threading2():
    t2=Thread(target=load_url)
    t2.start()
def progress_hook(progress_data):
    if progress_data['status'] == 'downloading':
        percentage = progress_data['_percent_str']
        eta = progress_data['_eta_str']
        p1['value'] = float(percentage.replace('%',""))
        l6.config(text=f"Downloading : {percentage} (ETA : {eta})")
    elif progress_data['status'] == 'finished':
        p1['value'] = 100
        l6.config(text='Finishing video...')
def disable_event():
    try:
        os.remove(file_path[0:len(file_path)-4]+'_temp.jpg')
    except:
        pass
    extensions = ['.part', '.ytdl']
    try:
        for fichier in os.listdir(dossier):
            for extension in extensions:
                if fichier.endswith(extension):
                    chemin_fichier = os.path.join(dossier, fichier)
                    os.remove(chemin_fichier)
    except:
        pass
    app.destroy()
    os._exit(0)
def cookie():
    global file_cookie
    file_cookie = filedialog.askopenfilename()
def threading3():
    t3=Thread(target=cookie)
    t3.start()
def back():
    for i in checkbox_frames:
        i.pack_forget()
    for i in radio_frames:
        i.pack_forget()
    try:
        radio_frame.pack_forget()
    except:
        pass
    try:
        radio_frame2.pack_forget()
    except:
        pass
    try:
        radio2_frame.pack_forget()
    except:
        pass
    try:
        radio2_frame2.pack_forget()
    except:
        pass
    try:
        l_image.pack_forget()
    except:
        pass
    try:
        l_name.pack_forget()
    except:
        pass
    try:
        l_name2.pack_forget()
    except:
        pass
    b1.config(state="normal")
    b5.config(state="normal")
    b3.pack_forget()
    p1.pack_forget()
    l5.pack_forget()
    l6.pack_forget()
    l2.pack_forget()
    l2_2.pack_forget()
    l_space.pack_forget()
    l4.pack_forget()
    b5.pack()
    l9.pack()
    e1.pack()
    b1.pack()
    b4.pack_forget()
    min_width = 580
    min_height = 150
    app.minsize(min_width, min_height)
app = Tk()
app.title("Yt-DlpGuiDownloader")
min_width = 580
min_height = 150
app.minsize(min_width, min_height)
app.wm_attributes("-topmost", True)
app.resizable(False, False)
app.protocol("WM_DELETE_WINDOW", disable_event)
errfont = font.Font(weight="bold")
l1= ttk.Label(app, anchor='center', text = '" Free Video Downloader " ')
l1.pack(pady=10)
b5 = ttk.Button(app, text="Open Cookie File", command=threading3, state="normal")
b5.pack()
l9 = ttk.Label(app, anchor='center', text = ' Set the url : ')
l9.pack()
e1 = ttk.Entry(app, width=50,justify='center')
e1.pack()
b1 = ttk.Button(app, text="Load video", command=threading2, state="normal")
b1.pack()  
l2= ttk.Label(app, anchor='center', text = " Subtitles : ", font = errfont)
l2_2 = ttk.Label(app, anchor='center', text = " Language : ", font =errfont)
l4= ttk.Label(app, anchor='center', text='Resolutions :', font = errfont)
b3 = ttk.Button(app, text="Download", command=threading)
b4 = ttk.Button(app, text="Back", command=back)
p1 = ttk.Progressbar(app, orient='horizontal', length=500, mode='determinate')
l5= ttk.Label(app, anchor='center', text='')
l6= ttk.Label(app, anchor='center', text = '')
lerror= ttk.Label(app, anchor='center', text='')
lerror.pack()
app.mainloop()
exit()
"""
'postprocessors': [{
    'key': 'FFmpegEmbedSubtitle'
    'already_have_subtitle': False,
}],
"""
