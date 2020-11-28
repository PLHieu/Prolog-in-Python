female(queen_elizabethII).

married(queen_elizabethII, prince_philip).
married(prince_philip,queen_elizabethII).


parent(queen_elizabethII, prince_charles).
parent(prince_philip, prince_charles).
parent(queen_elizabethII, prince_andrew).
parent(prince_philip, prince_andrew).
parent(queen_elizabethII, princess_anne).
parent(prince_philip, princess_anne).
parent(queen_elizabethII, prince_edward).
parent(prince_philip, prince_edward).

father(Parent,Child) :- parent(Parent,Child), male(Parent).
mother(Parent,Child) :- parent(Parent,Child), female(Parent).