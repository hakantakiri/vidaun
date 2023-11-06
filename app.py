import app.services.downloadService as DS
import tkinter as tk
from tkinter import filedialog

def run() :

    state_no_process = ''

    root = tk.Tk(className='Vidaun')
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

        info = DS.get_info_without_download(url.get())
        print('info')
        print(info)
        out_name = folder_name+'/'+(info['title']).replace(' ', '_')+'.mp4'
        url.config(state='disabled')
        download_button.config(state='disabled')
        name.config(state='normal')

        name.insert(0, out_name)

        save_button.config(state='normal')

    def save():

        name.config(state='disabled')
        DS.download(url.get(), name.get())

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




    

