variable snake-x-head
500 cells allot

variable snake-y-head
500 cells allot

variable apple-x
variable apple-y

0 constant left
1 constant up
2 constant right
3 constant down

80 constant width
60 constant height

variable direction
variable length

: snake-x
  cells snake-x-head + ;

: snake-y
  cells snake-y-head + ;

: convert-x-y 24 cells * + ;
: draw pixon4 ;
: draw-black 0 col draw ;
: draw-white 16777215 col draw ;
: draw-red 16711680 col draw ;

: draw-walls
  width 0 do
    i 0 draw-black
    i height 1 - draw-black
  loop
  height 0 do
    0 i draw-black
    width 1 - i draw-black
  loop ;

: initialize-snake
  4 length !
  length @ 1 + 0 do
    12 i - i snake-x !
    12 i snake-y !
  loop
  down direction ! ;

: set-apple-position apple-x ! apple-y ! ;

: initialize-apple 50 50 set-apple-position ;

: initialize
  width 0 do
    height 0 do
      j i draw-white
    loop
  loop
  draw-walls
  initialize-snake
  initialize-apple ;

: move-up  -1 snake-y-head +! ;
: move-left  -1 snake-x-head +! ;
: move-down  1 snake-y-head +! ;
: move-right  1 snake-x-head +! ;

: move-snake-head  direction @
  left over  = if move-left else
  up over    = if move-up else
  right over = if move-right else
  down over  = if move-down
  then then then then drop ;

: move-snake-tail  0 length @ do
    i snake-x @ i 1 + snake-x !
    i snake-y @ i 1 + snake-y !
  -1 +loop ;

: is-horizontal  direction @ dup
  left = swap
  right = or ;

: is-vertical  direction @ dup
  up = swap
  down = or ;

: turn-up     is-horizontal if up direction ! then ;
: turn-left   is-vertical if left direction ! then ;
: turn-down   is-horizontal if down direction ! then ;
: turn-right  is-vertical if right direction ! then ;

: change-direction
  7 over = if turn-left else
  2 over = if turn-up else
  8 over = if turn-right else
  12 over = if turn-down
  then then then then drop ;

: check-input
  lastkey change-direction
  ;

: random-position 
  height 4 - random 2 +
  width 4 - random 2 + ;

: move-apple
  apple-x @ apple-y @ draw-white
  random-position
  set-apple-position ;

: grow-snake  1 length +! ;

: check-apple
  snake-x-head @ apple-x @ =
  snake-y-head @ apple-y @ =
  and if
    move-apple
    grow-snake
  then ;

: check-collision
  snake-x-head @ snake-y-head @

  getpix4

  0 = ;

: draw-snake
  length @ 0 do
    i snake-x @ i snake-y @ draw-black
  loop
  length @ snake-x @
  length @ snake-y @
  draw-white ;

: draw-apple
  apple-x @ apple-y @ draw-red ;


: game-loop
  begin
    draw-snake
    draw-apple
    50 length @ - dup 0< if drop 5 then sleep
    check-input
    move-snake-tail
    move-snake-head
    check-apple
    check-collision
  until ;

: snake cls initialize game-loop length @ . ;
