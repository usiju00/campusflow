from app.auth import bp

@bp.route('/')
def index():
    return 'CampusFlow is alive!'

