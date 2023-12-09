aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 098964451146.dkr.ecr.eu-west-3.amazonaws.com

# docker build -t vocabulary .
docker-compose build

docker tag vocabulary_web:latest public.ecr.aws/e8w4p1y9/vocabulary_compose:latest
#docker tag vocabulary_web:latest 098964451146.dkr.ecr.eu-west-3.amazonaws.com/vocabulary_web:latest

#docker push 098964451146.dkr.ecr.eu-west-3.amazonaws.com/vocabulary_compose:latest
docker push public.ecr.aws/e8w4p1y9/vocabulary_compose:latest
