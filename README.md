# dxtracter
<p align="center">
   <img width="240" height="380" src="https://github.com/dylanchang44/dxtracter/assets/52403864/6ab7b12a-5402-4d69-8d85-d8100cc3970c">
</p>
<h4 align="center">A telegram bot to provide infos of the stock, with following features</h4>

<p align="center">
- dockerize
- github action
- AWS ec2 hosting
</p>

## Workflow

- Image CI
- Deploy to EC2
```sh
Push the update => Build program as a docker image => Push the image to dockerhub => SSH to AWS ec2 instance => Clear the existing local image => Pull and run latest image from Docker Hub => Done! The bot is running with latest update
```

### Deployment on push


https://github.com/dylanchang44/dxtracter/assets/52403864/6ecba497-c1fa-402b-af6a-cdf464929006



### DEMO


https://github.com/dylanchang44/dxtracter/assets/52403864/a0770698-0b3d-4026-b97b-e0a4cbaff87b



