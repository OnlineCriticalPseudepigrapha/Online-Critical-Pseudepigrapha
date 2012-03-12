import urllib

def authbar():
    if 'auth' in globals():
        action = URL('default', 'user')
        if URL() == action:
            next = ''
        else:
            next = '?_next='+urllib.quote(URL(args=request.args, vars=request.vars))
        if auth.is_logged_in():
            logout=LI(A(T('Logout'), _href=action+'/logout'+next, _class='logoutlink'))
            profile=LI(A(T(auth.user.first_name + ' ' + auth.user.last_name), _href=action+'/profile'+next, _class='profilelink'))
            bar = UL(logout, profile, _class='auth_navbar')
        else:
            login=LI(A(T('login'), _href=action+'/login'+next, _class='loginlink'))
            register=LI(A(T('register'), _href=action+'/register'+next, _class='registerlink'))
            bar = UL(login, register, _class='auth_navbar')

        return bar