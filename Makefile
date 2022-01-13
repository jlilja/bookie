name=bookie

build:
	docker build -t $(name) .

run:
	docker run $(name)

run-dev:
	cp /home/j/.mozilla/firefox/37rfrt13.default/places.sqlite /home/j/Private/bookie
	docker run \
		-v "$(PWD):/usr/src/app" \
		-v "$(HOME)/.mozilla/firefox:$(HOME)/.mozilla/firefox" \
		-v "$(HOME)/Desktop:$(HOME)/Desktop" \
		$(name)
