# GoIT_WEB_HW_4
Individual homework #4 in GoIT school (Python WEB) 

### Installation
Clone this repository
```
https://github.com/S-Stepanov-1/GoIT_WEB_HW_4.git
```

### Description
The file `main.py` implements a simple web application. Here we have two simple servers running in separate threads. 

The HTTP server runs on port 3000.
The socket server runs on port 5000.

During the execution of the program the statistical resources `style.css`, `logo.png` are processed; also the work with the form on the page `message.html` is implemented.
The data we get on the `message.html` page is sent to the `socket server`, processed and stored in `data.json`.

### Docker
The image is available on the docker hub.
```
docker push stepanovdevelop/my-simple-web-app:tagname
```

When you start the docker container, the `storage` folder is created on the local computer (if it is missing).

Use the command in your command line to start the container:
```
docker run -p 3000:3000 -v d:/storage:/app/storage stepanovdevelop/my-simple-web-app
```

