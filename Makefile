IMAGE_NAME=mongp-demo:latest

build:
	docker build -t ${IMAGE_NAME} . 
	
init-sql:
	python -m scripts.insert_data_to_db