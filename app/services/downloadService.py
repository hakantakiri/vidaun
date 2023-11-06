from pathvalidate import sanitize_filename
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
    
    if(url == None): return
    
    # Initializing variables
    response = {
        'url': url,
        'title': None,
        'formats': [],
        'preview_image': None,
    }
    info = None
    formats = []

    # Downloading raw info from url
    try:
        ydl_opts = {}
        with DL.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e: 
        print('There was an error verifying if video from url can be downloaded.')
    
    if info == None : return None
    
    raw_formats = info['formats'] if 'formats' in info else info['entries']
    for raw_format in raw_formats:
        formats.append({
            'format_id':  raw_format['format_id'] if hasattr(raw_format, 'format_id') else None,
            'resolution': raw_format['resolution'] if hasattr(raw_format, 'resolution') else None,
            'ext': raw_format['ext'] if hasattr(raw_format,'ext') else None,
            'fps': raw_format['ext'] if hasattr(raw_format,'fps') else None,
            'format':  raw_format['format'] if hasattr(raw_format, 'format')   else None,
            'dynamic_range': raw_format['dynamic_range'] if hasattr(raw_format, 'dynamic_range') else None,
        })
    
    # Formatting response
    response['title'] = sanitize_filename(info['title']).replace(' ', '_')
    response['formats'] = formats
    response['preview_image'] = info['thumbnails'][0]['url'] if hasattr(info, 'thumbnails') else info['entries'][0]['thumbnails'][0]['url']

    return response
