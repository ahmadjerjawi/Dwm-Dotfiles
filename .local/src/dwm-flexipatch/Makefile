# dwm - dynamic window manager
# See LICENSE file for copyright and license details.

include config.mk

SRC = drw.c dwm.c util.c
OBJ = ${SRC:.c=.o}
USER_HOME := $(shell sudo -u $(SUDO_USER) sh -c 'echo $$HOME')

# FreeBSD users, prefix all ifdef, else and endif statements with a . for this to work (e.g. .ifdef)

ifdef YAJLLIBS
all: dwm dwm-msg
else
all: dwm
endif

.c.o:
	${CC} -c ${CFLAGS} $<

${OBJ}: config.h config.mk patches.h

config.h:
	cp config.def.h $@

patches.h:
	cp patches.def.h $@

dwm: ${OBJ}
	${CC} -o $@ ${OBJ} ${LDFLAGS}

ifdef YAJLLIBS
dwm-msg:
	${CC} -o $@ patch/ipc/dwm-msg.c ${LDFLAGS}
endif

clean:
	rm -f dwm ${OBJ} dwm-${VERSION}.tar.gz
	rm -f dwm-msg

dist: clean
	mkdir -p dwm-${VERSION}
	cp -R LICENSE Makefile README config.def.h config.mk\
		dwm.1 drw.h util.h ${SRC} dwm.png transient.c dwm-${VERSION}
	tar -cf dwm-${VERSION}.tar dwm-${VERSION}
	gzip dwm-${VERSION}.tar
	rm -rf dwm-${VERSION}

install: all
	mkdir -p ${DESTDIR}${PREFIX}/bin
	cp -f dwm ${DESTDIR}${PREFIX}/bin
ifdef YAJLLIBS
	cp -f dwm-msg ${DESTDIR}${PREFIX}/bin
endif
	#cp -f patch/dwmc ${DESTDIR}${PREFIX}/bin
	chmod 755 ${DESTDIR}${PREFIX}/bin/dwm
ifdef YAJLLIBS
	chmod 755 ${DESTDIR}${PREFIX}/bin/dwm-msg
endif
	mkdir -p ${DESTDIR}${MANPREFIX}/man1
	sed "s/VERSION/${VERSION}/g" < dwm.1 > ${DESTDIR}${MANPREFIX}/man1/dwm.1
	chmod 644 ${DESTDIR}${MANPREFIX}/man1/dwm.1
	mkdir -p ${DESTDIR}${PREFIX}/share/xsessions
	test -f ${DESTDIR}${PREFIX}/share/xsessions/dwm.desktop || cp -n dwm.desktop ${DESTDIR}${PREFIX}/share/xsessions
	chmod 644 ${DESTDIR}${PREFIX}/share/xsessions/dwm.desktop

# Only install the wiki if 'nowiki' is not passed
ifeq ($(nowiki),)
	mkdir -p ${USER_HOME}/.wiki
	@for file in wiki.page/*; do \
		cp -r $$file ${USER_HOME}/.wiki/; \
	done
	chmod -R 777 ${USER_HOME}/.wiki
endif

uninstall:
	rm -f ${DESTDIR}${PREFIX}/bin/dwm\
		${DESTDIR}${MANPREFIX}/man1/dwm.1\
		${DESTDIR}${PREFIX}/share/xsessions/dwm.desktop
	rm -rf ${USER_HOME}/.wiki

.PHONY: all clean dist install uninstall
