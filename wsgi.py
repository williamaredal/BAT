from ui import create_app

############ App ############
App = create_app()

############ Debug mode ############
if __name__ == '__main__':
    App.run(debug=True, host='127.0.0.1', port=8000)