port=5000
env=./env
python=./${env}/bin/python

all:
	bundle install

${env}:
	uv venv ${env} --python 3.12
	uv pip install -r requirements.txt --python ./${env}/bin/python

config:
	bundle config set --local path '${HOME}/.local/share/gem'

dev:
	bundle exec jekyll serve --host 0.0.0.0 --port ${port} --drafts

start:
	bundle exec jekyll serve --host 0.0.0.0 --port ${port}

# Local env
any:

# Make new post with date
new-post:
	# TODO

host:
	# TODO

