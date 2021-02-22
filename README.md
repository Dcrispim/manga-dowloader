# Manga Downloader

This a application to create PDF files from mangas images.

## API

### 1.1 Download a specifc manga

The main function of aplications is the `download_manga()` from __manga.py__ module. This functions:

* Make download of manga chapeters
* Fix the images: Rotate the horizontal images
* Fit the images: Resize to Kindle ratio (can be changed on __config.json__)
* Convert the Chapter in PDF file

Folder tree exemple after manga download
CMD: __./run ajin 6__

```
Documents
└── mangas
    └── ajin
        ├── Ajin Cap0001.pdf
        ├── Ajin Cap0002.pdf
        ├── Ajin Cap0003.pdf
        ├── Ajin Cap0004.pdf
        ├── Ajin Cap0005.pdf
        ├── Ajin Cap0006.pdf
        └── jpgs
            ├── ajin_cap0001
            │   ├── 01.jpg
            │   ├── 02.jpg
            │   └── 03.jpg
            |   ... 
            ├── ajin_cap0002
            │   ├── 01.jpg
            │   ├── 02.jpg
            │   └── 03.jpg
            |   ... 
            ├── ajin_cap0003
            │   ├── 01.jpg
            │   ├── 02.jpg
            │   └── 03.jpg
            |   ... 
            ├── ajin_cap0004
            │   ├── 01.jpg
            │   ├── 02.jpg
            │   └── 03.jpg
            |   ... 
            ├── ajin_cap0005
            │   ├── 01.jpg
            │   ├── 02.jpg
            │   └── 03.jpg
            |   ... 
            └── ajin_cap0006
                ├── 01.jpg
                ├── 02.jpg
                └── 03.jpg
                ... 

```


#### Params

* __manga-name__: name of manga splited with "__-__"  ex: boku-no-hero-academia
* __end-chapter__: number of chapter which ends the manga
* __custom-start-chapter__: chapter number if is diferent of 1
* __especial-chapters__: chapters splited with "__/__" ex: 28.5/80.7/90-2 
    * or a file path starting  with "__//__" ex: __//___/home/user/documents/esp.tsx_
* __exclude-chapters__: chapters splited with "__/__" ex: 28.5/80.7/90-2 


`./run` `<manga-name>` `<end-chapter>` `--start=<custom-start-chapter>` `--especials=<especial-chapters>` `--exclude=<exclude-chapters>`

```shell
./run magi-sinbad-no-bouken 182 --start=0 --especials=70.5/51.5/43.5
```
ou
```shell
./run magi-sinbad-no-bouken 182 --start=0 --especials=///home/user/Documents/esp.txt
```

esp.txt
```
70.5/51.5/43.5
```

### 1.2 Extensions

You can make extensions with decorator @extension. The functions are given * args and normally args [0] is the name of the manga. but this can be changed if necessary

```python
from decorators import extension
@extension
def myExtension(*args):
    #my logic

if __name__ == "__main__":
    myExtension()


```

The extesion files must finish with `.ext.py` to be recognized.

run extension `my-extension.ext.py`
```
./extension my-extension args1 args2 args3 ...
```