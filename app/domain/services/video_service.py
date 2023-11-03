import yt_dlp as DL

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