flowchart TD
    %% --- Top Level Functions ---
    main
    choose_file
    guess_author
    make_known_signatures
    find_closest_signature
    calculate_distance
    _process_single_file

    %% --- TextStats Class Methods ---
    subgraph TextStats_Class [TextStats Class]
        TS_init[__init__]
        TS_get_sig[get_signature]
        TS_clean[_get_clean_words]
        
        %% Metrics
        TS_avg_word[average_word_length]
        TS_diff_total[different_to_total]
        TS_once_total[exactly_once_to_total]
        TS_avg_sent[average_sentence_length]
        TS_avg_complex[average_sentence_complexity]
    end

    %% --- Helper Functions ---
    clean_word
    split_into_sentences
    split_into_phrases
    split_string

    %% --- Logic Flow ---

    %% Main Execution
    main --> choose_file
    main --> guess_author

    %% Guessing Logic
    guess_author --> TS_init
    guess_author --> TS_get_sig
    guess_author --> make_known_signatures
    guess_author --> find_closest_signature

    %% Known Signatures Generation (Parallel)
    make_known_signatures --> _process_single_file
    _process_single_file --> TS_init
    _process_single_file --> TS_get_sig

    %% Comparison
    find_closest_signature --> calculate_distance

    %% --- TextStats Internal Flow ---
    
    %% Initialization (Pre-calculation)
    TS_init --> split_into_sentences
    TS_init --> TS_clean
    TS_clean --> clean_word

    %% Signature Gathering
    TS_get_sig --> TS_avg_word
    TS_get_sig --> TS_diff_total
    TS_get_sig --> TS_once_total
    TS_get_sig --> TS_avg_sent
    TS_get_sig --> TS_avg_complex

    %% Metric Calculations
    %% (Note: Most metrics now use pre-calculated data from __init__)
    TS_avg_complex --> split_into_phrases

    %% --- Helper Dependencies ---
    split_into_sentences --> split_string
    split_into_phrases --> split_string
