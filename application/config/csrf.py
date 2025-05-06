from config.env import app_settings


csrf_settings = {
    "secret": app_settings.SECRET_KEY,
    "exempt_urls": app_settings.EXCLUDED_PATHS,
    "cookie_name": app_settings.CSRF_COOKIE_NAME,
    "cookie_secure": app_settings.COOKIE_SECURE,
    "cookie_httponly": app_settings.COOKIE_HTTP_ONLY,
    "cookie_samesite": app_settings.COOKIE_SAME_SITE,
    "header_name": app_settings.CSRF_HEADER_NAME,
}
