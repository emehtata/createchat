NAME=createchat
NAMESPACE=$(NAME)
IMAGE=localhost:5000/$(NAME)
VERSION := $(shell date +%Y.%m.%d)-$(shell git rev-parse --short HEAD)

build:

	echo "VERSION = '$(VERSION)'" > app/my_version.py    
	docker build . -t $(IMAGE)

run:
	docker run -d -p 5777:5777 --name $(NAME) $(IMAGE)

stop:
	docker stop $(NAME)
	docker rm $(NAME)

push:
	docker push $(IMAGE)

install:
	helm upgrade --install $(NAME) k8s/chart -n $(NAMESPACE) --create-namespace

uninstall:
	helm uninstall $(NAME) -n $(NAMESPACE)
