from CacApp import fcp

@fcp.route('/')
def index():
        return "Hello World"