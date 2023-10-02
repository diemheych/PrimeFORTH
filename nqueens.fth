8 constant rr
variable ii
variable ss
variable xx
variable yy
create aa rr 1 + allot
: rclaa @ aa + @ ;
: stoaa @ aa + ! ;

: NQPRINT
   1 II !
   BEGIN
     II RCLAA .
     1 II +!
   II @ XX @ 1 + = until
;

 : NQCORE
   0 SS !
   0 XX !
   BEGIN
     1 XX +!
     RR XX STOAA
     BEGIN
       1 SS +!
       XX @ YY !
       BEGIN YY @ DUP II ! 1 > IF
         -1 YY +!
         XX RCLAA YY RCLAA - DUP
         0 = SWAP ABS XX @ YY @ - = OR IF
           0 YY !
           BEGIN XX RCLAA 1 - DUP XX STOAA DUP 0 = IF
               -1 XX +!
             then
             0 <>
           UNTIL
         THEN
         THEN
         II @ 2 <
       UNTIL
     YY @ 1 = UNTIL
   RR XX @ = UNTIL
 ;

: NQUEENS
  NQCORE
  NQPRINT
;
