# dxtracter
<h4 align="center">A telegram bot to provide infos of the stock, with below features</h4>

- dockerize
- github action
- AWS ec2 hosting

## Workflow

- #c5f015 Docker Image CI
- #1589F0 Deploy to EC2

```sh
Push the update => <span style="color:green;">Build program as a docker image</span> => <span style="color:green;">Push the image to dockerhub</span> => <span style="color:yellow;">SSH to AWS ec2 instance</span> => <span style="color:yellow;">Clear the existing local image</span> => <span style="color:yellow;">Pull and run latest image from Docker Hub</span> => Done! The bot is running with latest update
```
### Deployment on push
https://www.youtube.com/watch?v=PlgFvjalyVk&ab_channel=DylanChang)https://www.youtube.com/watch?v=PlgFvjalyVk&ab_channel=DylanChang

### DEMO
https://www.youtube.com/watch?v=jFlgQn0ibBM&ab_channel=DylanChang)https://www.youtube.com/watch?v=jFlgQn0ibBM&ab_channel=DylanChang

