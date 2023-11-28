import app.services.downloadService as DS
import app.utils.utils as utils
import tkinter as tk
from tkinter import filedialog
from enum import Enum
from threading import Thread
from multiprocessing import Process
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
        print(f'INTERFACE: Setting interface step to {step}')
        if( step == STEP_ENUM.INSERT_URL):
            url.config(state = 'normal')
            url.delete(0, 'end')
            url.focus_set()
            download_button.config(state='normal')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
            downloading_label.pack_forget()
        
        elif( step == STEP_ENUM.VALIDATING_URL):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
        
        elif( step == STEP_ENUM.SELECT_FOLDER):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='disabled')
            name.config(state='normal')
            name.delete(0, 'end')
            name.focus_set()
            save_button.config(state='disabled')
        
        elif( step == STEP_ENUM.FOLDER_SELECTED):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='normal')
            name.config(state='normal')
            name.focus_set()
            save_button.config(state='normal')
        
        elif( step == STEP_ENUM.DOWNLOADING):
            url.config(state = 'disabled')
            download_button.config(state='disabled')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
            downloading_label.pack()
        
        elif( step == STEP_ENUM.DOWNLOADED):
            url.config(state = 'normal')
            download_button.config(state='normal')
            change_url_button.config(state='disabled')
            name.config(state='disabled')
            save_button.config(state='disabled')
            downloading_label.pack_forget()
        
        else:
            print(f'INTERFACE: Step {step} is not implemented. ')
        
        print(f'INTERFACE: Step set to {step}')
            

    def interface_ask_folder():
        folder_selected = filedialog.askdirectory()
        print('selected folder is:')
        print(folder_selected)
        return folder_selected
    
    def validate_url(url:str, thread_resp:Queue):
        print('2.5- Message from inside the thread')
        result = DS.get_info_without_download(url)
        print('3- Final message form inside the thread')
        thread_resp.put(result)


    def click_download(url: str):
        interface_set_step(STEP_ENUM.VALIDATING_URL)
        print('1 - Downloading url: {}'.format(url))

        info = None
        thread_resp = Queue()
        thread = Thread(target=validate_url, args=[url, thread_resp] )
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
        out_name = folder_name+'/'+(utils.clean_name(info['title'])).replace(' ', '_')+'.mp4'
        name.insert(0, out_name)
        interface_set_step(STEP_ENUM.FOLDER_SELECTED)

    def save(url: str, out_name: str):
        interface_set_step(STEP_ENUM.DOWNLOADING)
        thread = Thread(target=DS.download, args=[url, out_name])
        thread.start()
        thread.join()
        interface_set_step(STEP_ENUM.DOWNLOADED)
        interface_set_step(STEP_ENUM.INSERT_URL)

    # Defining interface
    title_label = tk.Label(root, text = "Vidaun")
    input_url_label = tk.Label(root, text = "Insert Url")
    downloading_label = tk.Label(root, text= 'Downloading ...')
    url = tk.Entry(root, width=50)
    name = tk.Entry(root, width=35)
    url.bind('<Return>', lambda event:Thread(target=click_download, args=[url.get()]).start())
    download_button = tk.Button(root, text='Download',command=lambda:Thread(target=click_download, args=[url.get()]).start(), bg='white')
    change_url_button = tk.Button(root, text="Change url", command= lambda: interface_set_step(STEP_ENUM.INSERT_URL))
    name.bind('<Return>', lambda event:Thread(target=save, args=[url.get(), name.get()]).start())
    save_button = tk.Button(root, text='Save', command=lambda:Thread(target=save, args=[url.get(), name.get()]).start(), bg='green')	



    # Loading interface
    title_label.pack()
    input_url_label.pack()
    url.pack()
    download_button.pack()
    change_url_button.pack()
    
    name.pack()
    downloading_label.pack()
    save_button.pack()
    downloading_label.pack()

    interface_set_step(STEP_ENUM.INSERT_URL)
    root.mainloop()


if __name__ == "__main__":
    run()




    

