# Go Image 
Host Images for free via your Github and get pretty easy to remember links to use it wherever you want.

[Interactive Link Generator](https://go-image-8la.pages.dev/)

[Demo Page Repo](https://go-image-8la.pages.dev/)

[GoImage Server Repo](https://go-image-8la.pages.dev/)


## Self Host

You can self-host this microservice in your infra using Docker to enable advanced features such as Image caching.
```bash
docker pull ans29hul/goimg1:latest
```

## Usage

#### Generate GitHub Image Links
Create a repo called **goimg** and push all your images to the **main** branch, then use the link as shown to access them directly. 
```
http://goimg.me/g/<user_name>/<filename>
```

Example: <http://goimg.me/g/anshulagx/a.png>

---
#### Generate GitHub Image Links for a specific repo
```
http://goimg.me/gr/<user_name>/<repo_name>/<filename>
```
Example: <http://goimg.me/gr/anshulagx/goimg/a.png/>

---
#### Get Images and format them via URL

List of valid Query params

 **Query Param** | **Description** | **Values**   
-----------------|-----------------|--------------
 w               | Width           | in px        
 h               | Height          | in px        
 rot             | Rotation        | in degrees   
 b               | Blur            | true/false   
 f               | Image format    | jpeg/png/bmp 
 q               | Quality         | 0\-100       

```
http://www.goimg.me/?img=<url>&w=<width>....
```
Example: <http://www.goimg.me/?img=https://images.unsplash.com/photo-1640132090233-8c418da50822?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY0MTcxNDczMw&ixlib=rb-1.2.1&w=200&h=200&f=png>

---
#### Generate a Random Image
```
http://www.goimg.me/
```
Example: <http://www.goimg.me>


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
