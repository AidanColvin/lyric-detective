# Function Flow 
Function flow for the lyric detective program

```mermaid
flowchart TD
    %% --- Node Definitions ---
    
    %% Top Level Script Functions
    main
    choose_file
    guess_author
    make_known_signatures
    _process_single_file
    find_closest_signature
    calculate_distance

    %% TextStats Class Methods
    TS_init[TextStats.__init__]
    TS_get_sig[TextStats.get_signature]
    TS_clean[TextStats._get_clean_words]
    
    TS_avg_word[TextStats.average_word_length]
    TS_diff[TextStats.different_to_total]
    TS_once[TextStats.exactly_once_to_total]
    TS_avg_sent[TextStats.average_sentence_length]
    TS_avg_complex[TextStats.average_sentence_complexity]

    %% Low Level Helpers
    clean_word
    split_into_sentences
    split_into_phrases
    split_string

    %% --- Connections (Logic Flow) ---

    %% Main Program Flow
    main --> choose_file
    main --> guess_author

    %% Guessing Logic
    guess_author --> TS_init
    guess_author --> TS_get_sig
    guess_author --> make_known_signatures
    guess_author --> find_closest_signature

    %% Signatures & Parallel Processing
    make_known_signatures --> _process_single_file
    _process_single_file --> TS_init
    _process_single_file --> TS_get_sig

    %% Comparison Logic
    find_closest_signature --> calculate_distance

    %% TextStats Initialization (Pre-calculation)
    TS_init --> split_into_sentences
    TS_init --> TS_clean
    TS_clean --> clean_word

    %% TextStats Signature Generation
    TS_get_sig --> TS_avg_word
    TS_get_sig --> TS_diff
    TS_get_sig --> TS_once
    TS_get_sig --> TS_avg_sent
    TS_get_sig --> TS_avg_complex

    %% Specific Metric Dependencies
    TS_avg_complex --> split_into_phrases

    %% Helper Function Dependencies
    split_into_sentences --> split_string
    split_into_phrases --> split_string
