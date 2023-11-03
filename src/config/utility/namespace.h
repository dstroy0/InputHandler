/**
 * @file namespace.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief InputHandler specific namespaces
 * @version 1.0.0
 * @date 2023-02-13
 *
 * @copyright Copyright (c) 2023
 */
/*
 * Copyright (c) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
 *
 * License: GNU GPL3
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 3 as published by the Free Software Foundation.
 */

#if !defined(__IH_NAMESPACES__)
    #define __IH_NAMESPACES__

/**
 * @defgroup namespaces Namespaces
 * @{
 */
/**
 * @brief InputHandler "auto" type namespace
 *
 * The source of macros in this namespace is src/config.h.
 * [config src](https://github.com/dstroy0/InputHandler/blob/main/src/config/config.h)
 * [namespace
 * src](https://github.com/dstroy0/InputHandler/blob/main/src/config/noedit.h#:~:text=namespace%20IH)
 *
 *
 * The idea behind this namespace is to let users set config.h items to
 * whatever they want, sizing variables for the least amount of space, automatically.
 * The preprocessor evaluates the if macros in a way that will leave typedefs that
 * size type aliases to the minimum byte-width required automatically.  It also warns users
 * about the change.  The only hand-holding that happens is for type sizing, it's up
 * to you to make sure you have the resources for your settings.
 * Convenience namespace.
 *
 * @namespace ih_auto
 */
namespace ih_auto
{
// Input private member type (future bit array)
typedef bool type_match_flags; ///< Input private member type (future bit array)

// Input variable sizing
    #if (IH_MAX_COMMANDS_PER_TREE <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_COMMANDS_PER_TREE @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_COMMANDS_PER_TREE <= UINT8_MAX)
 * typedef uint8_t max_cmds_per_tree;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT8_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT16_MAX)
 * typedef uint16_t max_cmds_per_tree;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT16_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT32_MAX)
 * typedef uint32_t max_cmds_per_tree;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_cmds_per_tree;

/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_COMMANDS_PER_TREE @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_COMMANDS_PER_TREE <= UINT8_MAX)
 * typedef uint8_t cmd_id_grp;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT8_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT16_MAX)
 * typedef uint16_t cmd_id_grp;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT16_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT32_MAX)
 * typedef uint32_t cmd_id_grp;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t cmd_id_grp;
    #elif (IH_MAX_COMMANDS_PER_TREE > UINT8_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT16_MAX)
typedef uint16_t max_cmds_per_tree;
typedef uint16_t cmd_id_grp;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_COMMANDS_PER_TREE|max_cmds_per_tree, cmd_id_grp changed from uint8_t to uint16_t
    #elif (IH_MAX_COMMANDS_PER_TREE > UINT16_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT32_MAX)
typedef uint32_t max_cmds_per_tree;
typedef uint32_t cmd_id_grp;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_COMMANDS_PER_TREE|max_cmds_per_tree, cmd_id_grp changed from uint8_t to uint32_t
    #elif (IH_MAX_COMMANDS_PER_TREE > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_COMMANDS_PER_TREE greater than UINT32_MAX; behavior undefined, compilation should fail.
    #endif // end IH_MAX_COMMANDS_PER_TREE

    #if (IH_MAX_ARGS_PER_COMMAND <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_ARGS_PER_COMMAND @endlink is set by the user.
 * @code{.c}
 * #if (IH_MAX_ARGS_PER_COMMAND <= UINT8_MAX)
 * typedef uint8_t max_args_per_cmd;
 * #elif (IH_MAX_ARGS_PER_COMMAND > UINT8_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT16_MAX)
 * typedef uint16_t max_args_per_cmd;
 * #elif (IH_MAX_ARGS_PER_COMMAND > UINT16_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT32_MAX)
 * typedef uint32_t max_args_per_cmd;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_args_per_cmd;
    #elif (IH_MAX_ARGS_PER_COMMAND > UINT8_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT16_MAX)
typedef uint16_t max_args_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_ARGS_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint16_t
    #elif (IH_MAX_ARGS_PER_COMMAND > UINT16_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT32_MAX)
typedef uint32_t max_args_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_ARGS_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint32_t
    #elif IH_MAX_ARGS_PER_COMMAND > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #warning IH_MAX_ARGS_PER_COMMAND greater than UINT32_MAX; behavior undefined, compilation should fail.
    #endif // end IH_MAX_ARGS_PER_COMMAND

    #if (IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_TREE_DEPTH_PER_COMMAND @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT8_MAX)
 * typedef uint8_t max_tree_depth_per_cmd;
 * #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > UINT8_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT16_MAX)
 * typedef uint16_t max_tree_depth_per_cmd;
 * #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > UINT16_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT32_MAX)
 * typedef uint32_t max_tree_depth_per_cmd;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_tree_depth_per_cmd;
    #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > UINT8_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT16_MAX)
typedef uint16_t max_tree_depth_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_TREE_DEPTH_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint16_t
    #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > UINT16_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT32_MAX)
typedef uint32_t max_tree_depth_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_TREE_DEPTH_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint32_t
    #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_TREE_DEPTH_PER_COMMAND cannot be greater than UINT32_MAX
    #endif // end IH_MAX_TREE_DEPTH_PER_COMMAND

    #if (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT8_MAX)
 * typedef uint8_t max_num_child_cmds;
 * #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT8_MAX && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <=
 * UINT16_MAX) typedef uint16_t max_num_child_cmds; #elif
 * (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT16_MAX && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <=
 * UINT32_MAX) typedef uint32_t max_num_child_cmds; #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_num_child_cmds;
    #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT8_MAX && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT16_MAX)
typedef uint16_t max_num_child_cmds;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT|max_args_per_cmd changed from uint8_t to uint16_t
    #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT16_MAX && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT32_MAX)
typedef uint32_t max_num_child_cmds;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT|max_args_per_cmd changed from uint8_t to uint32_t
    #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT cannot be greater than UINT32_MAX
    #endif // end IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT

    #if (IH_MAX_CMD_STR_LEN <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_CMD_STR_LEN @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_CMD_STR_LEN <= UINT8_MAX)
 * typedef uint8_t max_cmd_str_len;
 * #elif (IH_MAX_CMD_STR_LEN > UINT8_MAX && IH_MAX_CMD_STR_LEN <= UINT16_MAX)
 * typedef uint16_t max_cmd_str_len;
 * #elif (IH_MAX_CMD_STR_LEN > UINT16_MAX && IH_MAX_CMD_STR_LEN <= UINT32_MAX)
 * typedef uint32_t max_cmd_str_len;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_cmd_str_len;
    #endif
    #if (IH_MAX_CMD_STR_LEN > UINT8_MAX && IH_MAX_CMD_STR_LEN <= UINT16_MAX)
typedef uint16_t max_cmd_str_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_CMD_STR_LEN|max_cmd_str_len changed from uint8_t to uint16_t
    #endif
    #if (IH_MAX_CMD_STR_LEN > UINT16_MAX && IH_MAX_CMD_STR_LEN <= UINT32_MAX)
typedef uint32_t max_cmd_str_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_CMD_STR_LEN|max_cmd_str_len changed from uint8_t to uint32_t
    #endif
    #if (IH_MAX_CMD_STR_LEN > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_CMD_STR_LEN cannot be greater than UINT32_MAX
    #endif // end IH_MAX_CMD_STR_LEN

    #if (IH_MAX_NUM_PROC_DELIM_SEQ <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_NUM_PROC_DELIM_SEQ @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_NUM_PROC_DELIM_SEQ <= UINT8_MAX)
 * typedef uint8_t max_num_delim_seq;
 * #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT8_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT16_MAX)
 * typedef uint16_t max_num_delim_seq;
 * #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT16_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT32_MAX)
 * typedef uint32_t max_num_delim_seq;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_num_delim_seq;
    #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT8_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT16_MAX)
typedef uint16_t max_num_delim_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_PROC_DELIM_SEQ|max_num_delim_seq changed from uint8_t to uint16_t
    #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT16_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT32_MAX)
typedef uint32_t max_num_delim_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_PROC_DELIM_SEQ|max_num_delim_seq changed from uint8_t to uint32_t
    #elif (IH_MAX_NUM_PROC_DELIM_SEQ > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_PROC_DELIM_SEQ cannot be greater than UINT32_MAX
    #endif // end IH_MAX_NUM_PROC_DELIM_SEQ

    #if (IH_MAX_NUM_START_STOP_SEQ <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_NUM_START_STOP_SEQ @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_NUM_START_STOP_SEQ <= UINT8_MAX)
 * typedef uint8_t max_num_start_stop_seq;
 * #elif (IH_MAX_NUM_START_STOP_SEQ > UINT8_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT16_MAX)
 * typedef uint16_t max_num_start_stop_seq;
 * #elif (IH_MAX_NUM_START_STOP_SEQ > UINT16_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT32_MAX)
 * typedef uint32_t max_num_start_stop_seq;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_num_start_stop_seq;
    #elif (IH_MAX_NUM_START_STOP_SEQ > UINT8_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT16_MAX)
typedef uint16_t max_num_start_stop_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_START_STOP_SEQ|max_num_start_stop_seq changed from uint8_t to uint16_t
    #elif (IH_MAX_NUM_START_STOP_SEQ > UINT16_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT32_MAX)
typedef uint32_t max_num_start_stop_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_START_STOP_SEQ|max_num_start_stop_seq changed from uint8_t to uint32_t
    #elif (IH_MAX_NUM_START_STOP_SEQ > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_START_STOP_SEQ cannot be greater than UINT32_MAX
    #endif // end IH_MAX_NUM_START_STOP_SEQ

    #if (IH_MAX_PROC_INPUT_LEN <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_PROC_INPUT_LEN @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_PROC_INPUT_LEN <= UINT8_MAX)
 * typedef uint8_t max_proc_input_len;
 * #elif (IH_MAX_PROC_INPUT_LEN > UINT8_MAX && IH_MAX_PROC_INPUT_LEN <= UINT16_MAX)
 * typedef uint16_t max_proc_input_len;
 * #elif (IH_MAX_PROC_INPUT_LEN > UINT16_MAX && IH_MAX_PROC_INPUT_LEN <= UINT32_MAX)
 * typedef uint32_t max_proc_input_len;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_proc_input_len;
    #elif (IH_MAX_PROC_INPUT_LEN > UINT8_MAX && IH_MAX_PROC_INPUT_LEN <= UINT16_MAX)
typedef uint16_t max_proc_input_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PROC_INPUT_LEN|max_proc_input_len changed from uint8_t to uint16_t
    #elif (IH_MAX_PROC_INPUT_LEN > UINT16_MAX && IH_MAX_PROC_INPUT_LEN <= UINT32_MAX)
typedef uint32_t max_proc_input_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PROC_INPUT_LEN|max_proc_input_len changed from uint8_t to uint32_t
    #elif (IH_MAX_PROC_INPUT_LEN > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PROC_INPUT_LEN cannot be greater than UINT32_MAX
    #endif // end IH_MAX_PROC_INPUT_LEN

    #if (IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_PER_ROOT_MEMCMP_RANGES @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT8_MAX)
 * typedef uint8_t max_per_root_memcmp_ranges;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT8_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT16_MAX)
 * typedef uint16_t max_per_root_memcmp_ranges;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT16_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT32_MAX)
 * typedef uint32_t max_per_root_memcmp_ranges;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_per_root_memcmp_ranges;

/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_PER_ROOT_MEMCMP_RANGES @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT8_MAX)
 * typedef uint8_t memcmp_idx_t;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT8_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT16_MAX)
 * typedef uint16_t memcmp_idx_t;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT16_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT32_MAX)
 * typedef uint32_t memcmp_idx_t;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t memcmp_idx_t;
    #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT8_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT16_MAX)
typedef uint16_t max_per_root_memcmp_ranges;
typedef uint16_t memcmp_idx_t;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PER_ROOT_MEMCMP_RANGES|max_per_root_memcmp_ranges, memcmp_idx_t changed from uint8_t to uint16_t
    #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT16_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT32_MAX)
typedef uint32_t max_per_root_memcmp_ranges;
typedef uint32_t memcmp_idx_t;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PER_ROOT_MEMCMP_RANGES|max_per_root_memcmp_ranges, memcmp_idx_t changed from uint8_t to uint32_t
    #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PER_ROOT_MEMCMP_RANGES cannot be greater than UINT32_MAX
    #endif // end IH_MAX_PER_ROOT_MEMCMP_RANGES
// end typedef sizing
} // end namespace IH

/**
 * @brief User facing namespace
 *
 * @namespace ih
 */
namespace ih
{
/**
 * @defgroup typedefs typedefs
 */
///@{
/**
 * @brief This is an alias for a char array.
 *
 * process_name[@link IH_PROCESS_NAME_PGM_LEN @endlink]
 *
 * To increase or decrease the pgm len of this array edit
 * @link IH_PROCESS_NAME_PGM_LEN @endlink in src/config/config.h.
 */
typedef char ProcessName[IH_PROCESS_NAME_PGM_LEN];

/**
 * @brief char array typedef.
 *
 * InputProcessEndOfLineChar[@link IH_EOL_SEQ_PGM_LEN @endlink]
 *
 * To increase or decrease the pgm len of this array edit
 * @link IH_EOL_SEQ_PGM_LEN @endlink in src/config/config.h.
 */
typedef char EndOfLineChar[IH_EOL_SEQ_PGM_LEN];

/**
 * @brief char array typedef.
 *
 * InputControlChar[@link IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN @endlink]
 *
 * To increase or decrease the pgm len of this array edit
 * @link IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN @endlink in src/config/config.h.
 */
typedef char ControlCharSeq[IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN];

/**
 * @brief char array typedef.
 *
 * InputWildcardChar[@link IH_WCC_SEQ_PGM_LEN @endlink]
 *
 * To increase or decrease the pgm len of this array edit
 * @link IH_WCC_SEQ_PGM_LEN @endlink in src/config/config.h.
 */
typedef char WildcardChar[IH_WCC_SEQ_PGM_LEN];
///@}

/**
 * @defgroup ENUMS ENUMS
 */
///@{
/**
 * @brief Command identifier enum.
 *
 * This is used to explicitly state something is related to a root command
 * in the context of CommandParameters.
 *
 * @enum CMD_ID
 */
enum CMD_ID
{
    root ///< this is the root command id, it's the number 0 ALWAYS
};

/**
 * @brief Command wildcard flag enum.
 *
 * These flags are used inside of CommandParameters.
 *
 * @enum WC_FLAG
 */
enum WC_FLAG
{
    no_wildcards = false, ///< this command has no wildcard char (false (0))
    has_wildcards = true ///< this command contains one or more wildcard char (true (1))
};

/**
 * @brief Input::\_compareCommandToString() return values.
 *
 * These flags are only used to provide clarity to Input::\_compareCommandToString(),
 * they make it easy to understand what is happening inside of that method.
 *
 * @enum UI_COMPARE
 */
enum UI_COMPARE
{
    no_match, ///< no match
    match_all_wcc_cmd, ///< match all wcc command
    match ///< match command
};

/**
 * @brief Strongly typed argument handling flags.
 *
 * This is used in CommandParameters as a visual reminder of
 * how the process will handle your arguments.
 * @enum UI_ARG_HANDLING
 */
enum class UI_ARG_HANDLING
{
    no_args, ///<  no arguments expected
    one_type, ///<  every argument is of the same type
    type_arr ///<  there is an array of input types
};

/**
 * @brief Input type specifier.
 *
 * These are the different types of user input the process can accept.
 * NOTYPE and START_STOP can be any 0-255 value.
 * This is strongly typed to help avoid name conflicts, and as an indicator that
 * these types are not built-in.
 * @enum UITYPE
 */
enum class UITYPE
{
    UINT8_T, ///<  8-bit unsigned integer
    UINT16_T, ///<  16-bit unsigned integer
    UINT32_T, ///<  32-bit unsigned integer
    INT16_T, ///<  16-bit signed integer
    FLOAT, ///<  32-bit float
    CHAR, ///<  8-bit char
    START_STOP, ///<  array of 8-bit char
    NOTYPE, ///<  no type validation
    NO_ARGS, ///<  no arguments expected
    _LAST ///<  reserved
};
///@}

/**
 * @defgroup structs structs
 */
///@{
/**
 * @brief Holds user defined input data delimiters.
 *
 * A delimiter sequence is a predefined number or set of numbers that is used to separate
 * input arguments, subcommands or data.  The input process needs to know three things
 * about the delimiter sequences you want to use.  The number of delimiter sequences there are
 * (up to @link IH_MAX_NUM_PROC_DELIM_SEQ @endlink), the 8-bit byte (char) length of each delimiter
 * sequence, and finally each delimiter sequence which can be up to @link IH_DELIM_SEQ_PGM_LEN
 * @endlink in length.
 */
struct DelimiterSequences
{
    size_t num_seq; ///< the number of token delimiters in delimiter_sequences
    ih_auto::max_num_delim_seq delimiter_lens[IH_MAX_NUM_PROC_DELIM_SEQ]; ///< delimiter sequence lens delimiter_lens
                                                                          ///< [@link IH_MAX_NUM_PROC_DELIM_SEQ @endlink]
    char delimiter_sequences[IH_MAX_NUM_PROC_DELIM_SEQ][IH_DELIM_SEQ_PGM_LEN]; ///< string-literal "" delimiter sequence array
                                                                               ///< delimiter_sequences
                                                                               ///< [@link IH_MAX_NUM_PROC_DELIM_SEQ @endlink]
                                                                               ///< [@link IH_DELIM_SEQ_PGM_LEN @endlink]
};

/**
 * @brief Holds regex-like start-stop match sequence pairs.
 *
 * A start-stop sequence is a pair of numbers or a pair of a set of numbers which do not have to
 * be identical to one another.  The "start" sequence demarcs the beginning of a chunk of data,
 * the "stop" sequence demarcs the end of the chunk of data. The input process needs to know
 * three things about the start-stop sequences you want to use.  The number of start-stop
 * sequences there are (up to @link IH_MAX_NUM_START_STOP_SEQ @endlink), the 8-bit byte (char)
 * length of each start-stop sequence, and finally each start-stop sequence which can be up to
 * @link IH_START_STOP_SEQ_PGM_LEN @endlink in length.
 */
struct StartStopSequences
{
    size_t num_seq; ///< num start/stop sequences
    ih_auto::max_num_start_stop_seq start_stop_sequence_lens[IH_MAX_NUM_START_STOP_SEQ]; ///< start stop sequence lens start_stop_sequence_lens
                                                                                         ///< [@link IH_MAX_NUM_START_STOP_SEQ @endlink]
    char start_stop_sequence_pairs[IH_MAX_NUM_START_STOP_SEQ][IH_START_STOP_SEQ_PGM_LEN]; ///< start/stop sequences.  Match
                                                                                          ///< start, match end, copy what is
                                                                                          ///< between markers start_stop_sequence_pairs
                                                                                          ///< [@link IH_MAX_NUM_START_STOP_SEQ @endlink]
                                                                                          ///< [@link IH_START_STOP_SEQ_PGM_LEN @endlink]
};

/**
 * @brief Input process parameters and constructor parameters.
 *
 * This struct is an array of pointers to other structs/arrays contained in PROGMEM.
 * It's required by the input process constructor, all together they define the
 * input process behavior.
 */
struct InputParameters
{
    const ProcessName* process_name; ///< this process' name, can be NULL; MAX len ==
                                     ///< @link IH_PROCESS_NAME_PGM_LEN @endlink
    const EndOfLineChar* eol_char; ///< end of line term; MAX len == @link IH_EOL_SEQ_PGM_LEN @endlink
    const ControlCharSeq* input_control_char_sequence; ///< two char len sequence to input a control char
    const WildcardChar* wildcard_char; ///< single char wildcard char
    const DelimiterSequences* delimiter_sequences; ///< reference to ih::DelimiterSequences struct
    const StartStopSequences* start_stop_sequences; ///< reference to ih::StartStopSequences struct
};

/**
 * @brief Contains arrays and indices determined at runtime.
 *
 * These structs are associated with wildcard commands; CommandParameters which
 * contains wildcards will have a CommandRuntimeCalc.
 */
struct CommandRuntimeCalc
{
    ih_auto::memcmp_idx_t num_prm_with_wc; ///< the number of CommandParameters structs in this command
                                           ///< that contain char(ih::WildcardChar[0]); the WildCard Character
    ih_auto::memcmp_idx_t* idx_of_prm_with_wc; ///< indices of CommandParameters struct that contain wcc
    ih_auto::max_per_root_memcmp_ranges* num_memcmp_ranges_this_row; ///< the number of memcmp ranges for this Parameters command
                                                                     ///< string, array members always an even number
    ih_auto::max_per_root_memcmp_ranges** memcmp_ranges_arr; ///< 2d array[row][col], each [row] is for one Parameters command string
                                                             ///< which contains wcc
};
// end group structs
///@}
};

/**
 * @brief library constants located in PROGMEM.
 *
 * This namespace's purpose is to avoid name collision
 * and to consolidate the library's PROGMEM variables.
 *
 * @namespace ihc
 */
namespace ihc
{
/**
 * @defgroup literals literals
 */
///@{
/**
 * @brief Type string literals.
 *
 * Input type string literal PROGMEM array, each of the types in @link ih::UITYPE @endlink has
 * a corresponding string literal for display purposes.
 *
 */
const char PROGMEM type_strings[10][IH_INPUT_TYPE_STRINGS_PGM_LEN] = {
    "UINT8_T", ///< 8-bit unsigned integer
    "UINT16_T", ///< 16-bit unsigned integer
    "UINT32_T", ///< 32-bit unsigned integer
    "INT16_T", ///< 16-bit signed integer
    "FLOAT", ///< 32-bit floating point number
    "CHAR", ///< single char
    "STARTSTOP", ///< c-string enclosed with start/stop delimiters
    "NOTYPE", ///< user defined NOTYPE
    "NO_ARGS", ///< no arguments expected
    "error" ///< error
};

// default constructor paramters
const ih::ProcessName PROGMEM _process_name = ""; ///< default process name is an empty string
const ih::EndOfLineChar PROGMEM _eol_char = "\r\n"; ///< default process eol characters CRLF
const ih::ControlCharSeq PROGMEM _input_control_char_sequence = "##"; ///< default process input control character sequence "##"
const ih::WildcardChar PROGMEM _wildcard_char = "*"; ///< default process wildcard char '*'

/**
 * @brief Default delimiter sequences.
 *
 */
const ih::DelimiterSequences PROGMEM _delimiter_sequences = {
    2, ///< number of delimiter sequences
    {1, 1}, ///< delimiter sequence lens
    {" ", ","} ///< delimiter sequences
};

/**
 * @brief Default start stop sequences.
 *
 */
const ih::StartStopSequences PROGMEM _start_stop_sequences = {
    1, ///< num start stop sequence pairs
    {1, 1}, ///< start stop sequence lens
    {"\"", "\""} ///< start stop sequence pair sequences
};

/**
 * @brief Input default ih::InputParameters.
 *
 */
const ih::InputParameters PROGMEM default_parameters = {
    &ihc::_process_name, ///< process name
    &ihc::_eol_char, ///< process eol term
    &ihc::_input_control_char_sequence, ///< process input control char sequence
    &ihc::_wildcard_char, ///< process wildcard char
    &ihc::_delimiter_sequences, ///< process default delimiter sequences
    &ihc::_start_stop_sequences ///< process default start/stop sequences
};

// messages

// error types
const char fatal_error[] PROGMEM = "FATAL ERROR! ";

// error types pointer array
const char* const error_type_strings[] PROGMEM = {
    fatal_error,
};

// error types pointer array convenience index
enum class ERR_TYP
{
    fatal_error,
};

// lib error messages
// fatal
const char fatal_halt[] PROGMEM = "%SINPUTHANDLER IS FUNCTIONALLY DISABLED.\n";
const char fatal_begin_not_set[] PROGMEM = "%SInput::begin() not set.\n";
const char fatal_allocation[] PROGMEM = "%Scouldn't allocate memory for %S.\n";
const char fatal_arr_alloc_idx[] PROGMEM = "%Scouldn't allocate memory for %S[%02u].\n";

// error message pointer array
const char* const error_message_strings[] PROGMEM = {
    fatal_halt,
    fatal_begin_not_set,
    fatal_allocation,
    fatal_arr_alloc_idx,
};

// error message pointer array convenience index
enum class ERR_MSG
{
    fatal_halt,
    fatal_begin_not_set,
    fatal_allocation,
    fatal_arr_alloc_idx,
};

    // var identifiers
    #if defined(__DEBUG_ADDCOMMAND__)
const char memcmp_idx[] PROGMEM = "memcmp_idx";
const char memcmp_ranges[] PROGMEM = "memcmp_ranges";
const char memcmp_ranges_arr[] PROGMEM = "memcmp_ranges_arr";
    #endif
const char input_type_match_flags[] PROGMEM = "_input_type_match_flags_";
const char data_pointers[] PROGMEM = "_data_pointers_";
    #if defined(DEBUG_listCommands)
const char sort_array[] PROGMEM = "sort_array";
const char sorted_ptr[] PROGMEM = "sorted_ptr";
    #endif
    #if defined(__DEBUG_READCOMMANDFROMBUFFER__)
const char token_buffer[] PROGMEM = "_token_buffer_";
    #endif
    #if defined(__DEBUG_GETCOMMANDFROMSTREAM__)
const char stream_data[] PROGMEM = "_stream_data_";
    #endif
    #if defined(__DEBUG_READCOMMANDFROMBUFFER__)
const char split_input[] PROGMEM = "rprm.split_input";
    #endif
// function var identifiers
const char listsettings_buf[] PROGMEM = "listSettings()::buf";

// var identifiers pointer array
const char* const var_id_strings[] PROGMEM = {
    // var
    #if defined(__DEBUG_ADDCOMMAND__)
    memcmp_idx,
    memcmp_ranges,
    memcmp_ranges_arr,
    #endif
    input_type_match_flags,
    data_pointers,
    #if defined(DEBUG_listCommands)
    sort_array,
    sorted_ptr,
    #endif
    #if defined(__DEBUG_READCOMMANDFROMBUFFER__)
    token_buffer,
    #endif
    #if defined(__DEBUG_GETCOMMANDFROMSTREAM__)
    stream_data,
    #endif
    #if defined(__DEBUG_READCOMMANDFROMBUFFER__)
    split_input,
    #endif
    // function var identifiers
    listsettings_buf,

};

// var identifiers pointer array convenience index
enum class VAR_ID
{
    // var
    #if defined(__DEBUG_ADDCOMMAND__)
    memcmp_idx,
    memcmp_ranges,
    memcmp_ranges_arr,
    #endif
    input_type_match_flags,
    data_pointers,
    #if defined(DEBUG_listCommands)
    sort_array,
    sorted_ptr,
    #endif
    #if defined(__DEBUG_READCOMMANDFROMBUFFER__)
    token_buffer,
    #endif
    #if defined(__DEBUG_GETCOMMANDFROMSTREAM__)
    stream_data,
    #endif
    #if defined(__DEBUG_READCOMMANDFROMBUFFER__)
    split_input,
    #endif
    // function var identifiers
    listsettings_buf,
    // reserved
    _reserved,
};

// command error checking
const char command_string[] PROGMEM = "command <%s> %S.\n";
const char root_pointer_warn[] PROGMEM = "root command function pointer cannot be NULL";
const char wcc_warn[] PROGMEM = "has_wildcard is set, but no wildcards were found in the command";
const char cmd_len_warn[] PROGMEM = "command too long, increase IH_MAX_CMD_STR_LEN or reduce command length";
const char cmd_len_dec_warn[] PROGMEM = "command_length too large for command";
const char cmd_len_inc_warn[] PROGMEM = "command_length too small for command";
const char cmd_depth_inc_warn[] PROGMEM = "depth exceeds UI_MAX_DEPTH";
const char cmd_subc_inc_warn[] PROGMEM = "sub_commands exceeds UI_MAX_SUBCOMMANDS";
const char cmd_num_args_inc_warn[] PROGMEM = "num_args exceeds UI_MAX_ARGS";
const char cmd_max_num_args_inc_warn[] PROGMEM = "max_num_args exceeds UI_MAX_ARGS";
const char cmd_flip_num_args_warn[] PROGMEM = "num_args must be less than max_num_args";

const char cmd_rejected_warn[] PROGMEM = "CommandParameters error! Root command tree rejected!";

// error types pointer array
const char* const command_error_strings[] PROGMEM = {
    command_string,
    root_pointer_warn,
    wcc_warn,
    cmd_len_warn,
    cmd_len_dec_warn,
    cmd_len_inc_warn,
    cmd_depth_inc_warn,
    cmd_subc_inc_warn,
    cmd_num_args_inc_warn,
    cmd_max_num_args_inc_warn,
    cmd_flip_num_args_warn,
    cmd_rejected_warn,
};

// error types pointer array convenience index
enum class CMD_ERR_IDX
{
    command_string,
    root_pointer_warn,
    wcc_warn,
    cmd_len_warn,
    cmd_len_dec_warn,
    cmd_len_inc_warn,
    cmd_depth_inc_warn,
    cmd_subc_inc_warn,
    cmd_num_args_inc_warn,
    cmd_max_num_args_inc_warn,
    cmd_flip_num_args_warn,
    cmd_rejected_warn,
};

// terminal
const char prompt[] PROGMEM = ">%s$";

// terminal strings array
const char* const terminal_strings[] PROGMEM = {
    prompt,
};

// terminal strings pointer array convenience index
enum class TRM
{
    prompt,
};
// end literals
///@}
} // end namespace ihc
// end namespaces group
///@}

#endif // include guard
// end of file
