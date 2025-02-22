
all:
	bundle install

config:
	bundle config set --local path '${HOME}/.local/share/gem'

dev:
	bundle exec jekyll serve

# Local env
any:

# Make new post with date
new-post:
	# TODO

host:
	# TODO

