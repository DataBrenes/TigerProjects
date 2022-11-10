from configparser import ConfigParser

def get_params(section):
   
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read('configs/GrandWelcome.ini')
    params = parser.items(section)
    login={}
    # turn params into dictionary
    for param in params:
        login[param[0]] = param[1]
    return login   