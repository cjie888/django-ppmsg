# -*- coding: utf-8 -*-
"""
config file for authenyication app
If you just use default features, ignore this file trustingly.
"""

"""
If you want to limit email to xxxx@yourname.com,
just set EMAIL_SUFFIX = '@yourcom.com'.
Default, no limits.
"""
EMAIL_SUFFIX = "@funshion.com"


"""limit password min length, default 6"""
PASSWORD_MIN_LENGTH = 6


"""whether login automatically after register success"""
REGISTER_AUTO_LOGIN = True


"""set the directory where user-uploaded-icon lays,
   it is under your project's media directory.
   if set "aaa", so icons lay in MEDIA_ROOT/aaa/
"""
USER_ICON_DIR = "user_icons"


"""user icon size"""
USER_ICON_WIDTH = 120
USER_ICON_HEIGHT = 120


"""
limit user icon file suffix, case insensitive
if set [], no limits
"""
USER_ICON_SUFFIXS = ["jpg", "jpeg", "png"]
