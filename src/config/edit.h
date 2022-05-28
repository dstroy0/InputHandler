    #if UI_MAX_PER_CMD_MEMCMP_RANGES <= UINT8_MAX
        typedef uint8_t ui_max_per_cmd_memcmp_ranges_t;
    #endif
    #if UI_MAX_PER_CMD_MEMCMP_RANGES > UINT8_MAX && UI_MAX_PER_CMD_MEMCMP_RANGES <= UINT16_MAX
        typedef uint16_t ui_max_per_cmd_memcmp_ranges_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_PER_CMD_MEMCMP_RANGES|ui_max_per_cmd_memcmp_ranges_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_PER_CMD_MEMCMP_RANGES > UINT16_MAX && UI_MAX_PER_CMD_MEMCMP_RANGES <= UINT32_MAX
        typedef uint32_t ui_max_per_cmd_memcmp_ranges_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_PER_CMD_MEMCMP_RANGES|ui_max_per_cmd_memcmp_ranges_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_PER_CMD_MEMCMP_RANGES > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_PER_CMD_MEMCMP_RANGES cannot be greater than UINT32_MAX
    #endif // end UI_MAX_PER_CMD_MEMCMP_RANGES