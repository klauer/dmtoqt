Documentation for dmtoqt is generated using Sphinx (http://www.sphinx-doc.org).

Generating documentation requires that the Sphinx package be installed.  Once that's
done, follow these steps:

cd doc
make

HTML documentation will then be in the doc/_build/html subdirectory.  You may copy
it to a web-accessible directory if you want to make it available at your site.

To generate other formats (such as Qt help files), simply add the builder name to
the OUTPUT variable in the make command.  For instance,

make OUTPUT=qthelp

For a list of builders, refer to http://www.sphinx-doc.org/en/stable/builders.html.
