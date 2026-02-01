flowchart TD
    %% --- Top Level Functions ---
    main
    choose_file
    guess_author
    make_known_signatures
    _process_single_file
    find_closest_signature
    calculate_distance

    %% --- TextStats Class Methods ---
    %% These replace the old standalone calculation functions
    TextStats_init[TextStats.__init__]
    TextStats_get_signature[TextStats.get_signature]
    
    TextStats_clean_words[TextStats._get_clean_words]
    TextStats_avg_word[TextStats.average_word_length]
    TextStats_diff_total[TextStats.different_to_total]
    TextStats_once_total[TextStats.exactly_once_to_total]
    TextStats_avg_sent[TextStats.average_sentence_length]
    TextStats_avg_complex[TextStats.average_sentence_complexity]

    %% --- Low Level Helpers ---
    clean_word
    split_into_sentences
    split_into_phrases
    split_string

    %% --- Flow Connections ---

    %% Main Execution
    main --> choose_file
    main --> guess_author

    %% Guessing Logic
    guess_author --> TextStats_init
    guess_author --> TextStats_get_signature
    guess_author --> make_known_signatures
    guess_author --> find_closest_signature

    %% Known Signatures (Parallel Processing)
    make_known_signatures --> _process_single_file
    _process_single_file --> TextStats_init
    _process_single_file --> TextStats_get_signature

    %% Comparison
    find_closest_signature --> calculate_distance

    %% --- Inside TextStats Logic ---
    
    %% Initialization (Optimization: calculate lists once)
    TextStats_init --> split_into_sentences
    TextStats_init --> TextStats_clean_words
    TextStats_clean_words --> clean_word

    %% Getting the Signature (calls all metrics)
    TextStats_get_signature --> TextStats_avg_word
    TextStats_get_signature --> TextStats_diff_total
    TextStats_get_signature --> TextStats_once_total
    TextStats_get_signature --> TextStats_avg_sent
    TextStats_get_signature --> TextStats_avg_complex

    %% Metric Dependencies
    %% (Note: Most now use the pre-calculated lists from init)
    TextStats_avg_complex --> split_into_phrases

    %% Low Level Dependencies
    split_into_sentences --> split_string
    split_into_phrases --> split_string
