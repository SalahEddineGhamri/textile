# textile
Helper to learn sturdy german texts and extract vocabulary
it show case grammer cases and help you remember the rules
while reading the text

# roadmap
- input a text from a txt file
- analyze text for what is available "article"
- define a color scheme
- give all article colors
- show the text in text widget
- make articles csv complete

# dependencies
- pip3 install pandas
- pip3 install spacy
- python3 -m spacy download de_core_news_sm
- pip3 install pandarallel
- pretty is used to print in python
- TUI is using Textual

"""
Categories
    GENDER
        masc     Masculine
        fem      Feminine
        neut     Neutral
        noGender No gender. Not exactly a gender indeed, rather a derivational property
    NUMERUS
        sing     Singular
        plu      Plural
    CASE
        nom      Nominative
        acc      Accusative
        dat      Dative
        gen      Genitive
    PERSON
        1per     First person
        2per     Second person
        3per     Third person
    TENSE
        pres     Simple present, Präsens
        ppres    Present participle, Partizip I (Partizip Präsens)
        past     Simple past, Preterite (Präteritum/Imperfekt)
        ppast    past perfect, Partizip II (Partizip Perfekt)
    MODE
        imp      Imperative
        ind      Indicative
        subj     Subjunctive
    INFLECTION
        inf      Infinitive
        zu       Infinitive with zu, e.g. umzugehen
    DEGREE
        pos      Positive, base form for adjectives
        comp     Comparative form for adjectives
        sup      Superlative form for adjectives
    ORTO
        old      Old, now unused Dativ
        short    shortened forms for  Dativ/Akkusativ e.g. dem Mensch <- dem Menschen
    STARKE
        strong   Strong inflection
        weak     Weak inflection
    CATEGORY
        V        Verb
        ADJ      Adjective
        ADV      Adverb
        ART      Article
        CARD     Cardinal number
        CIRCP    Zirkumposition rechts, please consult tag manual
        CONJ     Conjunction
        DEMO     Demonstrative
        INDEF    Indefinite pronoun
        INTJ     Interjection
        ORD      Ordinal number
        NN       Noun
        NNP      Proper noun
        POSS     Possesive
        POSTP    Postposiiton
        PRP      Personal pronoun
        PREP     Preposition
        PREPART  Preposition with incorporated article
        PROADV   Pronominal adverb
        PRTKL    Particle 
        REL      Relative pronoun
        TRUNC    Kompositions-Erstglied
        VPART    Verb particle
        WPADV    Adverbial interrogative pronoun
        WPRO     Interrogative pronoun
        ZU       Zu for infinitive, zu [gehen]
    ADDITIONAL ATTRIBUTES
        <mod>    Modal verbs
        <aux>    Auxiliary verbs
        <adv>    Adverbial used adjective
        <pred>   Predicative participle or adjective
        <ans>    Answers, ja bitte nein 
        <attr>   Attribute form for adjectives
        <adj>    Verbal particles of adjectival origin and particles
        <cmp>    Comparative form for conjunction
        <coord>  Coordinative form for conjunction
        <def>    Definite form for articles
        <indef>  Indefinite form for articles
        <noinfl> No inflection is possible
        <neg>    Negating form
        personal Personal pronoun
        <prfl>   Pronouns can be used both reflexive or non-reflexive
        <rec>    Reciprocal pronoun, einander
        <pro>    Pronominal use
        <refl>   Reflexive form
        <subord> Subordinate form
        <subst>  Substituierende form
"""
