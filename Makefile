.PHONY:   build_app_image register_app_image app_local_up app_helm_up 


# deploy app in local
app_local_up:
	docker compose -f deployment/app/docker-compose.yaml up -d

# build calculator app image
build_app_image:
	docker build -f deployment/app/App_Dockerfile -t kevvn/calculator-app .

register_app_image:
	docker push kevvn/calculator-app