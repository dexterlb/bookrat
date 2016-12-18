male_article("а").
male_article("ът").
male_article("я").
male_article("ят").
male_article("то").
female_article("та").
middle_article("то").

plural_article("те").

article_base(X, A) :- atom_concat(A, B, X), male_article(B), male_noun(A).
article_base(X, A) :- atom_concat(A, B, X), female_article(B), female_noun(A).
article_base(X, A) :- atom_concat(A, B, X), middle_article(B), middle_noun(A).

% стол-ове
% бро/й - еве
% чайни/к-ци
% учител-и
% бинок/ъл - ли
% стол-а
% кон-я
% кон-е
% стади/й-и


% вкаменелост-и
% мас/а-и
% бирари/я -и

% дърв/о-ета
% цвет/е-я
% дърв/о-а
% бижу-та

male_plural("ове").
male_plural("eве").
male_plural("ли").
male_plural("ци").
male_plural("и").
male_plural("я").
male_plural("а").
male_plural("е").
male_plural("зи").

female_plural("и").

middle_plural("ета").
middle_plural("та").
middle_plural("а").
middle_plural("я").

plural_base(X, A) :- atom_concat(A, B, X), male_plural(B), male_noun(A).
plural_base(X, C) :- atom_concat(A, B, X), male_plural(B), atom_concat(A, "к", C), male_noun(C).
plural_base(X, C) :- atom_concat(A, B, X), male_plural(B), atom_concat(A, "г", C), male_noun(C).
plural_base(X, C) :- atom_concat(A, B, X), male_plural(B), atom_concat(A, "й", C), male_noun(C).
plural_base(X, C) :- atom_concat(A, B, X), male_plural(B), atom_concat(A, "ъл", C), male_noun(C).

plural_base(X, A) :- atom_concat(A, B, X), female_plural(B), female_noun(A).
plural_base(X, C) :- atom_concat(A, B, X), female_plural(B), atom_concat(A, "а", C), female_noun(C).
plural_base(X, C) :- atom_concat(A, B, X), female_plural(B), atom_concat(A, "я", C), female_noun(C).

plural_base(X, A) :- atom_concat(A, B, X), middle_plural(B), middle_noun(A).
plural_base(X, C) :- atom_concat(A, B, X), middle_plural(B), atom_concat(A, "о", C), middle_noun(C).
plural_base(X, C) :- atom_concat(A, B, X), middle_plural(B), atom_concat(A, "е", C), middle_noun(C).

adjective_suffix("на").
adjective_suffix("а").
adjective_suffix("но").
adjective_suffix("о").
adjective_suffix("ни").
adjective_suffix("и").

adjective_base(X, A) :- atom_concat(A, B, X), adjective_suffix(B), adjective(A).
adjective_base(X, C) :- atom_concat(A, B, X), adjective_suffix(B), atom_concat(A, "ен", C), adjective(C).
adjective_base(X, C) :- atom_concat(A, B, X), adjective_suffix(B), atom_concat(A, "и", C), adjective(C).

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

not_empty(A) :- not((A = '')).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "я", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "я", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "я", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "я", C), not_empty(A), verb(C).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "а", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "а", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "а", C), not_empty(A), verb(C).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "ам", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "ам", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "ам", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "ам", C), not_empty(A), verb(C).

verb_base(X, C) :- atom_concat(A, B, X), present_tense(B), atom_concat(A, "ям", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_simple_tense(B), atom_concat(A, "ям", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_continous_tense(B), atom_concat(A, "ям", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "ям", C), not_empty(A), verb(C).

verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "та", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "ша", C), not_empty(A), verb(C).
verb_base(X, C) :- atom_concat(A, B, X), past_undefied_tense(B), atom_concat(A, "вам", C), not_empty(A), verb(C).

article_adjective("ият").
article_adjective("ата").
article_adjective("ото").
article_adjective("ите").
article_adjective("ният").
article_adjective("ната").
article_adjective("ните").
article_adjective("ното").

article_pronoun("то").

article_adjective_base(X, A) :- atom_concat(A, B, X), article_adjective(B), adjective(A).
article_adjective_base(X, A) :- atom_concat(A, B, X), article_pronoun(B), pronoun(A).
article_adjective_base(X, C) :- atom_concat(A, B, X), article_adjective(B), atom_concat(A, "ен", C), not_empty(A), adjective(C).

mix_base(X, C) :- atom_concat(A, B, X), plural_article(B), plural_base(A, C). 
mix_base(X, C) :- atom_concat(A, B, X), plural_article(B), exception(A, C). 
mix_base(X, C) :- atom_concat(A, B, X), female_article(B), exception(A, C).

% изклюения:
replace("етра", "етър"). 
replace("етри", "етър").

exception(X, C) :- atom_concat(A, B, X), replace(B, T), atom_concat(A, T, C). 
exception(X, C) :- atom_concat(C, "ка", X), male_noun(C).

base(X) :- male_noun(X).
base(X) :- female_noun(X).
base(X) :- middle_noun(X).
base(X) :- adjective(X).
base(X) :- pronoun(X).
base(X) :- verb(X).

base_of(X, X) :- base(X).
base_of(X, A) :- exception(X, A).
base_of(X, A) :- article_base(X, A).
base_of(X, A) :- mix_base(X, A).
base_of(X, A) :- plural_base(X, A).
base_of(X, A) :- adjective_base(X, A).
base_of(X, A) :- verb_base(X, A).
base_of(X, A) :- article_adjective_base(X, A).
base_of(X, X).

bases_of(L, R) :- maplist(base_of, L, R).