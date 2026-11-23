
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

LINKNAMES = 00008160000006810000408080010102 \
028006030e0e7ebffc7f7070c0600140 \
08e8e1c95fe2fc01f976f1e063a24ccd \
14fef782d02440884392942c11205230 \
2870a09082c103050810ffdffffe0204 \
5c6cd98b3f3ebcb1f9c7f1c204630408 \
9d800788f1b08800ae810202380a0822 \
all-scroll \
cell \
col-resize \
d9ce0ab605698f320427677b458ad60b \
default \
dot_box_mask \
e29285e634086352946a0e7090d73106 \
e-resize \
ew-resize \
fcf1c3c7cd4491d801f1e1c78f100000 \
grabbing \
hand \
h_double_arrow \
help \
move \
ne-resize \
not-allowed \
n-resize \
ns-resize \
nw-resize \
pointer \
pointing_hand \
progress \
row-resize \
se-resize \
size_all \
size_hor \
size_ver \
s-resize \
sw-resize \
text \
v_double_arrow \
wait \
w-resize



TARGET_FILES = $(foreach name,$(FILENAMES),$(PREFIX)/$(THEME)/cursors/$(name))
TARGET_LINKS = $(foreach name,$(LINKNAMES),$(PREFIX)/$(THEME)/cursors/$(name))


$(PREFIX)/$(THEME)/index.theme: $(TARGET_FILES) $(TARGET_LINKS)

$(TARGET_FILES): $(PREFIX)/%: %
	cp --no-preserve=ownership $< $@

$(TARGET_LINKS): $(PREFIX)/%: %
	ln -snf $$(readlink $<) $@
