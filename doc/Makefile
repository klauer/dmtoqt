# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = dmtoqt
SOURCEDIR     = .
BUILDDIR      = _build
OUTPUT        = html
INSTALLDIR    = /home/als2/www/htdoc/alscg/dmtoqt
TAG           = `hg log -r "." --template "{latesttag}\n"`

all: api $(BUILDDIR)

clean:
	rm -rf api $(BUILDDIR)

install:
	cp -rfp $(BUILDDIR)/$(OUTPUT) $(INSTALLDIR)/$(TAG)
	unlink $(INSTALLDIR)/latest
	ln -s $(INSTALLDIR)/$(TAG) $(INSTALLDIR)/latest

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

#.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

FILES=Makefile \
	../dmtoqt.py \
	../findEDMProps.py \
	../setup.py \
	../version.py \
	../src/ColorsParser.py \
	../src/DMReader.py \
	../src/edmVarTypes.py \
	../src/EDMWidget.py \
	../src/__init__.py \
	../src/StackedEDMWidget.py \
	../src/UIWriter.py \
	../src/widgets/activeArcClass.py \
	../src/widgets/activeBarClass.py \
	../src/widgets/activeButtonClass.py \
	../src/widgets/activeChoiceButtonClass.py \
	../src/widgets/activeCircleClass.py \
	../src/widgets/activeExitButtonClass.py \
	../src/widgets/activeGroupClass.py \
	../src/widgets/activeLineClass.py \
	../src/widgets/activeMenuButtonClass.py \
	../src/widgets/activeMessageButtonClass.py \
	../src/widgets/activeMeterClass.py \
	../src/widgets/activeMotifSliderClass.py \
	../src/widgets/activeRadioButtonClass.py \
	../src/widgets/activeRectangleClass.py \
	../src/widgets/activeSliderClass.py \
	../src/widgets/activeUpdownButtonClass.py \
	../src/widgets/activeWindowClass.py \
	../src/widgets/activeXTextClass.py \
	../src/widgets/activeXTextDspClass.py \
	../src/widgets/BaseWidget.py \
	../src/widgets/ByteClass.py \
	../src/widgets/__init__.py \
	../src/widgets/relatedDisplayClass.py \
	../src/widgets/shellCmdClass.py \
	../src/widgets/StackWidget.py \
	../src/widgets/TextupdateClass.py \
	../src/widgets/widget_template.py \
	../src/widgets/xyGraphClass.py

DOCS=index.rst \
	devel.rst \
	env.rst \
	faq.rst \
	findEDMProps.rst \
	license.rst \
	overview.rst \
	stack.rst \
	widgets.rst \
	conf.py


API_EXCLUDES=../setup.py \
	../version.py \
	../src/widgets/widget_template.py

api: $(FILES)
	rm -rf api/*
	sphinx-apidoc -f -o api .. $(API_EXCLUDES)

$(BUILDDIR): api $(DOCS)
	mkdir -p $(BUILDDIR)
	@$(SPHINXBUILD) -M $(OUTPUT) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

