# dxtracter
<p align="center">
   <img width="200" height="380" src="[https://picsum.photos/460/300](https://github.com/dylanchang44/dxtracter/assets/52403864/84f43aab-2c74-48cf-93cd-6a5a7f23e9d4)">
</p>
<h4 align="center">A telegram bot to provide infos of the stock, with below features</h4>

- dockerize
- github action
- AWS ec2 hosting

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



