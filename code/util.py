import os
config_dict={}


def read_os_environment_parameters():
    for variable_key in os.environ:
        config_dict[variable_key] = os.environ[variable_key]

def read_config_file():
    read_os_environment_parameters()
    config_file_path = os.path.join(config_dict['PARENT_DIR'], "config/astrobot.properties")
    print config_file_path
    # try:
    with open(config_file_path) as f:
        for line in f:
            if line is not None and line.strip() != "":
                config_dict[line.strip().split("=")[0]] = \
                    line.strip().split("=")[1]

def get_configs():
    read_config_file()
    read_os_environment_parameters()
    return config_dict

def load_saved_response_known_qa():
    known_qa_dict = dict()
    response_file_path = os.path.join(
        config_dict['PARENT_DIR'],
        config_dict['known_qa'+'_response_file'])

    try:
        with open(response_file_path) as f:
            for line in f:
                known_qa_dict[line.split("=")[0].lower()] = line.split("=")[1]
    except Exception, e:
        print str(e)
        print "Error! Could not load saved known qa"
    return known_qa_dict


def load_bot_specific_questions():
    bot_specifc_questions = list()
    question_file_path = os.path.join(
        config_dict['PARENT_DIR'],
        config_dict['bot_specific_questions'])
    try:
        with open(question_file_path) as f:
            for line in f:
                bot_specifc_questions.append(line.strip())
    except Exception, e:
        print str(e)
        print "Error! Could not load bot specific questions"
    return bot_specifc_questions


if __name__ == '__main__':
    print get_configs()