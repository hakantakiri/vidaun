import yt_dlp as DL
import tkinter as tk
from tkinter import filedialog
from pathvalidate import sanitize_filename


def download(url:str, outname:str) -> str:
    if(url == None):
        print('Insert a valid url')
        return
    full_outname =  outname
    ydl_opts = {
        'format': 'best[height=720]',
        'outtmpl': full_outname,
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True,
    }

    result = 0

    with DL.YoutubeDL(ydl_opts) as ydl:
        r = ydl.download([url])
        if(r == 1):
            result = 1

    if (result == 1):  # An error ocurred while downloading, it doesn't throw errors
        print(
            'Unable to download with 720p resolution. Trying its default best resolution.')
        result = 0  # Restarting error indicator to its original value
        ydl_opts['format'] = 'best'
        with DL.YoutubeDL(ydl_opts) as ydl:
            r = ydl.download([url])
            if(r == 1):
                result = 1

    if (r == 1):
        raise Exception('There was a problem while downloading')

    return full_outname

def get_info_without_download(url: str):
    if(url == None):
        print('Insert a url.')
        return

    ydl_opts = {

    }
    with DL.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info
    

def get_formats(url:str):
    formats = []
    raw_formats = get_info_without_download(url)['formats']
    for raw_format in raw_formats:
        formats.append(raw_format['format_id'])
    return formats

def run() :

    state_no_process = ''
    state_loading = 'Loading'
    state_finisçhed = 'Finished'
    final_name = ''

    root = tk.Tk()
    root.title('Vidaun')




    def getFolder():
    
        folder_selected = filedialog.askdirectory()
        print('selected folder is:')
        print(folder_selected)
        return folder_selected



    def click_download():
        url.config(state = 'disabled')
        print('Downloading url: {}'.format(url.get()))

        folder_name = getFolder()
        info = get_info_without_download(url.get())
        
        title = sanitize_filename(info['title'])
        preview_url = info['thumbnails'][0]['url']
        
        formats = []
        for f in info['formats']:
            formats.append({
                'format': f['format_id'], 
                'resolution': f['resolution'],
                'ext':f['ext']
                })

        print('info:')
        print(info['formats'])
        # print(info['title'])
        # print(formats)
        print('preview url: ', preview_url)



        url.config(state='disabled')
        download_button.config(state='disabled')
        name.config(state='normal')

        name.insert(0, folder_name+'/'+title.replace(' ', '_')+'.mp4')

        save_button.config(state='normal')



    def save():

        name.config(state='disabled')
        download(url.get(), name.get())

        url.config(state='normal')
        download_button.config(state='normal')

        name.config(state='disabled')
        save_button.config(state='disabled')


    title_label = tk.Label(root, text = "Vidaun")
    input_url_label = tk.Label(root, text = "Insert Url")
    url = tk.Entry(root, width=50)
    name = tk.Entry(root, width=35)
    process_label =tk.Label(root, text=state_no_process)
    download_button = tk.Button(root, text='Download',command=lambda: click_download(), bg='white')
    img = tk.PhotoImage()
    save_button = tk.Button(root, text='Save', command=lambda: save(), bg='green')



    title_label.pack()
    input_url_label.pack()
    url.pack()
    process_label.pack()
    download_button.pack()
    name.pack()
    name.config(state='disabled')

    save_button.pack()
    save_button.config(state='disabled')

    root.mainloop()


if __name__ == "__main__":
    run()




    

