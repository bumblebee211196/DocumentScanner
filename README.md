# DocumentScanner

A simple document scanner using python and opencv. For detailed explanation check out my [blog](https://bumblebee2196.netlify.app/simple-document-scanner/).

This was possible only due to the simple and clear explanation by Adrian Rosebrock's [blog](https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/).

## How to run?

1. Create virtual environment

```
python3 -m venv my_env
source my_env/bin/activate
```

2. Install required dependencies

```
pip3 install -r requirements.txt
```

3. Execute

```
python3 -m scanner -i /path/to/image/file.jpg
```