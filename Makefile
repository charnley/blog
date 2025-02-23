
all:
	bundle install

config:
	bundle config set --local path '${HOME}/.local/share/gem'

dev:
	bundle exec jekyll serve --host 0.0.0.0 --drafts

# Local env
any:

# Make new post with date
new-post:
	# TODO

host:
	# TODO

