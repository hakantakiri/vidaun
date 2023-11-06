import app.services.downloadService as DS
import tkinter as tk
from tkinter import filedialog
from enum import Enum
import threading
from queue import Queue

def run() :

    root = tk.Tk(className='Vidaun')
    root.title('Vidaun')

    class STEP_ENUM(Enum):
        INSERT_URL = '1',
        VALIDATING_URL = '2'
        SELECT_FOLDER = '3',
        FOLDER_SELECTED = '4',
        DOWNLOADING = '5',
        DOWNLOADED = '6'
        
    def interface_set_step(step: STEP_ENUM):
        
        if( step == STEP_ENUM.INSERT_URL):
            url.config(state = 'normal')
            url.delete(0, 'end')
            url.focus_set()
            download_button.config(state='normal')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
            return
            
        if( step == STEP_ENUM.VALIDATING_URL):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
            return
        
        if( step == STEP_ENUM.SELECT_FOLDER):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='disabled')
            name.config(state='normal')
            name.delete(0, 'end')
            save_button.config(state='disabled')
            return
        
        if( step == STEP_ENUM.FOLDER_SELECTED):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='normal')
            name.config(state='normal')
            save_button.config(state='normal')
            return
        
        if( step == STEP_ENUM.DOWNLOADING):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
            return
        
        if( step == STEP_ENUM.DOWNLOADED):
            url.config(state = 'normal')
            download_button.config(state='normal')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
            return

    def interface_ask_folder():
        folder_selected = filedialog.askdirectory()
        print('selected folder is:')
        print(folder_selected)
        return folder_selected
    
    def validate_url(url:str, thread_resp:Queue):
        result = DS.get_info_without_download(url)
        thread_resp.put(result)

    def click_download(url: str):
        interface_set_step(STEP_ENUM.VALIDATING_URL)
        print('Downloading url: {}'.format(url))

        info = None
        thread_resp = Queue()
        thread = threading.Thread(target=validate_url, args=(url, thread_resp) )
        thread.start()
        thread.join()
        info = thread_resp.get()

        if info == None : 
            interface_set_step(STEP_ENUM.INSERT_URL)
            return
        interface_set_step(STEP_ENUM.SELECT_FOLDER)
        print('info')
        print(info)

        folder_name = interface_ask_folder()
        out_name = folder_name+'/'+(info['title']).replace(' ', '_')+'.mp4'
        name.insert(0, out_name)
        interface_set_step(STEP_ENUM.FOLDER_SELECTED)

    def save(url: str, out_name: str):
        interface_set_step(STEP_ENUM.DOWNLOADING)
        thread = threading.Thread(target=DS.download, args=(url, out_name))
        thread.start()
        thread.join()
        interface_set_step(STEP_ENUM.DOWNLOADED)
        interface_set_step(STEP_ENUM.INSERT_URL)

    # Defining interface
    title_label = tk.Label(root, text = "Vidaun")
    input_url_label = tk.Label(root, text = "Insert Url")
    url = tk.Entry(root, width=50)
    name = tk.Entry(root, width=35)
    download_button = tk.Button(root, text='Download',command=lambda: click_download(url.get()), bg='white')
    change_url_button = tk.Button(root, text="Change url", command= lambda: interface_set_step(STEP_ENUM.INSERT_URL))
    save_button = tk.Button(root, text='Save', command=lambda: save(url.get(), name.get()), bg='green')

    title_label.pack()
    input_url_label.pack()
    url.pack()
    download_button.pack()
    change_url_button.pack()
    
    name.pack()
    save_button.pack()

    interface_set_step(STEP_ENUM.INSERT_URL)

    root.mainloop()


if __name__ == "__main__":
    run()




    

