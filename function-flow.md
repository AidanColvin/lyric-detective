flowchart TD
    %% --- Top Level Script Functions ---
    main
    choose_file
    guess_author
    make_known_signatures
    _process_single_file
    find_closest_signature
    calculate_distance

    %% --- TextStats Class Methods ---
    subgraph TextStats_Class [TextStats Class]
        direction TB
        init[__init__]
        get_sig[get_signature]
        _get_clean[_get_clean_words]
        
        %% Metrics
        avg_word[average_word_length]
        diff_total[different_to_total]
        once_total[exactly_once_to_total]
        avg_sent[average_sentence_length]
        avg_complex[average_sentence_complexity]
    end

    %% --- Low Level Utilities ---
    clean_word
    split_into_sentences
    split_into_phrases
    split_string

    %% --- Execution Flow ---
    
    %% Main Entry
    main --> choose_file
    main --> guess_author

    %% Analyzing the Unknown File
    guess_author --> init
    guess_author --> get_sig
    guess_author --> make_known_signatures
    guess_author --> find_closest_signature

    %% Building Known Signatures (Parallel)
    make_known_signatures --> _process_single_file
    _process_single_file --> init
    _process_single_file --> get_sig

    %% The Comparison
    find_closest_signature --> calculate_distance

    %% --- Inside TextStats Class ---
    
    %% Initialization (The "Once" Logic)
    init --> split_into_sentences
    init --> _get_clean
    _get_clean --> clean_word

    %% Signature Generation calls all metrics
    get_sig --> avg_word
    get_sig --> diff_total
    get_sig --> once_total
    get_sig --> avg_sent
    get_sig --> avg_complex

    %% Complexity metric needs phrase splitting
    avg_complex --> split_into_phrases

    %% --- Utility Dependencies ---
    split_into_sentences --> split_string
    split_into_phrases --> split_string
