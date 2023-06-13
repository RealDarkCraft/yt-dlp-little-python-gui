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
from langcodes import Language
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
        
    if pkgutil.find_loader("requests") is not None:
        pass
    else:
        subprocess.run("pip install requests")
except FileNotFoundError:
    time.sleep(3)
    print("You need to put your Python to the path")
    exit()
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
    global video_name, radio_frames, checkbox_lists, checkbox_frames, checkbox, checkbox_vars, checkbox_vars, subtitle_languages, name_subtitles, l_name2, l_space, l_name, l_image, radio2_frame2, radio2_frame, radio_frame2, radio_frame, checkbox_frame2, checkbox_frame, radio_var, radio2_var, url, sub_fr_var, sub_en_var, sub_ar_var, sub_zh_var, sub_de_var, sub_hi_var, sub_it_var, sub_ja_var, sub_ko_var, sub_pl_var, sub_pt_var, sub_ru_var, sub_es_var, sub_tr_var, sub_uk_var    
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
        video_name = video_name.replace("(","").replace(")","").replace("-","").replace(" ","_").replace("–","")
        episode_thumbnail = info.get('thumbnail')
        response = requests.get(episode_thumbnail)
        image = Image.open(io.BytesIO(response.content))
        width, height = image.size
        max_width=600
        max_height=600
        if width > max_width or height > max_height:
            # Calculer les nouvelles dimensions proportionnelles
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            # Redimensionner l'image
            image = image.resize((new_width, new_height), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(image=image)
        l_image = ttk.Label(app, image=photo_image)
        l_image.image = photo_image
        l_image.pack()
        formats = info.get('formats', [])
        qualities = []
        audio_languages = []
        subtitle_languages = []
        for fmt in formats:
            ext = fmt.get('ext')
            resolution = fmt.get('resolution')
            format_id = fmt.get('format_id')
            #acodec = fmt.get('protocol')  # Récupération du codec audio
            
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
        print(audio_languages)
        for i in audio_languages:
            langue = Language.get(i)
            audio_language_names.append(str(langue.display_name()))
            counter+=1
        print(audio_language_names)
        
        """
        if 'formats' in info:
            for fmt in info['formats']:
                if 'language' in fmt:
                    audio_languages.append(fmt['language'])
        """
        
        name_subtitles=[]
        bool_1=False
        if 'subtitles' in info:
            for lang in info['subtitles']:
                if lang != "live_chat":
                    subtitle_languages.append(lang)
            for i in subtitle_languages :
                try:
                    name_subtitles.append(info['subtitles'][i][0]['name'])
                except:
                    name_subtitles.append("")
        print(name_subtitles)
        counter=0            
        for i in subtitle_languages:
            if name_subtitles[counter]=="":
                langue = Language.get(i)
                name_subtitles[counter]=(str(langue.display_name()))
            counter+=1
        #print(name_subtitles)
                    
        #print(name_subtitles)
        #lerror.pack_forget()
        #
        l9.pack_forget()
        e1.pack_forget()
        b1.pack_forget()
        b5.pack_forget()
        
        counter=0
        max_counter=3
        
        
        if len(subtitle_languages) > 0:
            l2.pack()
        sub_lang=[]
        
        checkbox_frames=[]
        checkbox_vars=[]
        checkbox_lists=[]
        if len(subtitle_languages) > 0:
            for i in range(len(subtitle_languages)):
                if i % 5 == 0:
                    # Créer une nouvelle frame pour chaque groupe de 8 checkbox
                    checkbox_frame = ttk.Frame(app)
                    checkbox_frame.pack()
                    checkbox_frames.append(checkbox_frame)
                checkbox_var = tk.BooleanVar(value=False)
                checkbox_vars.append(checkbox_var)
                checkbox_var.set(0)
                checkbox = ttk.Checkbutton(checkbox_frame, text=name_subtitles[i], variable=checkbox_var)
                checkbox_lists.append(checkbox)
                checkbox.pack(side=tk.LEFT)
        print(subtitle_languages)
        
        
        radio_frames=[]
        radio_vars=[]
        radio_list=[]
        radio_var = tk.StringVar(value="")
        if len(audio_languages) > 0:
            l2_2.pack()
            for i in range(len(audio_languages)):
                if i % 5 == 0:
                    # Créer une nouvelle frame pour chaque groupe de 8 checkbox
                    radio_frame = ttk.Frame(app)
                    radio_frame.pack()
                    radio_frames.append(radio_frame)
                #radio_var = tk.BooleanVar(value=False)
                #checkbox_vars.append(checkbox_var)
                #checkbox_var.set(0)
                radio = ttk.Radiobutton(radio_frame, text=audio_language_names[i],value=audio_languages[i], variable=radio_var)
                radio_list.append(radio)
                radio.pack(side=tk.LEFT)
        
        
        
        
        
        
        """
        radio_frame = ttk.Frame(app)
        
        
        audio_languages = [x for x in audio_languages if x is not None]
        if len(audio_languages) > 1:
            l2_2.pack()
            radio_frame.pack()
        if len(audio_languages) > 8:
            radio_frame2 = ttk.Frame(app)
            radio_frame2.pack()
        radio_lang=[]
        counter=0
        radio_var = tk.StringVar()
        if len(audio_languages) > 1:
            for i in audio_languages:
                if (i[0:2] == "fr") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_fr = ttk.Radiobutton(radio_frame, text="French",value="fr", variable=radio_var)
                    else:
                        radio_fr = ttk.Radiobutton(radio_frame2, text="French",value="fr", variable=radio_var)
                    radio_fr.pack(side="left", anchor="w")
                elif (i[0:2] == "en") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_en = ttk.Radiobutton(radio_frame, text="English",value="en", variable=radio_var)
                    else:
                        radio_en = ttk.Radiobutton(radio_frame2, text="English",value="en", variable=radio_var)
                    radio_en.pack(side="left", anchor="w")
                elif (i[0:2] == "ar") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_ar = ttk.Radiobutton(radio_frame, text="Arabic",value="ar", variable=radio_var)
                    else:
                        radio_ar = ttk.Radiobutton(radio_frame2, text="Arabic",value="ar", variable=radio_var)
                    radio_ar.pack(side="left", anchor="w")
                elif (i[0:2] == "zh") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_zh = ttk.Radiobutton(radio_frame, text="Chinese",value="zh", variable=radio_var)
                    else:
                        radio_zh = ttk.Radiobutton(radio_frame2, text="Chinese",value="zh", variable=radio_var)
                    radio_zh.pack(side="left", anchor="w")
                elif (i[0:2] == "de") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_de = ttk.Checkbutton(radio_frame, text="German",value="de", variable=radio_var)
                    else:
                        radio_de = ttk.Radiobutton(radio_frame2, text="German",value="de", variable=radio_var)
                    radio_de.pack(side="left", anchor="w")
                elif (i[0:2] == "hi") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_hi = ttk.Radiobutton(radio_frame, text="Hindi",value="hi", variable=radio_var)
                    else:
                        radio_hi = ttk.Radiobutton(radio_frame2, text="Hindi",value="hi", variable=radio_var)
                    radio_hi.pack(side="left", anchor="w")
                elif (i[0:2] == "it") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_it = ttk.Radiobutton(radio_frame, text="Italian",value="it", variable=radio_var)
                    else:
                        radio_it = ttk.Radiobutton(radio_frame2, text="Italian",value="it", variable=radio_var)
                    radio_it.pack(side="left", anchor="w")
                elif (i[0:2] == "ja") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_ja = ttk.Radiobutton(radio_frame, text="Japanese",value="ja", variable=radio_var)
                    else:
                        radio_ja = ttk.Radiobutton(radio_frame2, text="Japanese",value="ja", variable=radio_var)
                    radio_ja.pack(side="left", anchor="w")
                elif (i[0:2] == "ko") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_ko = ttk.Radiobutton(radio_frame, text="Korean",value="ko", variable=radio_var)
                    else:
                        radio_ko = ttk.Radiobutton(radio_frame2, text="Korean",value="ko", variable=radio_var)
                    radio_ko.pack(side="left", anchor="w")
                elif (i[0:2] == "pl") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_pl = ttk.Radiobutton(radio_frame, text="Polish",value="pl", variable=radio_var)
                    else:
                        radio_pl = ttk.Radiobutton(radio_frame2, text="Polish",value="pl", variable=radio_var)
                    radio_pl.pack(side="left", anchor="w")
                elif (i[0:2] == "pt") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_pt = ttk.Radiobutton(radio_frame, text="Portuguese",value="pt", variable=radio_var)
                    else:
                        radio_pt = ttk.Radiobutton(radio_frame2, text="Portuguese",value="pt", variable=radio_var)
                    radio_pt.pack(side="left", anchor="w")
                elif (i[0:2] == "ru") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_ru = ttk.Radiobutton(radio_frame, text="Russian",value="ru", variable=radio_var)
                    else:
                        radio_ru = ttk.Radiobutton(radio_frame2, text="Russian",value="ru", variable=radio_var)
                    radio_ru.pack(side="left", anchor="w")
                elif (i[0:2] == "es") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_es = ttk.Radiobutton(radio_frame, text="Spanish",value="es", variable=radio_var)
                    else:
                        radio_es = ttk.Radiobutton(radio_frame2, text="Spanish",value="es", variable=radio_var)
                    radio_es.pack(side="left", anchor="w")
                elif (i[0:2] == "tr") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_tr = ttk.Radiobutton(radio_frame, text="Turkish",value="tr", variable=radio_var)
                    else:
                        radio_tr = ttk.Radiobutton(radio_frame2, text="Turkish",value="tr", variable=radio_var)
                    radio_tr.pack(side="left", anchor="w")
                elif (i[0:2] == "uk") and (i not in radio_lang):
                    radio_lang.append(i)
                    if counter < 8:
                        radio_uk = ttk.Radiobutton(radio_frame, text="Ukrainian",value="uk", variable=radio_var)
                    else:
                        radio_uk = ttk.Radiobutton(radio_frame2, text="Ukrainian",value="uk", variable=radio_var)
                    radio_uk.pack(side="left", anchor="w")
                counter+=1
            """
        l4.pack()
        mp4_elements = []

        highest_resolution = 0

        resolutions_max = {}
        
        # Parcourir les éléments filtrés
        resolutions = []
        resolutions_max = {}
        for element in qualities:
            match = re.search(r'([^ ]+)\s+(?:mp4|webm)\s+(\d+x\d+)', element)  # Rechercher le nombre et la résolution
            if match:
                number = match.group(1)
                resolution = match.group(2)
                width, height = resolution.split('x')
                width = int(width)
                height = int(height)
                if width not in resolutions_max or height > resolutions_max[width]['height']:
                    resolutions_max[width] = {'height': height, 'number': number}

        # Construire le tableau final avec le nombre et la résolution maximale pour chaque largeur
        tableau_final = [f'{resolutions_max[width]["number"]} mp4 {width}x{resolutions_max[width]["height"]} ({resolutions_max[width]["height"]})' for width in sorted(resolutions_max.keys())]
        
        resolutions = []
        
        # Parcourir les éléments du tableau final
        for element in tableau_final:
            match = re.search(r'(\d+x\d+)', element)  # Rechercher la résolution
            if match:
                resolution = match.group(1)
                resolutions.append(resolution)

        qualities_text=resolutions
        resolutions = []
        for element in tableau_final:
            elements = element.split()
            match = re.search(r'\d+', element)  # Rechercher les nombres
            if match:
                number = match.group()
                resolutions.append(number)
                
        qualities = resolutions        
        radio2_frame = ttk.Frame(app)
        radio2_frame.pack()

        # Variable pour stocker la valeur sélectionnée
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
        print(e)
    except FileNotFoundError or UnicodeDecodeError as e:
        lerror.config(text=": Invalide Cokkies File :")
        lerror.pack()
        app.update()
        b1.config(state="normal")
        b5.config(state="normal")
        print(e)
    except Exception as e:
        lerror.config(text=e)
        lerror.pack()
        app.update()
        b1.config(state="normal")
        b5.config(state="normal")
        print(e)
        
        
def download_video():
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
    
    try:
        lang=radio_var.get()
        if lang=="":
            lang_verify=0
    except:
        pass
    
    subs_lang = []
    for i in range(len(subtitle_languages)):
        checkbox_var = checkbox_vars[i].get()  # Récupère l'état de la case à cocher

        if checkbox_var:  # Si la case à cocher est cochée
            subs_lang.append(subtitle_languages[i]) 
    print(subs_lang)
    
    
    
    if len(subs_lang) != 0:
        subs_lang_verify= True
    else:
        subs_lang_verify = False
    if lang_verify == 1:
        formats=f"bestvideo[width={width}][height={height}]+bestaudio[language={lang}]/best/[width={width}][height={height}]"
    else:
        formats=f"bestvideo[width={width}][height={height}]+bestaudio/best[width={width}][height={height}]"
    video_name2=video_name+".tempmp4"
    subs_lang.append("-live_chat")
    if file_cookie != "":
        ydl_opts = {
            'cachedir': r'C:\Users\Célestin\Desktop\traduction\test\trad\cache',
            'writesubtitles': True,
            'verbose': True,
            #'outtmpl' : video_name2,
            'subtitleslangs': subs_lang,
            'format': formats,
            'progress_hooks': [progress_hook],
            'playlistend': 0,
            'cookiefile': file_cookie,
            'no_color': True,
            'quiet': True,
            'noprogress': True,
            }
    else:
        ydl_opts = {
            'cachedir': r'C:\Users\Célestin\Desktop\traduction\test\trad\cache',
            'writesubtitles': True,
            #'outtmpl' : video_name2,
            'subtitleslangs': subs_lang,
            'format': formats,
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_color': True,
            'subtitlesformat': 'json3',
            'playlistend': 0,
            'noprogress': True,
            }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    ydl_opts=""
    #subprocess.call(f'ffmpeg -i {video_name}.tempmp4 -vf scale={width}:{height} {video_name}.mp4',shell=True)
    b3.config(state="normal")
    b4.config(state="normal")
# Exécution de la commande FFmpeg


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
        l6.config(text="Downloading finished !")
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
    
    for i in checkbox_lists:
        i.pack_forget()
    try:
        checkbox_frame2.pack_forget()
    except:
        pass
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
#app.geometry("580x350")

min_width = 580
min_height = 150

app.minsize(min_width, min_height)

#app.geometry(f"{max(app.winfo_width(), min_width)}x{max(app.winfo_height(), min_height)}")
#app.minsize(min_width, min_height)

#app.geometry(f"{max(app.winfo_width(), min_width)}x{max(app.winfo_height(), min_height)}")
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
subs= StringVar()
subs.set(0)
l2= ttk.Label(app, anchor='center', text = " Subtitles : ", font = errfont)
#l2.pack()
radio_frame = ttk.Frame(app)
radio_frame.pack(side="top", anchor="n")
r1 = ttk.Radiobutton(radio_frame, text="No", variable=subs, value=2)
#r1.pack(side='left',anchor="w")
r2 = ttk.Radiobutton(radio_frame, text="Yes", variable=subs, value=1)
#r2.pack(side='left',anchor="w")

l2_2 = ttk.Label(app, anchor='center', text = " Language : ", font =errfont)

#b1 = ttk.Button(app, text="Browse", command=browse_file)
#b1.pack()

l4= ttk.Label(app, anchor='center', text='Resolutions :', font = errfont)
"""
l7= ttk.Label(app, anchor='center', text = 'Quality ( % ) :')
l7.pack()
quality_var= StringVar(app)
quality_var.set("100")
spinbox1 = ttk.Spinbox(app, from_=0, to=100, textvariable=quality_var)
spinbox1.pack()
l8= ttk.Label(app, anchor='center', text='( May can alterate the drawing time )')
l8.pack()
"""
b3 = ttk.Button(app, text="Download", command=threading)
b4 = ttk.Button(app, text="Back", command=back)
#b3.pack()
p1 = ttk.Progressbar(app, orient='horizontal', length=500, mode='determinate')
#p1.pack()
l5= ttk.Label(app, anchor='center', text='')
#l5.pack()
l6= ttk.Label(app, anchor='center', text = '')
#l6.pack()
lerror= ttk.Label(app, anchor='center', text='')
lerror.pack()
app.mainloop()
exit()