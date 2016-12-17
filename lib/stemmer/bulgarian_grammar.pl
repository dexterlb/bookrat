article("а").
article("ът").
article("я").
article("ят").
article("та").
article("то").
article("те").

plural("и").
plural("ове").
plural("а").
plural("ци").
plural("ета").
plural("я").

adjective("на").
adjective("а").
adjective("но").
adjective("о").
adjective("ни").
adjective("и").

present_tense("иш").
present_tense("и").
present_tense("им").
present_tense("ите").
present_tense("ят").

present_tense("еш").
present_tense("е").
present_tense("ем").
present_tense("ете").

present_tense("аш").
present_tense("а").
present_tense("аме").
present_tense("ате").
present_tense("ат").

present_tense("яш").
present_tense("я").
present_tense("яме").
present_tense("яте").

past_simple_tense("ох").
past_simple_tense("е").
past_simple_tense("охме").
past_simple_tense("охте").
past_simple_tense("оха").

past_simple_tense("их").
past_simple_tense("и").
past_simple_tense("ихме").
past_simple_tense("ихте").
past_simple_tense("иха").

past_simple_tense("ах").
past_simple_tense("а").
past_simple_tense("ахме").
past_simple_tense("ахте").
past_simple_tense("аха").

past_simple_tense("ях").
past_simple_tense("я").
past_simple_tense("яхме").
past_simple_tense("яхте").
past_simple_tense("яха").

past_simple_tense("дох").
past_simple_tense("де").
past_simple_tense("дохме").
past_simple_tense("дохте").
past_simple_tense("доха").

past_continous_tense("ях").
past_continous_tense("еше").
past_continous_tense("яхме").
past_continous_tense("яхте").
past_continous_tense("яха").

past_continous_tense("ех").
past_continous_tense("ехме").
past_continous_tense("ехте").
past_continous_tense("еха").

past_continous_tense("аше").
past_continous_tense("яше").

past_undefied_tense("л").
past_undefied_tense("ла").
past_undefied_tense("ло").
past_undefied_tense("ли").

past_undefied_tense("сал").
past_undefied_tense("сала").
past_undefied_tense("сало").
past_undefied_tense("сали").

past_undefied_tense("ял").
past_undefied_tense("яла").
past_undefied_tense("яло").
past_undefied_tense("яли").

past_undefied_tense("ил").
past_undefied_tense("ила").
past_undefied_tense("ило").
past_undefied_tense("или").

past_undefied_tense("шъл").
past_undefied_tense("шла").
past_undefied_tense("шло").
past_undefied_tense("шли").

article_base(X, A) :- atom_concat(A, B, X), article(B), base(A).

plural_base(X, A) :- atom_concat(A, B, X), plural(B), base(A).
plural_base(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "а", C), base(C).
plural_base(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "о", C), base(C).
plural_base(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "к", C), base(C).
plural_base(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "е", C), base(C).
plural_base(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "й", C), base(C).
plural_base(X, C) :- atom_concat(A, B, X), plural(B), atom_concat(A, "я", C), base(C).

adjective_base(X, A) :- atom_concat(A, B, X), adjective(B), base(A).
adjective_base(X, C) :- atom_concat(A, B, X), adjective(B), atom_concat(A, "ен", C), base(C).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "я", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "я", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "я", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "я", C), base(C).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "а", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "а", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "а", C), base(C).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "ам", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "ам", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "ам", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "ам", C), base(C).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "ям", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "ям", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "ям", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "ям", C), base(C).

verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "та", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "ша", C), base(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "вам", C), base(C).

base_of(X, X) :- base(X).

base_of(X, A) :- article_base(X, A).
base_of(X, A) :- plural_base(X, A).
base_of(X, A) :- adjective_base(X, A).
base_of(X, A) :- verb_base(X, A).

base_of(X, C) :- atom_concat(A, B, X), article(B), plural_base(A, C). 
base_of(X, A) :- atom_concat(A, B, X), article(B), verb_base(A, C). 

base_of(X, X).

bases_of(L, R) :- maplist(base_of, L, R).
