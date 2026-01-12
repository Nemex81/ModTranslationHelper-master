from PyQt5 import QtCore


class LanguageConstants:
    menu = ''
    settings = ''
    program_version = ''

    game_directory_help = ''
    original_directory_help = ''
    previous_directory_help = ''
    target_directory_help = ''
    need_translation_help = ''
    disable_original_line_help = ''
    choice_supported_source_language_help = ''
    choice_supported_target_language_help = ''

    start_forming_hierarchy = ''
    start_file_processing = ''
    file_opened = ''
    forming_process = ''
    folder_created = ''
    error_with_data_processing = ''
    error_with_folder_creating = ''
    error_with_file_processing = ''
    error_with_modification = ''
    error_with_translation = ''
    error_quota_exceeded = ''
    api_service_changed = ''
    thread_stopped = ''
    localization_dict_creating_started = ''
    game_localization_processing = ''
    of_file = ''
    previous_localization_dict_creating_started = ''
    previous_localization_processing = ''
    process_string = ''
    final = ''
    final_time = ''

    error_settings_file_not_exist = ''
    error_folder_does_not_exist = ''
    error_drive_not_exist = ''
    error_path_not_exists = ''

    warning_disable_original_line = ''
    warning_disable_original_line_title = ''

    @classmethod
    def retranslate(cls):
        _translate = QtCore.QCoreApplication.translate
        cls.menu = _translate("Constants", "&Menu")
        cls.settings = _translate("Constants", "Settings")
        cls.program_version = _translate("Constants", "Version")

        cls.game_directory_help = _translate("Constants",
                                             "Location of the game you want to translate. The path must point to the localization folder (where the english, russian, french, etc. folders are). Default path for Crusader Kings 3:\n../Steam/steamapps/common/Crusader Kings III/game/localization")
        cls.original_directory_help = _translate("Constants",
                                                 "Folder that contains the mod localization you want to translate. Example: ../Steam/steamapps/workshop/content/1158310/2507209632/localization")
        cls.previous_directory_help = _translate("Constants",
                                                 "If you are updating a translation and already have the previous version, specify the previous translation directory. The program will scan the old files and reuse the strings it finds to build the new version. All new strings will be processed normally and marked with the #NT! comment.")
        cls.target_directory_help = _translate("Constants",
                                                "Folder where all files created by the program will be placed.\n"
                                                "(An exact copy of the original localization structure, but with language replacements and optional machine translation.)\n"
                                                "Example: if english is the source language and russian is the target, all l_english entries will be replaced with l_russian and the machine translation will be in Russian.")
        cls.need_translation_help = _translate("Constants", "When enabled, the program tries to translate all localization strings into the target language, writing the translation next to the original line. Manual review is required because machine translation may be inaccurate.")
        cls.disable_original_line_help = _translate("Constants", "Disables output of the original line, leaving only the machine translation.\n"
                                                                 "Enable only if you understand the consequences!")
        cls.choice_supported_source_language_help = _translate("Constants", "Game-supported language: choose the source language that the game supports. This is the folder/file language name where the original localization is stored.\n"
                                                                             "Original language: choose the language in which the text is written in those files.\n"
                                                                             "Note: if the game does not support Russian, Russian text may be stored in files for the English version (e.g., *_l_english can contain Russian text).")
        cls.choice_supported_target_language_help = _translate("Constants", "Game-supported language: choose the target language supported by the game. This is the folder/file name where the previous translation is stored and where you want to place the generated translation.\n"
                                                                             "Original language: choose the target language you want to translate the text into.\n"
                                                                             "Note: if the game does not officially support a language, you can still use it through the English version if the localization is placed inside the english folders.")

        cls.start_forming_hierarchy = _translate("Constants", "Directory hierarchy creation started -")
        cls.start_file_processing = _translate("Constants", "File processing started")
        cls.file_opened = _translate("Constants", "Started working with file")
        cls.forming_process = _translate("Constants", "Building directory hierarchy")
        cls.error_with_data_processing = _translate("Constants", "An error occurred")
        cls.folder_created = _translate("Constants", "Folder created")
        cls.error_with_folder_creating = _translate("Constants", "Error while creating directory")
        cls.error_with_file_processing = _translate("Constants", "Error while processing file")
        cls.error_with_modification = _translate("Constants", "Error during modification, unknown flag")
        cls.error_with_translation = _translate("Constants", "Error translating line:")
        cls.error_quota_exceeded = _translate("Constants", "Your translation quota was exceeded!")
        cls.api_service_changed = _translate("Constants", "Translation service changed to ")
        cls.thread_stopped = _translate("Constants", "Processing thread stopped")
        cls.localization_dict_creating_started = _translate("Constants", "Started creating game localization dictionary")
        cls.game_localization_processing = _translate("Constants", "Processing game localization")
        cls.of_file = _translate("Constants", "of file")
        cls.previous_localization_dict_creating_started = _translate("Constants",
                                                                     "Started creating previous localization dictionary")
        cls.previous_localization_processing = _translate("Constants", "Processing previous localization")
        cls.process_string = _translate("Constants", "Processing line")
        cls.final = _translate("Constants", "Data processing finished")
        cls.final_time = _translate("Constants", "Program finished in")

        cls.error_settings_file_not_exist = _translate("Constants", "Settings storage not found")
        cls.error_folder_does_not_exist = _translate("Constants", "Directory does not exist")
        cls.error_drive_not_exist = _translate("Constants", "Selected drive does not exist")
        cls.error_path_not_exists = _translate("Constants", "Unable to open")

        cls.warning_disable_original_line = _translate("Constants",
                                                       "Attention!\nThe author believes enabling this option will significantly reduce translation quality. Enable at your own risk. After running the program you will get fully machine-translated text with many errors! Review the translation before publishing it anywhere!")
        cls.warning_disable_original_line_title = _translate("Constants", "Warning")


class SettingsWindowConstants:

    protection_symbol_help = ''

    @classmethod
    def retranslate(cls):
        _translate = QtCore.QCoreApplication.translate

        cls.protection_symbol_help = _translate("SettingsWindow", "Warning! Do not change this setting unless you know how it works.\n"
                                                             "This symbol is used to replace values that could be corrupted by the translator and should not be sent with the main text.")


class StatWindowConstants:
    open_file = ''
    open_statements_directory = ''

    used_service_apis = ''
    lines_in_file_len = ''
    new_lines = ''
    translated_lines = ''
    lines_from_vanilla = ''
    lines_from_previous_version = ''
    lines_with_errors = ''
    time_of_process = ''

    translated_files = ''
    translated_chars = ''

    name_column_param = ''
    name_column_value = ''
    save_csv_pushButton = ''
    open_statements_pushButton = ''
    close_pushButton = ''


    @classmethod
    def retranslate(cls):
        _translate = QtCore.QCoreApplication.translate
        cls.open_file = _translate("StatWindow", "Open file")
        cls.open_statements_directory = _translate("StatWindow", "Statistics folder")
        cls.used_service_apis = _translate("StatWindow", "Used translation services")
        cls.lines_in_file_len = _translate("StatWindow", "Number of lines in file")
        cls.new_lines = _translate("StatWindow", "New lines")
        cls.translated_lines = _translate("StatWindow", "Translated lines")
        cls.lines_from_vanilla = _translate("StatWindow", "Lines from vanilla")
        cls.lines_from_previous_version = _translate("StatWindow", "Lines from previous translation")
        cls.lines_with_errors = _translate("StatWindow", "Translation errors in lines")
        cls.time_of_process = _translate("StatWindow", "Processing time")

        cls.translated_files = _translate("StatWindow", "Files translated")
        cls.translated_chars = _translate("StatWindow", "Characters translated")

        cls.name_column_param = _translate("StatWindow", "Metric")
        cls.name_column_value = _translate("StatWindow", "Value")
        cls.save_csv_pushButton = _translate("StatWindow", "Save statistics to CSV file")
        cls.open_statements_pushButton = _translate("StatWindow", "Open reports folder")
        cls.close_pushButton = _translate("StatWindow", "Close")
