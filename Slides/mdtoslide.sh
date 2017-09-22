#! /bin/bash
# Adrià Soto Tórtola
# 2ASIX
# Script que convierte Markdown a Slide
#----------------------------------------------------------

pandoc \
	--standalone \
	--to=dzslides \
	--incremental \
	--css=style.css \
	--output=presentacion.html \
presentacion.md
