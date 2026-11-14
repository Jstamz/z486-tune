CPU_DIR := ../../..
OBJ_DIR := boards/common/sim/build/obj_dir
RUN_DIR := build/run
TOP := tb_z486_led_demo

VERILATOR ?= verilator
VFLAGS := --binary --timing -Wall -Wno-fatal -Wno-UNOPTFLAT
VFLAGS += -Wno-SYNCASYNCNET -Wno-PINCONNECTEMPTY -Wno-DECLFILENAME
VFLAGS += -Wno-TIMESCALEMOD
VFLAGS += -Irtl -Irtl/x87 -f boards/common/rtl_sources.f

.PHONY: all firmware build run clean

all: run

firmware:
	$(MAKE) -C ../../firmware

build: firmware
	mkdir -p build/obj_dir
	cd $(CPU_DIR) && $(VERILATOR) $(VFLAGS) --Mdir $(OBJ_DIR) \
		--top-module $(TOP) boards/common/sim/$(TOP).sv

# ROM images use bare names; the firmware path is repository-relative.
run: build
	mkdir -p $(RUN_DIR)/boards/firmware
	cp $(CPU_DIR)/src/ucode.hex $(CPU_DIR)/src/pla_entry_rom.hex \
		$(CPU_DIR)/src/pla_group_entry.hex $(CPU_DIR)/src/x87/x87_ucode.mem \
		$(RUN_DIR)/
	cp $(CPU_DIR)/boards/firmware/blink.hex $(RUN_DIR)/boards/firmware/
	cd $(RUN_DIR) && ../obj_dir/V$(TOP)

clean:
	rm -rf build
