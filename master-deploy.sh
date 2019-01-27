# !/bin/bash
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker login -u gitlab-ci-token -p $DOCKER_TOKEN registry.gitlab.com"

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network create --subnet=172.22.0.0/16 social-service-network'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container stop social'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container stop social-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container rm social'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container rm social-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/social-service/social-swagger -q)'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/social-service/social -q)'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker run -d --restart always -e 'API_URL=definitions/swagger.yml' --name social-swagger --network social-service-network --ip 172.22.0.3 $REGISTRY_REPO/$SWAGGER:$TAG"
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker run -d --restart always -e 'FLASK_ENV=development' -e 'FLASK_APP=manage.py' -e 'APP_SETTINGS=project.config.DevelopmentConfig' -e 'DATABASE_URL=postgres://$DATABASE_PROD_USER:$DATABASE_PROD_PASSWORD@$DATABASE_PROD_URL:$DATABASE_PROD_PORT/$DATABASE_PROD_NAME' -e 'SECRET_KEY=$PROD_SECRET_KEY' -e USERS_SERVICE_URL=$PROD_USERS_SERVICE_URL -e AUTH_SERVICE_URL=$PROD_AUTH_SERVICE_URL -e COMPANIES_SERVICE_URL=$PROD_COMPANIES_SERVICE_URL -e NOTIFICATIONS_SERVICE_URL=$PROD_NOTIFICATIONS_SERVICE_URL -e 'AWS_BUCKET_NAME=onelike-prod' --name social --network social-service-network --ip 172.22.0.2 $REGISTRY_REPO/$SOCIAL:$TAG"

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network connect onelike-network --ip 172.18.0.10 social'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network connect onelike-network --ip 172.18.0.11 social-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container exec social python manage.py db upgrade'
