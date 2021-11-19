[![Tech](https://img.shields.io/static/v1?label=build&message=python3.7&color=009933)]()
[![Serverless declare](https://img.shields.io/static/v1?label=docker&message=microservice&color=ff69b4)]()

### This is the assignment of <a href="https://www.pelago.co/en-SG/">pelago</a> Easy to understand

# zeus
<img src="https://user-images.githubusercontent.com/5208231/130122261-312467a7-fc49-4e2a-abcb-c1fdda51c63f.png" width="200"/>

Zeus is the king of Olympians, all the power from his thunder

So, I put the functions in folder thunder of this project.

# Usage
### How to build
- step 1. install docker to your local. Click <a href="https://docs.docker.com/engine/install/">here</a> to install docker
- step 2. make sure you have docker-compose command working in your local, by type `$ docker-compose` if you see something as below screenshot you are ready to go.😀
![image](https://user-images.githubusercontent.com/5208231/130255489-7d76e202-6c79-400b-bc32-8a00a412cda1.png)
- step 3. (OPTIONAL) install python venv to the working folder, this one is tricky please be careful to do step by step as the following instruction.
```bash
# If window
python -m pip install --upgrade
python -m pip install --user virtualenv
python -m venv .venv # the second parameter is the target folder name. Please leave as the same.
.\.venv\Scripts\activate # Active the venv

# If mac
python -m pip install --user --upgrade pip
python -m pip install --user virtualenv
python -m venv .venv
source env/bin/activate
```
Afterwards you can see .venv folder be created
![image](https://user-images.githubusercontent.com/5208231/130257014-258429d9-31e1-4bbd-918c-74fb5ad0d796.png) 
And also you can see you are already in .venv source in your command line ![image](https://user-images.githubusercontent.com/5208231/130257225-7b9c7dbe-d32e-4d00-9699-9ab9c65756e4.png)

- step 4. run `$ docker-compose build`
- step 5. run `$ docker-compose up`
  - For the first time zeus will load the remote data and insert data to mongoDB, that require some time, you may need to wait for 1 to 2 min till the docker log showing the `Listening on port 5000` then you are ready to go.
  - Otherwise you can manually check the mongoDB by use this link <a href="http://localhost:8081/db/Olympians/Parthenon">http://localhost:8081/db/Olympians/Parthenon</a>
  - If every thing is OK, you can see the data be listed in mongoDB
  ![image](https://user-images.githubusercontent.com/5208231/130258814-6855d49c-716a-44e3-92ab-3979a0551ac3.png)
  - PS: the second time you start zeus, if the data already be init, zeus will not load remote data again.

### How to run
- If run docker
  - Open your <a href="https://www.postman.com/">postman</a> to access `http://localhost:5999` If you can see below, that means zeus is ready to use.
  ![image](https://user-images.githubusercontent.com/5208231/130259582-8ffd7f93-634d-477b-ae96-872a16ef7d16.png)
- Run qurey API
  - Use `localhost:5999/search?q=<package name>` to invoke query API
![image](https://user-images.githubusercontent.com/5208231/130259949-3c5bc574-a8ff-4576-a0d9-c9399b976a12.png)
  - For each package, the first time will be a little bit slow, because it require to retreve the tar file to do the data erichment. After that it will be respond fast.


### How to stop
To stop zeus, it's easy. Just you `Ctrl+C` in you terminal, please be patient to wait all the images be stoped, if you click `Ctrl+C` again to force stop docker, that may cause some issue during the next time you want to start up. You need to go to you docker desktop to delete the images and containers and rebuid it.


# Architecture
![image](https://user-images.githubusercontent.com/5208231/130275906-9ab030c4-51e4-46cf-8e96-feec1c858f36.png)

