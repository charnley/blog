port=5000
env=./env
python=./${env}/bin/python

all:
	bundle install

config:
	bundle config set --local path '${HOME}/.local/share/gem'

dev:
	bundle exec jekyll serve --host 0.0.0.0 --port ${port} --drafts

start:
	bundle exec jekyll serve --host 0.0.0.0 --port ${port}

format:
	prettier

# Python (for plots)

${env}:
	uv venv ${env} --python 3.12
	uv pip install -r requirements.txt --python ./${env}/bin/python

# Extra content

record-terminal-demo:
	terminalizer record demo --config ./configs/terminalizer_config.yml

render-terminal-demo:
	terminalizer render demo
