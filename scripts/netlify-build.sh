#!/usr/bin/env sh

curl -L https://github.com/rust-lang/mdBook/releases/download/v0.4.7/mdbook-v0.4.7-x86_64-unknown-linux-gnu.tar.gz | tar xvz

./mdbook build
