
.PHONY: default
default:
	$(error try `make install THEME=xcore-vector PREFIX=/usr/share/icons´ or `PREFIX=~/.icons´)

.PHONY: install
install: $(PREFIX)/$(THEME)/index.theme

FILENAMES = \
arrow \
based_arrow_down \
based_arrow_up \
boat \
bogosity \
bottom_left_corner \
bottom_right_corner \
bottom_side \
bottom_tee \
box_spiral \
center_ptr \
circle \
clock \
coffee_mug \
cross \
crosshair \
cross_reverse \
diamond_cross \
dot \
dotbox \
double_arrow \
draft_large \
draft_small \
draped_box \
exchange \
fleur \
gobbler \
gumby \
hand1 \
hand2 \
heart \
icon \
iron_cross \
leftbutton \
left_ptr \
left_side \
left_tee \
ll_angle \
lr_angle \
man \
middlebutton \
mouse \
pencil \
pirate \
plus \
question_arrow \
rightbutton \
right_ptr \
right_side \
right_tee \
rtl_logo \
sailboat \
sb_down_arrow \
sb_h_double_arrow \
sb_left_arrow \
sb_right_arrow \
sb_up_arrow \
sb_v_double_arrow \
shuttle \
sizing \
spider \
spraycan \
star \
target \
tcross \
top_left_arrow \
top_left_corner \
top_right_corner \
top_side \
top_tee \
trek \
ul_angle \
umbrella \
ur_angle \
watch \
X_cursor \
xterm

LINKNAMES = all-scroll \
cell \
col-resize \
default \
ew-resize \
grabbing \
help \
move \
not-allowed \
ns-resize \
pointer \
progress \
row-resize \
text \
wait


TARGET_FILES = $(foreach name,$(FILENAMES),$(PREFIX)/$(THEME)/cursors/$(name))
TARGET_LINKS = $(foreach name,$(LINKNAMES),$(PREFIX)/$(THEME)/cursors/$(name))


$(PREFIX)/$(THEME)/index.theme: $(TARGET_FILES) $(TARGET_LINKS)

$(TARGET_FILES): $(PREFIX)/%: %
	cp --no-preserve=ownership $< $@

$(TARGET_LINKS): $(PREFIX)/%: %
	ln -snf $$(readlink $<) $@
