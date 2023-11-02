import tkinter as tk

root = tk.Tk()
root.title('Vidaun')


def download():
    print('Downloading url: {}'.format(url.get()))

title_label = tk.Label(root, text = "Vidaun")
input_url_label = tk.Label(root, text = "Insert Url")
url = tk.Entry(root, width=50)
download_button = tk.Button(root, text='Download',command=lambda: download(), bg='white')



title_label.pack()
input_url_label.pack()
url.pack()
download_button.pack()


root.mainloop()