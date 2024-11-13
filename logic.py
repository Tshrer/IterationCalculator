import PyQt6.QtWidgets as QtWidgets
import Calu_ui
import numpy
value=0
err=False
epsilon=0.0001
max_count=0
show=False
itmat=numpy.zeros((1,1))

def get_txt(edit):
    txt=edit.text()
    if txt=='':
        txt='0'
    return txt

def setLineEdit(ui,r:int):#更改数字颜色，红色不被计入
    print("change_value",r)
    global value
    value=r
    for i in range(1, 37):
        lineedit = ui.get_option(f'lineEdit_{i}')#获取对象
        if i % 6 > r or i//6>=r:
            lineedit.setStyleSheet("color:red;")
        else:
            lineedit.setStyleSheet("color:green;")
    for i in range(37,43):
        lineedit_res = ui.get_option(f'lineEdit_{i}')  # 获取对象
        lineedit_ini = ui.get_option(f'lineEdit_{i+7}')
        if i-36>r:
            lineedit_res.setStyleSheet("color:red;")
            lineedit_ini.setStyleSheet("color:red;")
        else:
            lineedit_res.setStyleSheet("color:green")
            lineedit_ini.setStyleSheet("color:green")

def Ladd(ui,lineedit: QtWidgets.QLineEdit, number: int):
    global value
    value = int(lineedit.text())
    if value >= 6:
        return
    else:
        lineedit.setText(str(value + number))
        setLineEdit(ui,value+1)


def Lsub(ui,linedeit: QtWidgets.QLineEdit, number: int):
    global value
    value = int(linedeit.text())
    if value <= 1:
        return
    else:
        linedeit.setText(str(value - number))
        setLineEdit(ui,value-1)
#读入矩阵和向量，以及初值
def get_mtx(ui):
    global value
    print("called_get_mtx")
    mat=numpy.zeros((value,value))
    for i in range(1, value+1):
        for j in range(1, value+1):
            mat[i-1][j-1]=float(get_txt(ui.get_option(f'lineEdit_{i*6+j-6}')))
            #print(ui.get_option(f'lineEdit_{i*6+j-6}').text())
    print(f'get_mtx:\n{mat}')
    return mat

def get_vec(ui):
    global value
    vec=numpy.zeros((value,1))
    for i in range(1, value+1):
        vec[i-1][0]=float(get_txt(ui.get_option(f'lineEdit_{36+i}')))
    print(f'get_vec:\n{vec}')
    return vec

def get_ini(ui):
    global value
    ini=numpy.zeros((value,1))
    for i in range(1, value+1):
        ini[i-1][0]=float(get_txt(ui.get_option(f'lineEdit_{43+i}')))
    print(f'get_ini:\n{ini}')
    return ini

def create_itmax(it_mat,mat):
    global err
    global value
    global itmat
    itmat=mat.copy()
    for i in range(0,value):
        itmat[i][i]=0
        for j in range(0,value):
            if mat[i][i]==0:
                print(f'除零错误{i}')
                err=True
                return False
            else:
                itmat[i][j]/=-mat[i][i]
    print(f'itmat:\n{itmat}')
    return True

def check_to_exit(vec,lst):
    global epsilon
    global value
    for i in range(0,value):
        if abs(vec[i][0]-lst[i][0])>epsilon:
            return False
    return True

def solve_jacobi(ui,itmat,mat,vec,ini):
    global err
    global value
    global max_count
    global show
    solve =False
    lst=ini.copy()
    browser=ui.get_option('textBrowser')
    for count in range(0,max_count):
        for i in range(0,value):
            ini[i][0]=0
            for j in range(0,value):
                ini[i][0]+=itmat[i][j]*lst[j][0]
            ini[i][0]+=vec[i][0]/mat[i][i]
        if check_to_exit(ini,lst):
            browser.append(f"求解成功，共迭代{count}次")
            solve=True
            browser.append(f"结果为\n{lst}")
            break
        lst=ini.copy()
        if show:
            browser.append(f"第{count+1}次迭代，结果为\n{lst}")
    if not solve:
        browser.append("在设置步数内未收敛")
    return lst

def solve_gauss(ui,itmat,mat,vec,ini):
    global err
    global value
    global max_count
    global show
    solve =False
    lst=ini.copy()
    browser=ui.get_option('textBrowser')
    for count in range(0,max_count):
        for i in range(0,value):
            ini[i][0]=0
            for j in range(0,i):
                ini[i][0]+=itmat[i][j]*ini[j][0]
            for j in range(i+1,value):
                ini[i][0]+=itmat[i][j]*lst[j][0]
            ini[i][0]+=vec[i][0]/mat[i][i]
        if check_to_exit(ini,lst):
            browser.append(f"求解成功，共迭代{count}次")
            solve = True
            browser.append(f"结果为\n{lst}")
            break
        lst=ini.copy()
        if show:
            browser.append(f"第{count+1}次迭代，结果为\n{lst}")
    if not solve:
        browser.append("在设置步数内未收敛")
    return lst


def start(ui):    #获取信息并交给函数
    global value
    global err
    global epsilon
    global max_count
    global show
    global itmat
    print("called_start")
    browser = ui.get_option('textBrowser')
    browser.clear()
    mat=get_mtx(ui)
    vec=get_vec(ui)
    ini=get_ini(ui)
    max_count=int(get_txt(ui.get_option('lineEdit_50')))
    epsilon=float(get_txt(ui.get_option('lineEdit_51')))
    show = ui.get_option('checkBox_2').isChecked()
    if create_itmax(itmat,mat):
        if ui.get_option('radioButton').isChecked():#雅可比
            solve_jacobi(ui,itmat,mat,vec,ini)
        else:#高斯赛德尔
            solve_gauss(ui,itmat,mat,vec,ini)
    else:
        browser.append("除零错误，请检查矩阵对角元是否为零")