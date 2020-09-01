############ Assets ############
from flask_assets import Environment, Bundle

def compile_static_assets(app):

    #Configures static asset bundles.
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False

    # Stylesheets Bundles
    dashboard_less_bundle = Bundle(
        'src/less/dashboard.less',
        filters='less,cssmin',
        output=f'dist/css/dashboard.css',
        extra={'rel': 'stylesheet/less'}
    )

    login_less_bundle = Bundle(
        'src/less/login.less',
        filters='less,cssmin',
        output=f'dist/css/login.css',
        extra={'rel': 'stylesheet/less'}
    )

    signup_less_bundle = Bundle(
        'src/less/signup.less',
        filters='less,cssmin',
        output=f'dist/css/signup.css',
        extra={'rel': 'stylesheet/less'}
    )

    # JavaScript Bundle
    js_bundle = Bundle(
        'src/js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js'
    )

    # Registers assets
    assets.register('dashboard_less_bundle', dashboard_less_bundle)
    assets.register('login_less_bundle', login_less_bundle)
    assets.register('signup_less_bundle', signup_less_bundle)
    assets.register('js_all', js_bundle)

    # Builds assets
    dashboard_less_bundle.build()
    login_less_bundle.build()
    signup_less_bundle.build()
    js_bundle.build()