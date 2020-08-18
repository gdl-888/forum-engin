# -*- coding: ks_c_5601-1987 -*-

import flask
from flask import *
import re
import sqlite3
import html
import datetime
import hashlib
import urllib.parse

def encodeURI(url):
    return urllib.parse.quote(url).replace('/', '%2F')

def sha3(content):
    return hashlib.sha3_256(bytes(content, 'EUC-KR')).hexdigest()

conn = sqlite3.connect('data.db', check_same_thread = False)
curs = conn.cursor()

app = Flask(__name__)
app.secret_key = '사이트의 비밀키 입력'

try:
    curs.execute('''create table posts (
                        username text default '',
                        title text default '',
                        content text default '',
                        time text default '',
                        num text default '',
                        category text default ''
                    )
                ''')
    curs.execute('''create table comments (
                        num text default '',
                        username text default '',
                        time text default '',
                        content text default '',
                        id text default '',
                        hidden text default '0',
                        hider text default '',
                        isstatus text default '0'
                    )
                ''')
    curs.execute('''create table removed_users (
                        username text default ''
                    )
                ''')
    curs.execute('''create table users (
                        username text default '',
                        password text default '',
                        email text default '',
                        time text default ''
                    )
                ''')

except:
    pass

def render(title, content):
    return flask.render_template_string(
        '''
            <head>
                <title>{{ title }}</title>
                <meta charset=EUC-KR>
                <style>
                    .nolink {
                        color: #000;
                        text-decoration: none;
                    }

                    .btn {
                         appearance: button;
                         -moz-appearance: button;
                         -webkit-appearance: button;
                         -ms-appearance: button;

                         text-decoration: none;

                         color: #000;

                         cursor: default;
                    }

                    button, .btn, input[type=button], input[type=submit], input[type=reset] {
                        font-size: 9pt;
                    }

                    .form-control {
                        border-radius: 5px;
                        border: 1px solid #ddd;
                        padding: 10px;
                        width: 100%;
                    }
                    .form-control:focus {
                        border-radius: 5px;
                        border: 1px solid #4af;
                        padding: 10px;
                        width: 100%;
                    }

                    .form-control[disabled], .form-control[readonly] {
                        background-color: #eceeef;
                    }

                    .nav li {
                        display: inline-block;
                    }
                    ul.nav-tabs {
                        border-bottom: 1px solid #ddd;
                        padding: 0px;
                    }
                    a.btn-link {
                        padding: 10px;
                        border: 1px solid transparent;
                        text-decoration: none;
                        color: #000;
                        margin-top: -5px
                    }

                    ul.nav-tabs a.nav-link {
                        padding: 9px;
                        border: 2px outset #adf;
                        text-decoration: none;
                        color: #000;
                        border-radius: 10px 10px 0 0;
                        background: #adf;
                        border-bottom: 2px solid #adf;
                    }
                    ul.nav-tabs a.nav-link.active {
                        border-radius: 10px 10px 0 0;
                        border: 2px solid #adf;
                        border-bottom: 3px solid #fff;
                        border-top: 1px outset #adf;
                        margin-bottom: -1px;
                        background-image: linear-gradient(to bottom, #adf 20%, #fff 100%);
                    }
                    ul.nav-tabs li + li {
                        margin-left: -5px;
                    }
                    ul.nav-tabs li.nav-item {
                        max-width: 100px;
                    }
                    ul.nav-tabs {
                        margin-bottom: 0px;
                    }
                    .tab-content.bordered {
                        border: 1px solid #ddd;
                        border-top: none;
                    }

    `               .form-group {
                        margin-bottom: 30px;
                    }

                    .tab-content .tab-pane {
                        display: none;
                    }
                    .tab-content .tab-pane.active {
                        display: block;
                    }
                    #previewFrame {
                        border: none;
                        width: 100%;
                    }
                    strike {
                        text-decoration: line-through;
                        color: #aaa;
                    }
                    .btns * {
                        float: right;
                    }
                    .pull-right {
                        float: right;
                    }
                    .alert {
                        border: 1px solid #000;
                        border-radius: 6px;
                        background: #fd0;
                    }
                    body {
                        background: aliceblue;
                    }
                    .content {
                        margin: 5px;
                        background: white;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 10px;
                    }

                    .res-wrapper {
                        margin-bottom: 30px;
                    }

                    .res-wrapper .res .r-head {
                        border-radius: 4px 4px 0 0;
                        padding: 5px;
                        background: #ddd;
                    }
                    .res-wrapper .res .r-head.first-author {
                        border-radius: 4px 4px 0 0;
                        padding: 5px;
                        background: #5f7;
                    }
                    .res-wrapper .res .r-body {
                        padding: 5px;
                        background: #f0f0f0;
                    }
                    .res-wrapper .res.res-type-status .r-body {
                        padding: 5px;
                        background: orange;
                    }
                    .res-wrapper .res .r-body.r-hidden-body {
                        padding: 5px;
                        background: #555;
                    }
                    .wiki-heading {
                        border-bottom: 1px solid #ddd;
                        margin-bottom: 0px;
                    }
                    textarea.editor {
                        font-size: 12pt !important;
                        font-family: "IHIYAGI_SYS",Fixedsys,consolas,"Lucinda Console",System,monospace !important;
                    }
                </style>

                <!--[if lt IE 9]> <script src="https://code.jquery.com/jquery-1.8.0.min.js"></script> <![endif]-->
            </head>

            <h1>{{ title }}</h1>

            <div class=content>
                {{ content|safe }}
            </di>
        ''',
        title = title,
        content = content
    )

def getTime():
    return str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

def setLang(k, e):
    return k

def errorScreen(content):
    return render(setLang('문제가 발생했습니다!', 'Error'), '<h2>' + content + '</h2>')

def generateTime(t, fmt = 'Y-m-d H:i:s'):
    try:
        ddd = t.split(' ')[0]
        ttt = t.split(' ')[1]
        return '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="' + fmt + '">' + t + '</time>'
    except:
        return t

def markdown(content):
    content = html.escape(content)
    content = re.sub('\r', '', content)

    content = re.sub('[{][{][{][#][!]wiki\s{0,}style[=]["](?P<is>(?:(?!["]).)+)["]\s{0,}\n(?P<in>(?:(?:(?![}][}][}]).)*\n*)+)[}][}][}]', '<div style="\g<is>">\g<in></div>', content, flags=re.IGNORECASE)

    content = re.sub('[*][[](?P<in>(?:(?![]]).)*)[]][(](?P<il>(?:(?![)]).)+)[)]', '<a class=nolink title="\g<il>">\g<in></a>', content)

    content = re.sub('^[!]\s{0,}(?P<in>(?:(?![\n]).)+)', '', content, flags=re.MULTILINE)

    content = re.sub('[*][*][*](?P<in>(?:(?![*][*][*]).)+)[*][*][*]', '<strong><i>\g<in></i></strong>', content)

    content = re.sub('^[*][*][*][*][*]', '<hr>', content, flags=re.MULTILINE)
    content = re.sub('^[*]\s[*]\s[*]', '<hr>', content, flags=re.MULTILINE)
    content = re.sub('^[-]\s[-]\s[-]', '<hr>', content, flags=re.MULTILINE)
    content = re.sub('^[-]{3,80}', '<hr>', content, flags=re.MULTILINE)

    content = re.sub('--(?P<in>(?:(?!--).)+)--', '<strike>\g<in></strike>', content)
    content = re.sub('~~(?P<in>(?:(?!~~).)+)~~', '<strike>\g<in></strike>', content)
    content = re.sub('[*][*](?P<in>(?:(?![*][*]).)+)[*][*]', '<strong>\g<in></strong>', content)
    content = re.sub('__(?P<in>(?:(?!__).)+)__', '<u>\g<in></u>', content)

    content = re.sub('{{\|(?P<in>(?:(?:(?!\|}}).)*\n*)+)\|}}', '<div class=wiki-textbox>\g<in></div>', content)

    content = re.sub('[`][`][`](?P<in>(?:(?:(?![`][`][`]).)*\n*)+)[`][`][`]', '<pre class=source-code>\g<in></pre>', content)
    content = re.sub('\s{4,4}(?P<in>(?:(?!\n).)+)', '<code class=source-code>\g<in></code><br>', content)

    content = re.sub('[[]br[]]', '<br>', content, flags=re.IGNORECASE)

    content = re.sub('[`](?P<in>(?:(?![`]).)+)[`]', '<code>\g<in></code>', content)

    content = re.sub('^\s{0,}[-]\s(?P<in>(?:(?![\n]).)+)', '<li>\g<in></li>', content, flags=re.MULTILINE)
    content = re.sub('^\s{0,}[*]\s(?P<in>(?:(?![\n]).)+)', '<li>\g<in></li>', content, flags=re.MULTILINE)
    content = re.sub('&gt;\s(?P<in>(?:(?![\n]).)+)', '<blockquote class=wiki-quote>\g<in></blockquote>', content)

    content = re.sub('[!][[](?P<in>(?:(?![]]).)+)[]][(](?P<il>(?:(?![)]).)+)[)]', '<img alt="\g<in>" src="\g<il>">', content)

    content = re.sub('[@][[](?P<in>(?:(?![]]).)*)[]][(](?P<il>(?:(?![)]).)+)[)]', '<iframe src="\g<il>">\g<in></iframe>', content)

    content = re.sub('[[](?P<in>(?:(?![]]).)+)[]][(](?P<il>(?:(?![)]).)+)[)]', '<a target=_blank href="\g<il>">\g<in></a>', content)

    content = re.sub('^[#]\s(?P<in>(?:(?![\n]).)+)', '<h1 class=wiki-heading>\g<in></h1>', content, flags=re.MULTILINE)
    content = re.sub('^[#][#]\s(?P<in>(?:(?![\n]).)+)', '<h2 class=wiki-heading>\g<in></h2>', content, flags=re.MULTILINE)
    content = re.sub('^[#][#][#]\s(?P<in>(?:(?![\n]).)+)', '<h3 class=wiki-heading>\g<in></h3>', content, flags=re.MULTILINE)
    content = re.sub('^[#][#][#][#]\s(?P<in>(?:(?![\n]).)+)', '<h4 class=wiki-heading>\g<in></h4>', content, flags=re.MULTILINE)
    content = re.sub('^[#][#][#][#][#]\s(?P<in>(?:(?![\n]).)+)', '<h5 class=wiki-heading>\g<in></h5>', content, flags=re.MULTILINE)
    content = re.sub('^[#][#][#][#][#][#]\s(?P<in>(?:(?![\n]).)+)', '<h6 class=wiki-heading>\g<in></h6>', content, flags=re.MULTILINE)

    content = re.sub('[[]date[(](?P<in>(?:(?![)]).)+)[)][]]', generateTime(getTime(), '\g<in>'), content, flags=re.IGNORECASE)
    content = re.sub('[[]datetime[(](?P<in>(?:(?![)]).)+)[)][]]', generateTime(getTime(), '\g<in>'), content, flags=re.IGNORECASE)
    content = re.sub('[[]time[(](?P<in>(?:(?![)]).)+)[)][]]', generateTime(getTime(), '\g<in>'), content, flags=re.IGNORECASE)

    content = re.sub('[[]date[]]', generateTime(getTime(), 'Y-m-d'), content, flags=re.IGNORECASE)
    content = re.sub('[[]datetime[]]', generateTime(getTime(), 'Y-m-d H:i:s'), content, flags=re.IGNORECASE)
    content = re.sub('[[]time[]]', generateTime(getTime(), 'H:i:s'), content, flags=re.IGNORECASE)

    content = re.sub('[{][{][{][#][!]folding\s(?P<it>(?:(?![\n]).)+)\n(?P<ic>(?:(?:(?![}][}][}]).)*\n*)+)[}][}][}]', '<dl class=wiki-folding><dt>\g<it></dt><dd>\g<ic></dd></dl>', content, flags=re.MULTILINE)

    try:
        content = re.sub('[{][{][{][+](?P<is>(?:(?![\s]).)+)\s(?P<in>(?:(?![}][}][}]).)+)[}][}][}]', '<span style="font-size: calc(\g<is>pt + 13pt);">\g<in></span>', content)
        content = re.sub('[{][{][{][-](?P<is>(?:(?![\s]).)+)\s(?P<in>(?:(?![}][}][}]).)+)[}][}][}]', '<span style="font-size: calc(11pt - \g<is>pt);">\g<in></span>', content)
    except:
        pass

    content = re.sub('[[][*](?P<it>(?:(?!\s).)+)\s(?P<in>(?:(?![]]).)+)[]]', '<sup><a class=wiki-footnote title="\g<in>">[\g<it>]</a></sup>', content)
    content = re.sub('[[][*]\s(?P<in>(?:(?![]]).)+)[]]', '<sup><a class=wiki-footnote title="\g<in>">[*]</a></sup>', content)

    content = re.sub('[[]youtube[(](?P<in>(?:(?![)]).)+)[)][]]', '<iframe src="https://youtube.com/embed/\g<in>"></iframe>', content, flags=re.IGNORECASE)

    content = re.sub('[{][{][{][#](?P<ic>(?:(?![\s]).)+)\s(?P<in>(?:(?![}][}][}]).)+)[}][}][}]', '<span style="color: #\g<ic>;">\g<in></span>', content)

    content = re.sub('[*](?P<in>(?:(?![*]).)+)[*]', '<i>\g<in></i>', content)

    content = re.sub('\n', '<BR />', content)

    return content

def islogin():
    if 'id' in session:
        return 1
    else:
        return 0


def getUsername():
    if 'id' in session:
        return session['id']

    ip = request.remote_addr

    return setLang('익명 (', 'Annonymous (') + re.sub('[.]\d{1,3}[.]\d{1,3}$', '.***.***', ip) + ')'

def getperm(permname):
    if islogin() == 1:
        return 1

    return 0

def getForm(n, d = ''):
    return request.form.get(n, d)

def alertBalloon(content, typ='danger'):
    return '<div class="alert alert-' + typ + '" role=alert>' + content + '</div>'

@app.route('/member/signup', methods=['POST', 'GET'])
def signUp():
    content = '''
        <form method=post>
            <div class=form-group>
                <label>''' + setLang('사용자 이름', 'Username') + ''' ''' + setLang('(닉네임)', '') + ''':</label><br>
                <input type=text class=form-control name=username>
            </div>
            <div class=form-group>
                <label>''' + setLang('비밀번호', 'Password') + ''':</label><br>
                <input type=password class=form-control name=password>
            </div>
            <div class=form-group>
                <label>''' + setLang('비밀번호 확인', 'Password Check') + ''':</label><br>
                <input type=password class=form-control name=password_check>
            </div>
            <p>알림: 비밀번호 암호화 알고리즘은 SHA-3입니다.</p>
            <p>경고: 보안을 위해 HTTPS로 연결했는지 확인하십시오.</p>
            <div class=btns>
                <button type=submit style="width: 100px;" class="btn btn-primary">가입</button>
            </div>
        </form>
    '''

    if request.method == 'POST':
        if len(getForm('username')) < 1 or len(getForm('username')) > 64:
            return render(setLang('계정 만들기', 'Create Account'), alertBalloon(setLang('오류: 사용자 이름이 올바르지 않습니다.', 'Error: The username is invalid.')) + content)
        if getForm('password') != getForm('password_check'):
            return render(setLang('계정 만들기', 'Create Account'), alertBalloon(setLang('오류: 비밀번호와 확인이 서로 다릅니다.', 'Error: Password and its check is different.')) + content)
        if len(getForm('password')) < 1:
            return render(setLang('계정 만들기', 'Create Account'), alertBalloon(setLang('오류: 비밀번호가 없습니다.', 'Error: The password is invalid.')) + content)
        curs.execute("select username from users where username = ? COLLATE NOCASE", [getForm('username')])
        if curs.fetchall():
            return render(setLang('계정 만들기', 'Create Account'), alertBalloon(setLang('오류: 해당 이름의 사용자가 존재합니다.', 'Error: The user with that username already exists.')) + content)
        curs.execute("insert into users (username, password, email, time) values (?, ?, ?, ?)", [
            getForm('username'),
            sha3(getForm('password')),
            '',
            getTime()
        ])
        conn.commit()
        return render(setLang('계정 만들기', 'Create Account'), setLang('계정이 생성되었습니다.', 'The account is created.'))
    return render(setLang('계정 만들기', 'Create Account'), content)

@app.route('/member/withdraw', methods=['POST', 'GET'])
def withdraw():
    if islogin() != 1:
        return redirect('/member/login?redirect=' + encodeURI('/member/withdraw'))
    content = '''
        <form method=post onsubmit="return confirm('마지막 경고입니다. 복구할 수 없습니다. 계속하시겠습니까?');">
            <p>이 계정을 삭제합니다. 동일한 이메일로 재가입하는 가능하나 동일한 사용자 이름으로는 불가능합니다.</p>
            <div class=form-group>
                <label>현재 비밀번호:</label><br>
                <input type=password name=password class=form-control>
            </div>
            <div class=btns>
                <button type=submit class="btn btn-danger" style="width: 100px;">확인</button>
            </div>
        </form>
    '''

    if request.method == 'POST':
        curs.execute("select username from users where username = ? and password = ?", [getUsername(), sha3(getForm('password'))])
        if not curs.fetchall():
            return render('계정 탈퇴', alertBalloon('비밀번호가 올바르지 않습니다.') + content)
        curs.execute("delete from users where username = ?", [getUsername()])
        curs.execute("insert into removed_users (username) values (?)", [getUsername()])
        session.pop('id', None)
        conn.commit()
        return redirect('/')

    return render('계정 탈퇴', content)

@app.route('/member/login', methods=["POST", 'GET'])
def login():
    content = '''
        <form method=post>
            <div class=form-group>
                <label>사용자 이름:</label><br>
                <input type=text class=form-control name=username>
            </div>
            <div class=form-group>
                <label>비밀번호:</label><br>
                <input type=password class=form-control name=password>
            </div>
            <p>경고: 보안을 위해 HTTPS로 연결했는지 확인하십시오.</p>
            <div class=btns>
                <button type=submit class="btn btn-primary" style="width: 100px;">확인</button>
            </div>
        </form>
    '''

    if request.method == 'POST':
        curs.execute("select username from users where username = ? COLLATE NOCASE", [getForm('username')])
        username = ''
        try:
            username = curs.fetchall()[0][0]
        except:
            return render('로그인', alertBalloon('오류: 사용자 이름이 올바르지 않습니다.') + content)
        curs.execute("select username from users where username = ? and password = ?", [username, sha3(getForm('password'))])
        if not curs.fetchall():
            return render('로그인', alertBalloon('오류: 비밀번호가 올바르지 않습니다.') + content)
        session['id'] = username
        return redirect(request.args.get('redirect', '/'))

    return render('로그인', content)

@app.route('/New', methods=['POST', 'GET'])
def newPost():
    if getperm('post') != 1:
        return errorScreen(setLang('작성 권한이 없습니다.', 'No permission!'))

    content = '''
        <form method=post class=settings-section id=editForm>
            <div class=form-group>
                <label>''' + setLang('제목', 'Title') + ''':</label><br>
                <input type=text class=form-control id=titleInput name=title value="무제">
            </div>

            <div class=form-group>
                <ul class="nav nav-tabs" role=tablist style="height: 28px;">
                    <li class=nav-item>
                        <a class="nav-link active" data-toggle=tab href=#edit role=tab>''' + setLang('편집기', 'Editor') + '''</a>
                    </li>
                    <li class=nav-item>
                        <a id=previewLink class=nav-link data-toggle=tab href=#preview role=tab>''' + setLang('미리 보기', 'Preview') + '''</a>
                    </li>

                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('![제목](그림주소)', '![제목](', ')');">외부이미지</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('[파일(그림번호)]', '[파일(', ')]');">그림</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('[* 각주]', '[* ', ']');">각주</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('[레이블](주소)', '[레이블](', ')');">링크</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('{{{#색코드 내용}}}', '{{{#색코드 ', '}}}');">글씨색</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('{{{-수치 내용}}}', '{{{-수치 ', '}}}');">작은글씨</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('{{{+수치 내용}}}', '{{{+수치 ', '}}}');">큰글씨</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('--취소선--', '--', '--');">취소선</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('__밑줄__', '__', '__');">밑줄</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('*기울게*', '*', '*');">기울게</a>
                    <a class="nolink pull-right btn-link" href="javascript:insertMarkup('**굵게**', '**', '**');">굵게</a>
                </ul>

                <div class="tab-content bordered">
                    <div class="tab-pane active" id=edit role=tabpanel>
                        <textarea id=textInput class="form-control editor" name=text wrap=soft style="width: 100%; border: none; height: 500px;"></textarea>
                    </div>
                    <div class=tab-pane id=preview role=tabpanel>

                    </div>
                </div>
            </div>

            <div>
                <a class="btn btn-primary" style="padding: 0px 10px 0px 10px;" href="/NewVote">투표 추가</a>
                <a class="btn btn-primary" style="padding: 0px 10px 0px 10px;" href="/Upload">사진 올리기</a>

                <button type=submit class="btn btn-primary pull-right" style="width: 100px;">작성 완료</button>
            </div>
        </form>
    '''

    if request.method == 'POST':
        curs.execute("select num from posts order by time desc limit 1")
        try:
            num = str(int(curs.fetchall()[0][0]) + 1)
        except:
            num = 1
        curs.execute("insert into posts (time, username, title, content, num) values (?, ?, ?, ?, ?)", [
            getTime(), getUsername(), getForm('title'), getForm('text'), str(num)
        ])

        conn.commit()

        return redirect('/topic/' + str(num))

    return render(setLang('새 쓰레드 생성', 'New Thread'), content)

@app.route('/topic/<num>', methods=['POST', 'GET'])
def viewPost(num = '0'):
    curs.execute("select time, username, title, content from posts where num = ?", [num])
    postData = curs.fetchall()
    if not postData:
        return errorScreen(setLang('해당 쓰레드를 찾을 수 없습니다.', 'The thread is not found.'))

    postData = postData[0]

    title = postData[2] + ' (' + setLang('쓰레드', 'Thread') + ' ' + num + ')'

    content = '''
        <div id=res-container>
            <div class=res-wrapper>
                <div class="res res-type-normal">
                    <div class="r-head first-author">
                        <a id=1>#1</a> ''' + postData[1] + ''' <span class=pull-right>''' + generateTime(postData[0]) + '''</span>
                    </div>
                    <div class=r-body>
                        ''' + markdown(postData[3]) + '''
                    </div>
                </div>
            </div>
    '''
    #                      0        1       2      3     4      5        6
    curs.execute("select username, time, content, id, hidden, hider, isstatus from comments where num = ? order by time asc", [num])
    for comment in curs.fetchall():
        if comment[6] == '1':
            restype = 'status'
        else:
            restype = 'normal'

        curs.execute("select username from posts where username = ? and num = ?", [comment[0], num])
        if curs.fetchall():
            firstauthor = ' first-author'
        else:
            firstauthor = ''

        ccontent = markdown(comment[2])
        hideBtn = ''
        if comment[4] == '1':
            hiddenbody = ' r-hidden-body'
            if getperm('hide_thread_comment') == 1:
                hideBtn = '''
                    <div class="combo admin-menu">
                        <a href="/admin/topic/''' + num + '/' + comment[3] + '''/show" class="btn btn-danger">[ADMIN] 숨기기 해제</a>
                    </div>
                '''
                ccontent = '''<div class="text-line-break" style="margin: 25px 0px 0px -10px; display:block">
                                <a class="text" onclick="$(this).parent().parent().children(\'.hidden-content\').show(); $(this).parent().css(\'margin\', \'15px 0 15px -10px\'); $(this).hide(); return false;" style="display: block; color: #fff;">[ADMIN] Show hidden content</a>
                                <div class="line"></div>
                            </div>
                            <div class="hidden-content" style="display:none">
                            ''' + ccontent + '</div>'
            else:
                ccontent = '[' + html.escape(comment[5]) + '에 의해 숨겨진 글입니다.]'
        else:
            if getperm('hide_thread_comment') == 1:
                hideBtn = '''
                    <div class="combo admin-menu">
                        <a href="/admin/topic/''' + num + '/' + comment[3] + '''/hide" class="btn btn-danger">[ADMIN] 숨기기</a>
                    </div>
                '''
            hiddenbody = ''

        content += '''
            <div class=res-wrapper>
                <div class="res res-type-''' + restype + '''">
                    <div class="r-head''' + firstauthor + '''">
                        <a id=''' + comment[3] + '''>#''' + comment[3] + '''</a> ''' + comment[0] + ''' <span class=pull-right>''' + generateTime(comment[1]) + '''</span>
                    </div>
                    <div class="r-body''' + hiddenbody + '''">
                        ''' + ccontent + '''
                    </div>
                </div>''' + hideBtn + '''
            </div>
        '''
    content += '</div>'

    content += '''
        <h2 class=wiki-heading>댓글 달기</h2>
        <form method=post>
            <textarea class=form-control name=comment rows=2></textarea>
            <div class=btns>
                <button type=submit class="btn btn-primary" style="width: 120px;">전송</button>
            </div>
        </form>
    '''

    if islogin() != 1:
        content += '<p style="font-weight: bold;">비로그인 상태입니다. 댓글을 전송하면 IP의 일부(' + getUsername() + ')가 기록됩니다.</p>'

    if request.method == 'POST':
        curs.execute("select id from comments where num = ? order by time desc limit 1", [num])
        try:
            insnum = str(int(curs.fetchall()[0][0]) + 1)
        except:
            insnum = '2'
        curs.execute("insert into comments (num, username, time, content, id, hidden, hider, isstatus) values (?, ?, ?, ?, ?, ?, ?, ?)",
            [num, getUsername(), getTime(), getForm('comment'), insnum, '0', '0', '0'])
        conn.commit()
        return redirect('/topic/' + num)

    return render(title, content)

@app.route('/PreviewPost', methods=["POST"])
def previewPost():
    return markdown(request.form.get('text', ''))
    
app.run()
