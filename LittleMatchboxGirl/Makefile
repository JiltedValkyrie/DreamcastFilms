# The Little Match Girl: host test, Dreamcast program, disc image.
#   python tools/fetch_deps.py     first: fetches the two libraries into deps/
#   make test                      host test of the film's tables (any C compiler)
#   make [CDI=build/name.cdi]      the program and the image (KallistiOS environment sourced)
# Nothing is replaced: an image that exists is refused (give CDI a new name).
CC       ?= cc
DC_CC    ?= kos-cc
MKDCDISC ?= mkdcdisc
# The two libraries, as tools/fetch_deps.py fetches them; set either to a checkout of your own.
SH4DER   ?= deps/SH4DER-PVR
SH4ZAM   ?= deps/sh4zam
BUILD     = build
CDI      ?= $(BUILD)/little-match-girl.cdi
# The disc files the tools wrote (sound, subtitles, credits, title card); the image is made without them when the folder is not there.
DISC     ?= $(BUILD)/disc
# The library sources the program links: the spark pools, the falling snow, the frame texture.
LIB_SRC   = $(SH4DER)/src/sh4der_spark.c $(SH4DER)/src/sh4der_motes.c $(SH4DER)/src/sh4der_ca.c
DC_FLAGS  = -O3 -Wall -Wextra -Werror -I$(SH4DER)/include -I$(SH4DER)/sh4dow-dc/include -I$(SH4ZAM)/include -ffast-math -ffp-contract=fast -mfsrra -mfsca -fno-math-errno

.PHONY: all test
all: $(CDI)

need-sh4der:
	@test -e "$(SH4DER)/include/sh4der_core.h" || { echo "no SH4DER-PVR at $(SH4DER): run python tools/fetch_deps.py, or set SH4DER to your checkout"; exit 1; }

test: need-sh4der
	@mkdir -p $(BUILD)
	$(CC) -O2 -std=gnu11 -Wall -Wextra -Werror -DSH4DER_CORE_NO_SH4ZAM -I$(SH4DER)/include -I$(SH4DER)/sh4dow-dc/include test/matchlight_scene_test.c -lm -o $(BUILD)/matchlight_scene_test
	$(BUILD)/matchlight_scene_test

$(BUILD)/matchlight.elf: matchlight.c matchlight_scene.h | need-sh4der
	@test -e "$(SH4ZAM)/include" || { echo "no SH4ZAM at $(SH4ZAM): run python tools/fetch_deps.py, or set SH4ZAM to your checkout"; exit 1; }
	@mkdir -p $(BUILD)
	$(DC_CC) $(DC_FLAGS) matchlight.c $(LIB_SRC) -o $@

$(CDI): $(BUILD)/matchlight.elf
	@test ! -e "$@" || { echo "refuse existing image: $@"; exit 1; }
	$(MKDCDISC) -e $< -o $@ -N -n "LITTLE MATCH GIRL" $(if $(wildcard $(DISC)),-D $(DISC))
