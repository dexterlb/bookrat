article("а").
article("ът").
article("я").
article("ят").
article("ът").
article("ра").
article("та").
article("то").
article("те").

plural("и").
plural("ри").
plural("ци").
plural("е").
plural("я").
plural("ите").
plural("ета").
plural("ове").
plural("етата").
plural("а").


verb("е").
verb("а").
verb("и").
verb("ем").
verb("им").
verb("аме").
verb("аш").
verb("еш").
verb("иш").
verb("ете").
verb("ите").
verb("ате").
verb("ва").

verb("ил").
verb("ел").
verb("ал").
verb("ъл").

verb("их").
verb("ех").
verb("ил").
verb("ел").
verb("н").
verb("ен").
verb("ан").
verb("ещ").
verb("тох").
verb("дох").
verb("айки").
verb("ейки").


verb("ла").
verb("ела").
verb("ала").
verb("ила").
verb("ела").
verb("на").
verb("ена").
verb("ана").
verb("еща").

verb("тохме").
verb("тоха").

verb("оха").
verb("охме").

verb("дох").
verb("дохме").
verb("доха").

verb("айки").
verb("ейки").

verb("ло").
verb("ело").
verb("ало").
verb("ило").
verb("ело").
verb("но").
verb("ено").
verb("ано").
verb("ещо").


verb("ъл").
verb("ли").

base_of(X, X) :- base(X).

base_of(X, C) :- atom_concat(A, B, X), article(B), atom_concat(C, D, A), base(C), plural(D).
base_of(X, C) :- atom_concat(A, B, X), article(B), atom_concat(A, "ър", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "о", C), base(C).

base_of(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "а", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "к", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "е", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "ър", C), base(C).
base_of(X, A) :- atom_concat(A, B, X), plural(B), base(A).

base_of(X, C) :- atom_concat(A, B, X), verb(B), atom_concat(A, "а", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), verb(B), atom_concat(A, "я", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), verb(B), atom_concat(A, "ам", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), verb(B), atom_concat(A, "м", C), base(C).
base_of(X, C) :- atom_concat(A, B, X), verb(B), atom_concat(A, "вам", C), base(C).



base_of(X, A) :- atom_concat(A, B, X), article(B), base(A).

base_of(X, X).

bases_of(L, R) :- maplist(base_of, L, R).
