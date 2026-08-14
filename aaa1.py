import ctypes
import sys
import pymem
import threading
import webbrowser
import time
import base64
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QCheckBox,
    QLineEdit,

)
if sys.platform == "win32":
    app_id = "Shy666"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
class MemoryModifierApp(QWidget):

  def __init__(self):
    super().__init__()
    self.initUI()
    self.pm = None
    self.base_address = 0
    icon_base64 = (b"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"
    )
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(icon_base64))
    self.setWindowIcon(QIcon(pixmap))  
    

  def initUI(self):
    self.setWindowTitle("Shy🦈  (╯°□°）╯︵ ┻━┻")
    self.setWindowIcon(QIcon("icon.ico"))
    self.resize(600,4000)
    self.setMinimumSize(600, 400)
    self.setMaximumSize(600, 400)
    self.ini = 0x1
    self.cshxh = 0x1


#创建窗口ShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShy
# cs_ft =传送到方婷面前
# csh =初始化
# rwxk =0重力

    self.status_label = QLabel("状态: 未连接进程", self)
    self.status_label.setStyleSheet("color: red; font-size: 19px;")
    self.status_label.setGeometry(120, 0,1000,50)




    self.status_label1 = QLabel("坐标传送区———————————————————————————————————————————————————————", self)
    self.status_label1.setStyleSheet("color: black; font-size: 14px;")
    self.status_label1.setGeometry(0, 140,1000,50)
    self.status_label2 = QLabel("常用功能———————————————————————————————————————————————————————", self)
    self.status_label2.setStyleSheet("color: black; font-size: 14px;")
    self.status_label2.setGeometry(0, 30,1000,50)
    self.status_label3 = QLabel("🦈", self)
    self.status_label3.setStyleSheet("color: red; font-size: 40px;")
    self.status_label3.setGeometry(400, 0,1000,50)
    self.status_label3 = QLabel("社区与链接", self)
    self.status_label3.setGeometry(450, -7,80,40)
#初始化
    self.csh = QPushButton("！初始化！", self)
    self.csh.setStyleSheet("color: black; font-size: 19px;")
    self.csh.clicked.connect(self.csh1)
    self.csh.setGeometry(0, 0,100,50)
#跳转网页
    self.tzwy = QPushButton("Discord", self)
    self.tzwy.setStyleSheet("color: black; font-size: 12px; background-color: lightgray;")
    self.tzwy.clicked.connect(self.tzwy1)
    self.tzwy.setGeometry(450,18 ,60,30)
#语言切换
    self.zh = QPushButton("中文", self)
    #self.zh.setStyleSheet("color: black; font-size: 19px;")
    self.zh.clicked.connect(self.zh1)
    self.zh.setGeometry(30, 370,70,30)

    self.en = QPushButton("English", self)
    #self.en.setStyleSheet("color: black; font-size: 19px;")
    self.en.clicked.connect(self.en1)
    self.en.setGeometry(110, 370,70,30)

    self.ja = QPushButton("日本語", self)
    #self.ja.setStyleSheet("color: black; font-size: 19px;")
    self.ja.clicked.connect(self.ja1)
    self.ja.setGeometry(190, 370,70,30)

    self.ko = QPushButton("한국어", self)
    #self.ko.setStyleSheet("color: black; font-size: 19px;")
    self.ko.clicked.connect(self.ko1)
    self.ko.setGeometry(270, 370,70,30)


#人物浮空
    self.rwxk = QCheckBox("人物浮空", self)
    self.rwxk.stateChanged.connect(self.rwfk1)
    self.rwxk.setEnabled(False)
    self.rwxk.setGeometry(0, 120,120,30)
#秒杀怪物
    self.msgw = QCheckBox("一刀999", self)
    self.msgw.stateChanged.connect(self.msgw1)
    self.msgw.setEnabled(False)
    self.msgw.setGeometry(240, 60,120,30)
#锁血
    self.rwsx = QCheckBox("锁血", self)
    self.rwsx.stateChanged.connect(self.rwsx1)
    self.rwsx.setEnabled(False)
    self.rwsx.setGeometry(360, 60,120,30)
#超级防御
    self.cjfy = QCheckBox("超级防御", self)
    self.cjfy.stateChanged.connect(self.cjfy1)
    self.cjfy.setEnabled(False)
    self.cjfy.setGeometry(480, 60,120,30)
#视角转速
    self.sjzs = QCheckBox("视角转速", self)
    self.sjzs.stateChanged.connect(self.sjzs1)
    self.sjzs.setEnabled(False)
    self.sjzs.setGeometry(0, 60,120,30)
#连跳
    self.lt = QCheckBox("连跳", self)
    self.lt.stateChanged.connect(self.lt1)
    self.lt.setEnabled(False)
    self.lt.setGeometry(0, 90,120,30)
#大招无CD
    self.dzwcd = QCheckBox("大招无CD", self)
    self.dzwcd.stateChanged.connect(self.dzwcd1)
    self.dzwcd.setEnabled(False)
    self.dzwcd.setGeometry(120, 60,120,30)
#无限体力
    self.wxtl = QCheckBox("无限体力", self)
    self.wxtl.stateChanged.connect(self.wxtl1)
    self.wxtl.setEnabled(False)
    self.wxtl.setGeometry(240, 120,120,30)
#爬墙
    self.rwpq = QCheckBox("爬墙", self)
    self.rwpq.stateChanged.connect(self.rwpq1)
    self.rwpq.setEnabled(False)
    self.rwpq.setGeometry(120, 120,120,30)
#自定义跳跃高度
    self.gttxt = QLineEdit(self)
    self.gttxt.setText("1")
    self.gttxt.setPlaceholderText("1倍..")
    self.gttxt.setEnabled(False)
    self.gttxt.setGeometry(240, 90, 80, 30)



    self.gt = QCheckBox("高跳倍率", self)
    self.gt.stateChanged.connect(self.gt1)
    self.gt.setEnabled(False)
    self.gt.setGeometry(120, 90,120,30)

  #方婷面前
    self.cs_ft = QPushButton("方婷面前", self)
    self.cs_ft.clicked.connect(self.cs_ft1)
    self.cs_ft.setEnabled(False)
    self.cs_ft.setGeometry(0, 180,80,30)
  #收集月亮
    self.sjyltxt = QLabel("收集月亮默认写入速度300ms,如果游戏崩溃了,请改右侧的写速度—————————————————————————————>", self)
    self.sjyltxt.setStyleSheet("color: black; font-size: 12px;")
    self.sjyltxt.setGeometry(10, 350,550,30)
    self.sjyltxt1 = QLabel("收集月亮碎片——————————————————————————————————————————————————————————————————————", self)
    self.sjyltxt1.setStyleSheet("color: black; font-size: 14px;")
    self.sjyltxt1.setGeometry(0, 600,420,30)

    self.sjyltxt2 = QLineEdit(self)
    self.sjyltxt2.setText("300")
    self.sjyltxt2.setPlaceholderText("300ms")
    self.sjyltxt2.setEnabled(False)
    self.sjyltxt2.setGeometry(550, 350, 50, 30)

    self.sjyl_t1 = QCheckBox("<樱庭世界·昼>", self)
    self.sjyl_t1.stateChanged.connect(self.sjyl_t1_1)
    self.sjyl_t1.setEnabled(False)
    self.sjyl_t1.setGeometry(0, 290,160,30)

    self.sjyl_t2 = QCheckBox("<<贝海姆世界·正>>", self)
    self.sjyl_t2.stateChanged.connect(self.sjyl_t2_1)
    self.sjyl_t2.setEnabled(False)
    self.sjyl_t2.setGeometry(160, 290,160,30)

    self.sjyl_t3 = QCheckBox("<樱庭世界·夜>", self)
    self.sjyl_t3.stateChanged.connect(self.sjyl_t3_1)
    self.sjyl_t3.setEnabled(False)
    self.sjyl_t3.setGeometry(320, 290,160,30)

    self.sjyl_t4 = QCheckBox("<蛋糕世界·蜜>", self)
    self.sjyl_t4.stateChanged.connect(self.sjyl_t4_1)
    self.sjyl_t4.setEnabled(False)
    self.sjyl_t4.setGeometry(480, 290,160,30)

    self.sjyl_dlc_1 = QCheckBox("<DLC-鸳鸯锅>", self)
    self.sjyl_dlc_1.stateChanged.connect(self.sjyl_dlc_1_1)
    self.sjyl_dlc_1.setEnabled(False)
    self.sjyl_dlc_1.setGeometry(0, 320,160,30)

    self.sjyl_dlc_2 = QCheckBox("<DLC-水晶球>", self)
    self.sjyl_dlc_2.stateChanged.connect(self.sjyl_dlc_2_1)
    self.sjyl_dlc_2.setEnabled(False)
    self.sjyl_dlc_2.setGeometry(160, 320,160,30)

  #手动传送
    self.zbcs = QPushButton("手动传送", self)
    self.zbcs.clicked.connect(self.zbcs1)
    self.zbcs.setEnabled(False)
    self.zbcs.setGeometry(90, 180,120,30)
    self.zbcsx = QPushButton("仅更改x坐标", self)
    self.zbcsx.clicked.connect(self.zbcsx1)
    self.zbcsx.setEnabled(False)
    self.zbcsx.setGeometry(240, 210,100,30)
    self.zbcsz = QPushButton("仅更改z坐标", self)
    self.zbcsz.clicked.connect(self.zbcsz1)
    self.zbcsz.setEnabled(False)
    self.zbcsz.setGeometry(370, 210,100,30)
    self.zbcsy = QPushButton("仅更改y坐标", self)
    self.zbcsy.clicked.connect(self.zbcsy1)
    self.zbcsy.setEnabled(False)
    self.zbcsy.setGeometry(500, 210,100,30)

    self.zb_x = QLineEdit(self)
    self.zb_x.setText("1")
    self.zb_x.setPlaceholderText("X")
    self.zb_x.setEnabled(False)
    self.zb_x.setGeometry(250, 180, 80, 30)
    self.zb_x_txt = QLabel("X轴:", self)
    self.zb_x_txt.setGeometry(220, 180,30,30)

    self.zb_z = QLineEdit(self)
    self.zb_z.setText("1")
    self.zb_z.setPlaceholderText("Z")
    self.zb_z.setEnabled(False)
    self.zb_z.setGeometry(380, 180, 80, 30)
    self.zb_z_txt = QLabel("Z轴:", self)
    self.zb_z_txt.setGeometry(350, 180,30,30)

    self.zb_y = QLineEdit(self)
    self.zb_y.setText("1")
    self.zb_y.setPlaceholderText("Y")
    self.zb_y.setEnabled(False)
    self.zb_y.setGeometry(510, 180, 80, 30)
    self.zb_y_txt = QLabel("Y轴:", self)
    self.zb_y_txt.setGeometry(480, 180,30,30)
  #仅显示内容
    self.sxzb = QCheckBox("aaa.", self)
    self.sxzb.stateChanged.connect(self.sxzb1)
    self.sxzb.setGeometry(10, 210,1,1)
  
    self.x_zb_x = QLineEdit(self)
    self.x_zb_x.setReadOnly(True)
    self.x_zb_x.setText("")
    self.x_zb_x.setPlaceholderText("X")
    self.x_zb_x.setEnabled(False)
    self.x_zb_x.setGeometry(250, 240, 60, 30)
    self.x_zb_x_txt = QLabel("X轴:", self)
    self.x_zb_x_txt.setGeometry(220, 240,30,30)

    self.x_zb_z = QLineEdit(self)
    self.x_zb_z.setReadOnly(True)
    self.x_zb_z.setText("")
    self.x_zb_z.setPlaceholderText("Z")
    self.x_zb_z.setEnabled(False)
    self.x_zb_z.setGeometry(380, 240, 60, 30)
    self.x_zb_z_txt = QLabel("Z轴:", self)
    self.x_zb_z_txt.setGeometry(350, 240,30,30)

    self.x_zb_y = QLineEdit(self)
    self.x_zb_y.setReadOnly(True)
    self.x_zb_y.setText("")
    self.x_zb_y.setPlaceholderText("Y")
    self.x_zb_y.setEnabled(False)
    self.x_zb_y.setGeometry(510, 240, 60, 30)
    self.x_zb_y_txt = QLabel("Y轴:", self)
    self.x_zb_y_txt.setGeometry(480, 240,30,30)

#移速
    self.ystxt = QLineEdit(self)
    self.ystxt.setText("1")
    self.ystxt.setPlaceholderText("1倍..")
    self.ystxt.setEnabled(False)
    self.ystxt.setGeometry(480, 90, 80, 30)

    self.ys = QCheckBox("改移速", self)
    self.ys.stateChanged.connect(self.ys1)
    self.ys.setEnabled(False)
    self.ys.setGeometry(360, 90,120,30)

    #决定启动语言————————————————————————————————————————————————————————————————————————

    self.zh1()

#UIShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShyShy

  #语言切换
  def en1(self):  #英语
        self.ini = 0x1
        self.csh.setText("movement")
        self.rwxk.setText("Fly")
        self.msgw.setText("One Hit Kill")
        self.rwsx.setText("God Mode")
        self.cjfy.setText("Super Defense")
        self.sjzs.setText("Camera Speed")
        self.lt.setText("Bunny Hop")
        self.dzwcd.setText("Ultimate No CD")
        self.wxtl.setText("Infinite Stamina")
        self.rwpq.setText("Wall Climb")
        self.gt.setText("High Jump Multiplier")
        self.cs_ft.setText("In Front of Fang Ting")
        self.sjyl_t1.setText("<Sakura Garden World · Day>")
        self.sjyl_t2.setText("<Behemoth World · Normal>")
        self.sjyl_t3.setText("<Sakura Garden World · Night>")
        self.sjyl_t4.setText("<Cake World · Honey>")
        self.sjyl_dlc_1.setText("<DLC - Yuanyang Hotpot>")
        self.sjyl_dlc_2.setText("<DLC - Crystal Ball>")
        self.zbcs.setText("Manual Teleport")
        self.zbcsx.setText("Change X Only")
        self.zbcsz.setText("Change Z Only")
        self.zbcsy.setText("Change Y Only")
        self.ys.setText("Move Speed")
        self.sjyltxt.setText("Moon collection defaults to 300ms. If it crashes, adjust write speed on the right.——————>")
        self.sjyltxt1.setText("Collect Moon Fragments————————————————————————————————————————————————————————————————————————————————————")
        self.status_label.setText("Status: Process Not Connected")
        self.status_label1.setText("Coordinate Teleport———————————————————————————————————————————————————————")
        self.status_label2.setText("Common Features———————————————————————————————————————————————————————")
        self.status_label3.setText("Community & Links")
        self.ystxt.setPlaceholderText("1x..")
        self.gttxt.setPlaceholderText("1x..")

  def zh1(self):  #中文文本
      self.ini = 0x2
      self.csh.setText("！初始化！")
      self.zh.setText("中文")
      self.en.setText("English")
      self.ja.setText("日本語")
      self.ko.setText("한국어")
      self.tzwy.setText("Discord")
      self.rwxk.setText("人物浮空")
      self.msgw.setText("一刀999")
      self.rwsx.setText("锁血")
      self.cjfy.setText("超级防御")
      self.sjzs.setText("视角转速")
      self.lt.setText("连跳")
      self.dzwcd.setText("大招无CD")
      self.wxtl.setText("无限体力")
      self.rwpq.setText("爬墙")
      self.gt.setText("高跳倍率")
      self.cs_ft.setText("方婷面前")
      self.sjyl_t1.setText("<樱庭世界·昼>")
      self.sjyl_t2.setText("<<贝海姆世界·正>>")
      self.sjyl_t3.setText("<樱庭世界·夜>")
      self.sjyl_t4.setText("<蛋糕世界·蜜>")
      self.sjyl_dlc_1.setText("<DLC-鸳鸯锅>")
      self.sjyl_dlc_2.setText("<DLC-水晶球>")
      self.zbcs.setText("手动传送")
      self.zbcsx.setText("仅更改x坐标")
      self.zbcsz.setText("仅更改z坐标")
      self.zbcsy.setText("仅更改y坐标")
      self.ys.setText("改移速")
      self.sjyltxt.setText("收集月亮默认写入速度300ms,如果游戏崩溃了,请改右侧的写速度—————————————>")
      self.sjyltxt1.setText("收集月亮碎片—————————————————————————————————————————————————————————————————————————————————————————————")
      self.status_label.setText("状态: 未连接进程")
      self.status_label1.setText("坐标传送区———————————————————————————————————————————————————————")
      self.status_label2.setText("常用功能———————————————————————————————————————————————————————")
      self.status_label3.setText("社区与链接")
      self.ystxt.setPlaceholderText("1倍..")
      self.gttxt.setPlaceholderText("1倍..")

  def ja1(self):  #日语文本
      self.ini = 0x3
      self.csh.setText("！初期化！")
      self.zh.setText("中文")
      self.en.setText("English")
      self.ja.setText("日本語")
      self.ko.setText("한국어")
      self.tzwy.setText("Discord")
      self.rwxk.setText("キャラクター浮遊")
      self.msgw.setText("一撃999")
      self.rwsx.setText("HP固定")
      self.cjfy.setText("超防御")
      self.sjzs.setText("視点速度")
      self.lt.setText("連続ジャンプ")
      self.dzwcd.setText("必殺技CTなし")
      self.wxtl.setText("スタミナ無限")
      self.rwpq.setText("壁登り")
      self.gt.setText("ジャンプ倍率")
      self.cs_ft.setText("ファン・ティンの前")
      self.sjyl_t1.setText("<桜庭世界・昼>")
      self.sjyl_t2.setText("<<ベヘイム世界・正>>")
      self.sjyl_t3.setText("<桜庭世界・夜>")
      self.sjyl_t4.setText("<ケーキ世界・蜜>")
      self.sjyl_dlc_1.setText("<DLC-鴛鴦鍋>")
      self.sjyl_dlc_2.setText("<DLC-水晶玉>")
      self.zbcs.setText("手動テレポート")
      self.zbcsx.setText("X座標のみ変更")
      self.zbcsz.setText("Z座標のみ変更")
      self.zbcsy.setText("Y座標のみ変更")
      self.ys.setText("移動速度変更")
      self.sjyltxt.setText("収集速度はデフォルト300ms。クラッシュ時は右側の書き込み速度を変更————————>")
      self.sjyltxt1.setText("月の欠片を収集————————————————————————————————————————————————————————————————————————————————————————————————")
      self.status_label.setText("ステータス: 未接続")
      self.status_label1.setText("座標テレポート———————————————————————————————————————————————————————")
      self.status_label2.setText("よく使う機能———————————————————————————————————————————————————————")
      self.status_label3.setText("コミュニティとリンク")
      self.ystxt.setPlaceholderText("1倍..")
      self.gttxt.setPlaceholderText("1倍..")

  def ko1(self):  #韩语文本
      self.ini = 0x4
      self.csh.setText("！초기화！")
      self.zh.setText("中文")
      self.en.setText("English")
      self.ja.setText("日本語")
      self.ko.setText("한국어")
      self.tzwy.setText("Discord")
      self.rwxk.setText("캐릭터 공중부양")
      self.msgw.setText("한 방에 999")
      self.rwsx.setText("HP 고정")
      self.cjfy.setText("초강력 방어")
      self.sjzs.setText("시점 속도")
      self.lt.setText("연속 점프")
      self.dzwcd.setText("필살기 쿨타임 없음")
      self.wxtl.setText("스태미나 무한")
      self.rwpq.setText("벽 오르기")
      self.gt.setText("점프 배율")
      self.cs_ft.setText("팡팅 앞")
      self.sjyl_t1.setText("<사쿠라바 세계・낮>")
      self.sjyl_t2.setText("<<베헤임 세계・정>>")
      self.sjyl_t3.setText("<사쿠라바 세계・밤>")
      self.sjyl_t4.setText("<케이크 세계・꿀>")
      self.sjyl_dlc_1.setText("<DLC-원앙전골>")
      self.sjyl_dlc_2.setText("<DLC-수정구>")
      self.zbcs.setText("수동 순간이동")
      self.zbcsx.setText("X 좌표만 변경")
      self.zbcsz.setText("Z 좌표만 변경")
      self.zbcsy.setText("Y 좌표만 변경")
      self.ys.setText("이동 속도 변경")
      self.sjyltxt.setText("달 수집 속도는 기본 300ms입니다. 게임이 충돌하면 오른쪽의 기록 속도를 변경하세요———→")
      self.sjyltxt1.setText("달 조각 수집————————————————————————————————————————————————————————————————————————————————————————————————")
      self.status_label.setText("상태: 미연결")
      self.status_label1.setText("좌표 순간이동———————————————————————————————————————————————————————")
      self.status_label2.setText("자주 사용하는 기능———————————————————————————————————————————————————————")
      self.status_label3.setText("커뮤니티 및 링크")
      self.ystxt.setPlaceholderText("1배..")
      self.gttxt.setPlaceholderText("1배..")

  def csh1(self):  #初始化
    self.cshxh = 0x2
    try:
      self.pm = pymem.Pymem("launcher.exe")
      self.base_address = pymem.process.module_from_name(
          self.pm.process_handle, "GameAssembly.dll"
      ).lpBaseOfDll
      if self.ini == 0x1: #英语
          self.status_label.setText("Status: Process Connected")
          self.status_label.setStyleSheet("color: green; font-size: 19px;")
      if self.ini == 0x2: #中文
          self.status_label.setText("状态: 已成功连接进程")
          self.status_label.setStyleSheet("color: green; font-size: 19px;")
      if self.ini == 0x3: #日语
          self.status_label.setText("ステータス: プロセス接続済み")
          self.status_label.setStyleSheet("color: green; font-size: 19px;")
      if self.ini == 0x4: #韩语
          self.status_label.setText("상태: 프로세스 연결됨")
          self.status_label.setStyleSheet("color: green; font-size: 19px;")

      # 控健
      self.cs_ft.setEnabled(True)
      self.rwxk.setEnabled(True)
      self.msgw.setEnabled(True)
      self.rwsx.setEnabled(True)
      self.cjfy.setEnabled(True)
      self.sjzs.setEnabled(True)
      self.zbcs.setEnabled(True)
      self.lt.setEnabled(True)
      self.dzwcd.setEnabled(True)
      self.wxtl.setEnabled(True)
      self.rwpq.setEnabled(True)
      self.gt.setEnabled(True)
      self.ys.setEnabled(True)
      self.sjyl_t1.setEnabled(True)
      self.sjyl_t2.setEnabled(True)
      self.sjyl_t3.setEnabled(True)
      self.sjyl_t4.setEnabled(True)
      self.sjyl_dlc_1.setEnabled(True)
      self.sjyl_dlc_2.setEnabled(True)
      self.zbcsx.setEnabled(True)
      self.zbcsz.setEnabled(True)
      self.zbcsy.setEnabled(True)

      #输入框
      self.zb_x.setEnabled(True)
      self.zb_z.setEnabled(True)
      self.zb_y.setEnabled(True)
      self.gttxt.setEnabled(True)
      self.ystxt.setEnabled(True)
      self.sjyltxt2.setEnabled(True)

      #初始化默认启动项
      self.sxzb.setChecked(True)

    except Exception as e:
      QMessageBox.critical(self, "错误", f"连接进程失败: {e}")
#指针解析断——————————————————————————————————————————————————————————————————————————
  #玩家坐标结构体
  def wjzbx1(self):
    try:
      addr = self.pm.read_longlong(self.base_address + 0x79DCDC0)
      offsets = [0xB8, 0x70, 0x40, 0x20]
      for offset in offsets:
        addr = self.pm.read_longlong(addr + offset)
      return addr
    except Exception:
        return 0

  #玩家结构体（移速，血量，防御值，视角转速，攻击力）
  def wjjgt1(self):
    try:
      addr = self.pm.read_longlong(self.base_address + 0x079E21F8)
      offsets = [0x58, 0xB8, 0x0, 0x20, 0x60]
      for offset in offsets:
        addr = self.pm.read_longlong(addr + offset)
      return addr
    except Exception:
        return 0

  def wjjgt2(self):
    try:
      addr = self.pm.read_longlong(self.base_address + 0x79DCDC0)
      offsets = [0xB8,0x68,0x10,0x20,0x1B8]
      for offset in offsets:
        addr = self.pm.read_longlong(addr + offset)
      return addr
    except Exception:
        return 0
  def wjjgt3(self):
    try:
      addr = self.pm.read_longlong(self.base_address + 0x079DCDC0)
      offsets = [0xB8,0x70,0x40,0x20]
      for offset in offsets:
        addr = self.pm.read_longlong(addr + offset)
      return addr
    except Exception:
        return 0
  #技能结构体
  def jnjgt(self):
    try:
      addr = self.pm.read_longlong(self.base_address + 0x07B70828)
      offsets = [0x230,0xB8,0x0,0x20,0x20]
      for offset in offsets:
        addr = self.pm.read_longlong(addr + offset)
      return addr
    except Exception:
        return 0
  #连跳补丁
  def ltbd(self):
    try:
      addr = self.pm.read_longlong(self.base_address + 0x07B70828)
      offsets = [0xB8, 0x0, 0x40,0x20,0x28,0x28]
      for offset in offsets:
        addr = self.pm.read_longlong(addr + offset)
      return addr
    except Exception:
        return 0
 #执行写入断——————————————————————————————————————————————————————————————————————————————
#跳转网页
  def tzwy1(self):
    try:
      webbrowser.open("https://discord.gg/RWRDnqfp3")
    except Exception as e:
      QMessageBox.critical(self, "错误", f"错误！: {e}")
#传送方婷
  def cs_ft1(self):
    try:
        base_addr = self.wjzbx1()
        self.pm.write_float(base_addr + 0x110, -25.0)  # X
        self.pm.write_float(base_addr + 0x10C, 2.0)  # Y
        self.pm.write_float(base_addr + 0x108, -25.0)  # Z
    except Exception as e:
      QMessageBox.critical(self, "错误", f"错误！: {e}")
#坐标传送
  def zbcs1(self):
    try:
        base_addr = self.wjzbx1()
        x = float(self.zb_x.text())
        y = float(self.zb_y.text())
        z = float(self.zb_z.text())
        print(x)
        print(y)
        print(z)
        self.pm.write_float(base_addr + 0x110,x)  # X
        self.pm.write_float(base_addr + 0x10C,y)  # Y
        self.pm.write_float(base_addr + 0x108,z)  # Z
    except Exception as e:
      QMessageBox.critical(self, "错误", f"错误！: {e}")

  def zbcsx1(self):
    try:
        base_addr1 = self.wjzbx1()
        x = float(self.zb_x.text())
        print(x)
        self.pm.write_float(base_addr1 + 0x110,x)  # X
    except Exception as e:
      QMessageBox.critical(self, "错误", f"错误！: {e}")

  def zbcsz1(self):
    try:
        base_addr2 = self.wjzbx1()
        z = float(self.zb_z.text())
        print(z)
        self.pm.write_float(base_addr2 + 0x108,z)  # X
    except Exception as e:
      QMessageBox.critical(self, "错误", f"错误！: {e}")

  def zbcsy1(self):
    try:
        base_addr3 = self.wjzbx1()
        y = float(self.zb_y.text())
        print(y)
        self.pm.write_float(base_addr3 + 0x10C,y)  # X
    except Exception as e:
      QMessageBox.critical(self, "错误", f"错误！: {e}")

# 实时显示当前位置
  def sxzb1(self):
    if self.sxzb.isChecked():
      self.is_locking1 = True
      def background_write():
        while self.is_locking1:
          base_addr = self.wjzbx1()
          if not base_addr:
            time.sleep(0.5)
            continue
          x = self.pm.read_float(base_addr + 0x110)
          y = self.pm.read_float(base_addr + 0x10C)
          z = self.pm.read_float(base_addr + 0x108)
          self.x_zb_x.setText(f"{x:.2f}")
          self.x_zb_y.setText(f"{y:.2f}")
          self.x_zb_z.setText(f"{z:.2f}")
          print(x)
          print(z)
          print(y)
          time.sleep(0.6)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking1 = False

# #漂浮速度
  def rwfk1(self):
    if self.rwxk.isChecked():
      base_addr = self.wjjgt2()
      self.old_rwxk_val = self.pm.read_float(base_addr)
      self.is_locking1 = True
      def background_write():
        while self.is_locking1:
          base_addr = self.wjjgt2()
          if base_addr != 0:
            base_addr = base_addr + 0x84
          if base_addr != 0:
            self.pm.write_float(base_addr, 0.001)  # Z
          time.sleep(1)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking1 = False
      base_addr1 = self.wjjgt2()
      if base_addr1 != 0:
        base_addr1 = base_addr1 + 0x84
      if base_addr1 != 0:
        self.pm.write_float(base_addr1, 0.4)
# #伤害
  def msgw1(self):
    base_addr = self.wjjgt1()
    base_addr = self.pm.read_longlong(base_addr + 0x18)
    base_addr = self.pm.read_longlong(base_addr + 0x10)
    base_addr = base_addr + 0x18
    if self.msgw.isChecked():
      self.old_msgw_val = self.pm.read_float(base_addr)
      self.is_locking1 = True
      def background_write():
        while self.is_locking1:
          base_addr1 = self.wjjgt1()
          if base_addr1 != 0:
            base_addr1 = self.pm.read_longlong(base_addr1 + 0x18)
          if base_addr1 != 0:
            base_addr1 = self.pm.read_longlong(base_addr1 + 0x10)
          if base_addr1 != 0:
            base_addr1 = base_addr1 + 0x18
          if base_addr1 != 0:
            self.pm.write_float(base_addr1, 999999999.0)  # Z
          time.sleep(1)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking1 = False
      self.pm.write_float(base_addr, self.old_msgw_val)

#血量
  def rwsx1(self):
    base_addr = self.wjjgt1()
    base_addr = base_addr + 0x40
    if self.rwsx.isChecked():
      if base_addr != 0:
        self.old_msgw_val = self.pm.read_float(base_addr)
      self.is_locking = True
      def background_write():
        while self.is_locking:
          base_addr1 = self.wjjgt1()
          if base_addr1 != 0:
            base_addr1 = base_addr1 + 0x40
          if base_addr1 != 0:
            self.pm.write_float(base_addr1, 999999999.0)  # Z
          time.sleep(0.5)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking = False
      self.pm.write_float(base_addr, self.old_msgw_val)
#超级防御
  def cjfy1(self):
    base_addr = self.wjjgt1()
    base_addr = self.pm.read_longlong(base_addr + 0x58)
    base_addr = base_addr + 0x24
    if self.cjfy.isChecked():
      self.old_msgw_val = self.pm.read_float(base_addr)
      self.is_locking1 = True
      def background_write():
        while self.is_locking1:
          base_addr1 = self.wjjgt1()
          if base_addr1 != 0:
            base_addr1 = self.pm.read_longlong(base_addr1 + 0x58)
          if base_addr1 != 0:
            base_addr1 = base_addr1 + 0x24
          if base_addr1 != 0:
            self.pm.write_float(base_addr1, 999999999.0)  # Z
          time.sleep(1)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking1 = False
      self.pm.write_float(base_addr, self.old_msgw_val)

  #视角转速
  def sjzs1(self):
    base_addr = self.wjjgt1()
    base_addr = self.pm.read_longlong(base_addr + 0x28)
    base_addr = base_addr + 0x18
    if self.sjzs.isChecked():
      self.old_sjzs_val = self.pm.read_float(base_addr)
      self.is_locking1 = True
      def background_write():
        while self.is_locking1:
          base_addr1 = self.wjjgt1()
          if base_addr1 != 0:
            base_addr1 = self.pm.read_longlong(base_addr1 + 0x28)
          if base_addr1 != 0:
            base_addr1 = base_addr1 + 0x18
          if base_addr1 != 0:
            self.pm.write_float(base_addr1, 999999999.0)  # Z
          time.sleep(1)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking1 = False
      self.pm.write_float(base_addr, self.old_sjzs_val)

#爬墙
  def rwpq1(self):
        base_addr = self.wjjgt3()
        if self.rwpq.isChecked():
          self.is_locking1 = True
          def background_write():
            while self.is_locking1:
              base_addr = self.wjjgt3()
              if base_addr != 0:
                self.pm.write_float(base_addr+0x3c,120.0)
              if base_addr != 0:
                self.pm.write_float(base_addr+0x38,0.0)
            time.sleep(1)
          threading.Thread(target=background_write, daemon=True).start()
        else:
          self.is_locking1 = False
          base_addr1 = self.wjjgt3()
          self.pm.write_float(base_addr1+0x3c,60.0)
          self.pm.write_float(base_addr1+0x38,1.0)

#无限体力
  def wxtl1(self):
      try:
        if self.wxtl.isChecked():
          self.pm.write_bytes(self.base_address + 0x18E6EC6, b"\x75\x48", 2)
        else:
          self.pm.write_bytes(self.base_address + 0x18E6EC6, b"\x74\x48", 2)
      except Exception as e:
        QMessageBox.critical(self, "错误", f"错误: {e}")
#大招无cd
  def dzwcd1(self):
      try:
        base_addr = self.jnjgt()
        base_addr = self.pm.read_longlong(base_addr + 0x20)
        base_addr = base_addr + 0x28
        if self.dzwcd.isChecked():
          self.is_locking4 = True
          def background_write():
            while self.is_locking4:
              base_addr1 = self.jnjgt()
              base_addr1 = self.pm.read_longlong(base_addr1 + 0x20)
              base_addr1 = base_addr1 + 0x28
              if base_addr1 != 0:
                self.pm.write_int(base_addr1, 200)
              self.pm.write_bytes(self.base_address + 0x18E748E, b"\x90", 1)
              time.sleep(1)
          threading.Thread(target=background_write, daemon=True).start()
          self.is_locking4 = False
        else:
          self.pm.write_bytes(self.base_address + 0x18E748E, b"\xEB\x26", 2)
      except Exception as e:
        QMessageBox.critical(self, "错误", f"错误: {e}")
#连跳
  def lt1(self):
    if self.lt.isChecked():
      self.is_locking2 = True
      def background_write():
        while self.is_locking2:
          base_addr = self.wjjgt2()
          base_addr1 = self.ltbd()
          if base_addr != 0:
            self.pm.write_int(base_addr+0xA8,0)
          if base_addr1 != 0:
            self.pm.write_int(base_addr1+0xA8,0)
          print(base_addr)
          print(base_addr1)
          time.sleep(0.1)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking2 = False


#高挑
  def gt1(self):
    if self.gt.isChecked():
      self.is_locking3 = True
      def background_write():
        while self.is_locking3:
            base_addr = self.wjjgt1()
            if base_addr != 0:
              base_addr = self.pm.read_longlong(base_addr + 0x28)
              base_addr = base_addr + 0x1C
            x = float(self.gttxt.text())
            y = x * 12.0
            print(x)
            if base_addr != 0:
              self.pm.write_float(base_addr, y)
            time.sleep(5)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking3 = False
#移速
  def ys1(self):

    if self.ys.isChecked():
      self.is_locking5 = True
      def background_write():
        while self.is_locking5:
          base_addr = self.wjjgt1()
          if base_addr != 0:
            base_addr = self.pm.read_longlong(base_addr + 0x058)
          s=float(self.ystxt.text())
          s=s * 4.5
          print(s)
          if base_addr != 0:
            self.pm.write_float(base_addr+0xEC, s )
          time.sleep(1)
      threading.Thread(target=background_write, daemon=True).start()
    else:
      self.is_locking2 = False



#手机月亮
  def sjyl_t1_1(self):
      coordinates = [
     [33.40, 0.53, 19.71],
     [-29.25, 0.07, 71.38],
     [-64.39, 39.76, -80.50],
     [-49.79, 39.28, -87.75],
     [1.63, 43.38, -85.89],
     [-22.16, 44.92, -81.77],
     [14.41, 36.07, -68.39],
     [58.47, 42.44, -84.32],
     [80.68, 50.87, -51.29],
     [66.13, 53.15, -14.37],
     [-50.12, 62.70, 48.80],
     [44.29, 49.82, -42.57],
     [40.70, 53.81, -23.59],
     [45.07, 58.07, -31.40],
     [-47.59, 30.38, -49.86],
     [-41.50, 38.90, -39.19],
     [-46.03, 33.29, -32.93],
     [-4.55, 70.16, 0.05],
     [-0.71, 64.72, -14.49],
     [63.30, 34.94, 42.22],
     [70.88, 32.22, 59.45],
     [67.49, 30.82, 67.60],
     [-80.88, 45.46, 11.01],
     [-80.08, 45.88, 5.56],
     [39.61, 27.43, -21.66],
     [27.00, 25.71, 18.44],
     [33.89, 19.84, 31.44],
     [33.41, 18.41, 24.97],
     [64.32, 59.82, 44.94],
     [64.31, 59.82, 33.83],
     [-5.74, 24.65, -59.33],
     [-6.70, 11.94, -64.01],
     [-41.48, -0.23, -28.66],
     [-47.77, 0.37, -52.06],
     [-53.79, 4.00, -51.43],
     [-24.39, 13.38, -62.26],
     [-56.56, 9.75, -83.84],
     [-63.07, 17.75, -80.83],
     [67.86, 5.24, -77.77],
     [76.25, -0.14, -88.22],
     [79.00, 6.14, -16.58],
     [79.66, 6.14, -7.97],
     [32.99, 0.23, -7.78],
     [26.70, 54.72, 66.33],
     [55.24, 53.88, 72.48],
     [-29.96, 0.22, 14.27],
     [-25.37, 3.65, 31.52],
     [15.44, 9.16, 40.88],
     [79.47, -0.39, -55.38],
     [32.39, 28.66, -42.72],
     [-52.29, 3.41, 76.28],
     [-0.98, 6.69, -90.09],
     [37.07, 2.73, -78.74],
     [52.86, 15.02, -49.32],
     [49.91, 17.25, -50.56],
     [39.66, 22.77, -66.09],
     [40.79, 34.61, -65.89],
     [61.66, 41.84, -65.24],
     [-2.52, 46.11, 74.86],
     [25.79, 39.26, 71.60],
     [-33.79, 39.76, 70.70],
     [-62.82, 30.08, 36.38],
     [-70.15, 27.73, 51.10],
     [1.68, 18.54, 69.15],
     [6.96, 18.54, 78.91],
     [-14.87, 18.77, 80.59],
     [-19.24, 8.80, 87.79],
     [-13.86, 8.82, 87.75],
     [0.35, 46.29, -35.89],
     [50.69, 2.69, -8.86],
     [-4.18, 39.42, 43.77],
     [36.46, 36.29, -12.97],
     [-52.56, 37.42, -5.73],
     [-49.02, 35.00, -15.44],
     [-53.15, 41.94, 10.74],
     [-62.22, 50.46, 14.04],
     [-15.65, 58.16, 1.67],
     [8.30, 58.79, 3.49],
     [8.60, 57.77, 3.26],
     [-11.70, 46.54, 58.83],
     [-31.80, 37.32, -69.19],
     [65.70, 32.46, -79.14],
     [61.87, 43.49, -35.12],
     [61.80, 43.47, -35.15],
     [57.16, 17.86, 58.97],
     [14.94, 8.98, 59.30],
     [-45.43, 4.45, 68.55],
     [27.42, 6.62, -90.22],
     [47.94, 0.53, 18.48],
     [38.91, 0.30, 30.49],
     [26.74, 0.00, 61.75],
     [-11.37, 18.54, -35.94],
     [-15.18, 0.78, -18.98],
     [-4.63, 0.78, -27.68],
     [59.46, 10.31, -63.96],
     [54.44, 35.98, 13.49],
     [31.68, 21.81, 75.22],
      ]
      if self.sjyl_t2.isChecked():
        self.sjyl_t2.setChecked(False)
      if self.sjyl_t3.isChecked():
        self.sjyl_t3.setChecked(False)
      if self.sjyl_t4.isChecked():
        self.sjyl_t4.setChecked(False)
      if self.sjyl_dlc_1.isChecked():
        self.sjyl_dlc_1.setChecked(False)
      if self.sjyl_dlc_2.isChecked():
        self.sjyl_dlc_2.setChecked(False)
      def write_loop():
        for coord in coordinates:
          if getattr(self, "tpt_stop", False):
            break
          try:
            base_addr = self.wjzbx1()
            self.pm.write_float(base_addr + 0x108, coord[0])
            self.pm.write_float(base_addr + 0x10C, coord[1])
            self.pm.write_float(base_addr + 0x110, coord[2])
          except Exception as e:
            print(f"写入异常: {e}")
          time.sleep(float(self.sjyltxt2.text()) / 1000)
      if self.sjyl_t1.isChecked():
        self.tpt_stop = False
        threading.Thread(target=write_loop, daemon=True).start()
      else:
        self.tpt_stop = True
#手机月亮二图
  def sjyl_t2_1(self):
      coordinates = [
     [-5.40, 39.83, 23.04],
     [-5.05, 48.69, 15.62],
     [-3.26, 46.69, 16.88],
     [-58.74, 172.14, 97.15],
     [45.90, 169.22, 51.97],
     [34.57, 167.08, 35.19],
     [62.82, 180.70, 44.39],
     [64.00, 189.99, 51.03],
     [60.62, 190.84, 45.21],
     [56.17, 208.12, -2.34],
     [111.21, 199.33, 2.02],
     [82.62, 218.10, 62.74],
     [64.31, 204.46, 66.63],
     [64.13, 207.52, 64.63],
     [13.80, 205.80, 106.50],
     [5.53, 212.73, 105.90],
     [49.34, 220.91, 106.00],
     [47.34, 221.96, 97.73],
     [50.31, 209.66, 101.95],
     [-11.09, 206.43, 94.29],
     [-17.81, 206.68, 108.11],
     [-36.53, 205.11, 109.31],
     [-37.07, 204.18, 74.29],
     [-97.38, 206.29, 0.27],
     [-96.51, 204.49, -39.78],
     [-90.72, 206.43, -36.80],
     [-106.69, 204.46, -34.18],
     [-48.71, 224.00, -102.69],
     [65.29, 211.82, -102.73],
     [61.21, 218.88, -82.22],
     [31.66, 213.73, -68.33],
     [96.38, 204.00, -76.27],
     [109.76, 204.00, -54.36],
     [61.39, 220.73, -53.80],
     [45.48, 218.37, -31.72],
     [1.94, 233.35, -62.35],
     [-54.21, 235.04, -68.74],
     [-45.41, 226.28, -59.06],
     [-109.55, 229.40, -15.52],
     [-95.05, 233.52, 22.97],
     [-115.42, 240.36, 12.22],
     [-73.10, 224.02, 77.24],
     [-39.68, 228.68, 38.27],
     [-11.89, 234.53, 100.55],
     [19.58, 225.31, 49.13],
     [29.74, 227.54, 44.65],
     [-52.90, 231.71, 59.52],
     [38.34, 237.75, 46.25],
     [57.81, 234.74, 58.97],
     [68.63, 242.92, 83.20],
     [85.95, 213.29, 0.36],
     [87.54, 238.54, -11.12],
     [100.17, 234.73, 4.01],
     [104.58, 257.31, 17.44],
     [115.52, 257.51, 35.24],
     [104.43, 257.77, 53.27],
     [80.49, 259.81, 51.79],
     [73.99, 261.90, 35.31],
     [85.62, 260.64, 14.44],
     [46.40, 289.60, 62.21],
     [33.34, 289.92, 57.66],
     [4.10, 301.15, 99.77],
     [-62.80, 283.73, 81.36],
     [-49.90, 292.91, 71.59],
     [2.29, 283.40, -68.52],
     [-0.85, 283.15, -68.57],
     [0.83, 281.27, -63.79],
     [-64.38, 245.87, -77.74],
     [-99.84, 221.24, -66.17],
     [-10.38, 249.32, -71.43],
     [-9.12, 254.90, -61.64],
     [-10.35, 257.43, -65.52],
     [-9.61, 251.90, -99.34],
     [-3.74, 254.51, -117.85],
     [3.88, 276.58, -116.65],
     [-1.70, 276.88, -115.72],
     [1.02, 287.39, -126.85],
     [-2.73, 327.73, -1.60],
     [-37.91, 408.25, -79.85],
     [-12.39, 399.35, -120.28],
     [-5.25, 396.31, -121.66],
     [4.92, 396.11, -122.47],
     [55.48, 410.43, -99.42],
     [42.03, 200.00, -83.57],
     [51.22, 202.28, -96.88],
     [-99.12, 209.80, -21.59],
     [-73.86, 214.92, 25.46],
     [-37.12, 189.65, 71.39],
     [92.70, 219.18, 34.88],
     [28.15, 232.27, -71.76],
     [-6.35, 223.91, -82.19],
     [-109.42, 225.93, -37.40],
     [4.62, 187.50, -80.85],
     [-42.68, 183.05, -40.75],
     [-43.35, 188.27, -36.53],
     [-115.76, 184.86, 3.33],
     [-77.35, 187.19, 33.45],
     [-73.42, 187.19, 40.64],
     [-67.35, 187.19, 47.52],
     [-33.44, 181.78, 47.77],
     [-28.15, 178.79, 49.63],
     [89.78, 189.96, 34.22],
     [-57.64, 180.65, -101.40],
     [-47.69, 183.30, -110.73],
     [-50.52, 178.37, -107.19],
     [-9.66, 180.85, -117.07],
     [-104.86, 167.16, 45.46],
     [-109.07, 174.91, 30.92],
     [-113.18, 167.81, 22.79],
     [-75.24, 149.10, -50.86],
     [-67.45, 150.36, -61.69],
     [-55.22, 155.10, -53.37],
     [43.06, 156.94, 25.11],
     [58.51, 151.11, 25.00],
     [55.80, 157.18, 46.82],
     [61.57, 159.48, 56.79],
     [1.40, 138.94, 83.75],
     [-50.38, 125.87, -28.23],
     [-0.34, 129.99, -50.58],
     [45.85, 114.35, -22.12],
     [57.29, 94.22, -49.83],
     [31.67, 94.21, -53.76],
     [13.77, 127.38, 50.10],
     [-2.41, 114.06, -3.69],
     [1.74, 119.70, -3.65],
     [-4.47, 106.69, 13.63],
     [34.33, 88.22, 43.46],
     [29.50, 88.99, 50.87],
     [28.61, 88.12, 56.69],
     [26.81, 97.91, 76.87],
     [10.51, 88.79, 105.36],
     [-17.48, 94.76, 98.99],
     [-31.37, 92.57, 90.10],
     [-29.36, 96.11, 76.47],
     [-33.55, 97.88, 75.55],
     [-28.08, 102.75, 60.37],
     [-7.70, 113.04, 48.16],
     [-10.13, 90.29, -9.43],
     [28.00, 82.86, -1.12],
     [-5.30, 103.05, 82.91],
     [3.39, 80.51, 52.28],
     [6.61, 79.17, 55.08],
     [4.14, 73.86, 49.98],
     [21.26, 50.49, -12.22],
     [15.68, 55.15, -7.51],
     [12.98, 55.88, -13.78],
     [3.10, 65.01, 1.33],
     [38.77, 115.25, 47.09],
     [2.86, 113.89, 31.79],
     [-0.26, 112.84, 69.03],
     [-10.75, 111.60, 72.22],
     [-15.86, 106.79, 72.34],
      ]
      if self.sjyl_t1.isChecked():
        self.sjyl_t1.setChecked(False)
      if self.sjyl_t3.isChecked():
        self.sjyl_t3.setChecked(False)
      if self.sjyl_t4.isChecked():
        self.sjyl_t4.setChecked(False)
      if self.sjyl_dlc_1.isChecked():
        self.sjyl_dlc_1.setChecked(False)
      if self.sjyl_dlc_2.isChecked():
        self.sjyl_dlc_2.setChecked(False)

      def write_loop():
        for coord in coordinates:
          if getattr(self, "tpt_stop", False):
            break
          try:
            base_addr = self.wjzbx1()
            self.pm.write_float(base_addr + 0x108, coord[0])
            self.pm.write_float(base_addr + 0x10C, coord[1])
            self.pm.write_float(base_addr + 0x110, coord[2])
          except Exception as e:
            print(f"写入异常: {e}")
          time.sleep(float(self.sjyltxt2.text()) / 1000)
      if self.sjyl_t2.isChecked():
        self.tpt_stop = False
        threading.Thread(target=write_loop, daemon=True).start()
      else:
        self.tpt_stop = True
#收集月亮三图
  def sjyl_t3_1(self):
      coordinates = [
     [-1.40, 59.92, 2.09],
     [-5.92, 58.16, 2.83],
     [35.48, 40.04, 10.11],
     [36.49, 36.10, 26.63],
     [36.80, 39.15, -7.16],
     [67.44, 38.41, 42.52],
     [15.41, 38.45, 42.75],
     [22.96, 31.96, 56.78],
     [21.59, 31.61, 79.26],
     [27.10, 43.51, 74.13],
     [-34.99, 39.17, 75.31],
     [-38.99, 34.15, 42.58],
     [-65.55, 28.17, 33.71],
     [-61.36, 32.46, 8.92],
     [-62.23, 35.72, -5.38],
     [-52.08, 32.46, -13.40],
     [-69.44, 21.97, -54.54],
     [-62.85, 8.79, -80.44],
     [-60.95, 23.55, -31.33],
     [-16.84, 17.14, -56.47],
     [6.93, 31.55, -74.01],
     [13.80, 36.04, -63.39],
     [77.06, 47.25, -52.82],
     [62.61, 41.96, -63.53],
     [56.68, 41.84, -79.18],
     [61.47, 32.46, -37.41],
     [40.70, 27.43, -25.24],
     [29.75, 21.65, 15.43],
     [36.37, 20.20, 29.70],
     [58.71, 13.81, 66.79],
     [-57.89, 41.84, 4.89],
     [-58.95, 47.04, 16.78],
     [57.28, 16.22, -68.36],
     [66.95, 5.18, -77.33],
     [37.04, 27.78, -65.09],
     [34.99, -0.45, -78.52],
     [-55.31, 39.28, -78.08],
     [-62.23, 39.28, -79.34],
     [-65.43, 20.63, 53.88],
     [-62.50, 18.74, 2.56],
     [-28.99, 3.07, 14.79],
     [-26.39, 3.65, 30.95],
     [-25.02, 5.15, 56.96],
     [-17.07, 0.98, 71.34],
     [25.33, 2.88, 62.81],
     [28.36, 4.46, 76.44],
     [75.21, 5.21, 17.35],
     [64.32, 8.10, -3.03],
     [73.62, 13.34, -17.54],
     [46.53, 3.14, -9.83],
     [35.34, 0.00, -6.83],
     [35.71, 0.00, 7.22],
     [31.94, 4.64, 30.51],
     [4.21, 4.32, 77.97],
     [-48.57, 3.06, 75.02],
     [-48.42, 4.48, 63.36],
     [-25.41, 3.24, -3.47],
     [-9.80, 4.41, -15.71],
     [-46.39, 2.99, 14.56],
     [-69.06, 13.20, 63.95],
     [-37.19, 10.92, -69.64],
     [-48.16, 4.00, -48.45],
     [56.43, 53.13, 71.55],
     [52.41, 54.67, 72.54],
     [-59.87, 52.25, -18.12],
     [-7.19, 53.12, -48.18],
     [-6.77, 53.64, -61.43],
     [3.85, 50.53, -64.48],
     [-28.94, 39.85, 48.23],
     [-54.60, 20.74, -23.67],
     [-4.94, 18.56, 54.79],
     [-19.17, 14.18, 45.28],
     [19.77, -0.45, -79.07],
     [-0.76, 1.76, -83.07],
     [-78.57, 0.84, -53.48],
     [47.66, 0.33, 7.35],
      ]
      if self.sjyl_t1.isChecked():
        self.sjyl_t1.setChecked(False)
      if self.sjyl_t2.isChecked():
        self.sjyl_t2.setChecked(False)
      if self.sjyl_t4.isChecked():
        self.sjyl_t4.setChecked(False)
      if self.sjyl_dlc_1.isChecked():
        self.sjyl_dlc_1.setChecked(False)
      if self.sjyl_dlc_2.isChecked():
        self.sjyl_dlc_2.setChecked(False)
      def write_loop():
        for coord in coordinates:
          if getattr(self, "tpt_stop", False):
            break
          try:
            base_addr = self.wjzbx1()
            self.pm.write_float(base_addr + 0x108, coord[0])
            self.pm.write_float(base_addr + 0x10C, coord[1])
            self.pm.write_float(base_addr + 0x110, coord[2])
          except Exception as e:
            print(f"写入异常: {e}")
          time.sleep(float(self.sjyltxt2.text()) / 1000)
      if self.sjyl_t3.isChecked():
        self.tpt_stop = False
        threading.Thread(target=write_loop, daemon=True).start()
      else:
        self.tpt_stop = True
#手机月亮四图
  def sjyl_t4_1(self):
      coordinates = [
     [53.00, 231.11, -69.66],
     [57.84, 228.83, -78.70],
     [58.12, 227.41, -78.80],
     [41.80, 240.50, -17.67],
     [75.57, 257.43, -1.32],
     [75.42, 263.12, 2.18],
     [68.01, 272.62, 11.31],
     [33.72, 281.27, 31.33],
     [14.91, 267.59, 27.02],
     [18.97, 271.98, 28.66],
     [-6.61, 239.69, 6.01],
     [-14.73, 241.62, 12.23],
     [-1.61, 236.08, -1.49],
     [-66.32, 216.07, -17.42],
     [-59.12, 204.22, -41.79],
     [-79.02, 204.54, -7.72],
     [-90.33, 192.91, 15.04],
     [-90.27, 189.77, 18.23],
     [-82.83, 188.42, 28.14],
     [-88.33, 185.80, 33.13],
     [-14.59, 190.00, 39.42],
     [-18.31, 195.21, 33.42],
     [18.91, 206.80, 52.88],
     [77.39, 186.68, 50.04],
     [80.37, 192.68, 37.68],
     [64.94, 186.55, -7.00],
     [79.70, 186.55, -5.88],
     [64.94, 186.55, 18.65],
     [81.45, 186.55, 21.08],
     [62.99, 186.55, 6.31],
     [83.08, 186.55, 6.49],
     [-41.48, 187.36, 15.74],
     [-37.89, 188.10, 14.49],
     [4.44, 197.14, -62.50],
     [78.02, 206.33, -69.94],
     [70.19, 195.42, -45.23],
     [64.04, 193.67, -37.82],
     [59.22, 198.62, -36.40],
     [7.32, 205.20, -11.05],
     [8.33, 203.91, -18.34],
     [-67.22, 181.68, -66.53],
     [-70.46, 179.22, -71.06],
     [-60.22, 130.43, -73.83],
     [-58.75, 127.70, -68.99],
     [21.71, 151.44, -155.12],
     [105.87, 109.00, -78.95],
     [95.85, 111.80, -81.91],
     [103.18, 105.34, 1.62],
     [103.85, 107.13, 5.05],
     [107.38, 127.27, 53.50],
     [108.04, 126.87, 51.53],
     [107.12, 126.35, 55.35],
     [91.85, 131.23, 58.20],
     [92.52, 106.73, 35.59],
     [64.70, 141.58, 89.53],
     [56.44, 142.61, 90.03],
     [-0.10, 138.76, 88.14],
     [-78.34, 106.92, 56.41],
     [-78.46, 98.91, 52.68],
     [-4.98, 103.24, -3.43],
     [4.42, 99.82, -6.10],
     [28.52, 98.91, -30.99],
     [31.55, 98.91, -50.43],
     [29.05, 98.91, -57.74],
     [28.14, 98.91, -76.53],
     [10.55, 98.91, -77.28],
     [11.10, 98.91, -60.44],
     [11.70, 98.91, -47.78],
     [12.11, 98.91, -33.94],
     [12.02, 103.55, -160.74],
     [60.92, 120.33, -128.54],
     [54.29, 116.26, -132.95],
     [-44.32, 137.03, 76.14],
     [-40.39, 139.40, 77.67],
     [-38.37, 142.35, 62.14],
     [-68.56, 138.34, 50.82],
     [-42.35, 141.41, 47.75],
     [-68.64, 139.04, -10.10],
     [-44.84, 142.76, -11.62],
     [-55.26, 137.03, -12.51],
     [-63.83, 153.88, -15.54],
     [-3.48, 168.92, -51.52],
     [9.09, 154.03, -48.32],
     [12.24, 157.83, -48.05],
     [91.19, 150.37, -52.08],
     [91.38, 150.23, -13.56],
     [33.55, 126.94, -54.63],
     [82.52, 136.33, -68.32],
     [80.74, 137.61, -76.23],
     [63.46, 136.33, -84.48],
     [52.85, 136.33, -86.05],
     [49.54, 136.33, -74.61],
     [61.42, 136.33, -73.73],
     [-7.48, 117.62, -64.60],
     [8.57, 117.62, -64.58],
     [1.93, 117.62, -53.77],
     [-5.98, 123.44, -40.01],
     [87.27, 162.62, 23.63],
     [80.87, 164.65, 22.22],
     [91.83, 157.81, 38.50],
     [92.25, 156.21, 49.25],
     [43.17, 112.94, 139.00],
     [-20.09, 148.02, -20.58],
     [-27.30, 145.45, -25.52],
     [-50.12, 156.86, -56.84],
     [-74.69, 156.16, -45.88],
     [56.30, 216.80, 56.83],
     [-8.52, 211.05, -86.36],
     [-12.60, 209.64, -78.54],
     [-30.28, 178.20, 60.26],
     [-40.39, 185.77, 61.82],
     [-44.87, 185.84, 61.46],
     [-62.75, 158.59, -41.46],
     [-75.05, 183.82, -61.26],
     [20.55, 151.05, -154.45],
     [-71.23, 94.98, 108.70],
     [-93.94, 100.60, 13.43],
     [-94.03, 103.49, -9.98],
     [-93.25, 103.48, -36.03],
     [-50.19, 100.08, -62.55],
     [-42.13, 100.45, -62.70],
     [-36.21, 101.08, -63.44],
     [-42.63, 106.19, -73.04],
     [48.50, 104.87, -49.58],
     [59.94, 108.59, -45.70],
     [62.15, 111.18, -51.19],
     [-57.23, 137.03, 9.33],
     [31.25, 214.31, -52.26],
     [20.00, 212.68, -52.28],
      ]
      if self.sjyl_t1.isChecked():
        self.sjyl_t1.setChecked(False)
      if self.sjyl_t3.isChecked():
        self.sjyl_t3.setChecked(False)
      if self.sjyl_t2.isChecked():
        self.sjyl_t2.setChecked(False)
      if self.sjyl_dlc_1.isChecked():
        self.sjyl_dlc_1.setChecked(False)
      if self.sjyl_dlc_2.isChecked():
        self.sjyl_dlc_2.setChecked(False)
      def write_loop():
        for coord in coordinates:
          if getattr(self, "tpt_stop", False):
            break
          try:
            base_addr = self.wjzbx1()
            self.pm.write_float(base_addr + 0x108, coord[0])
            self.pm.write_float(base_addr + 0x10C, coord[1])
            self.pm.write_float(base_addr + 0x110, coord[2])
          except Exception as e:
            print(f"写入异常: {e}")
          time.sleep(float(self.sjyltxt2.text()) / 1000)
      if self.sjyl_t4.isChecked():
        self.tpt_stop = False
        threading.Thread(target=write_loop, daemon=True).start()
      else:
        self.tpt_stop = True
#手机月亮dlc1
  def sjyl_dlc_1_1(self):
      coordinates = [
     [15.27, 29.41, 15.25],
     [28.39, 30.49, 20.52],
     [24.39, 35.19, 20.26],
     [30.92, 44.17, 45.17],
     [5.53, 36.79, 50.30],
     [9.15, 30.03, 54.54],
     [6.05, 36.74, 50.26],
     [3.20, 33.32, 69.89],
     [3.20, 49.76, 70.34],
     [41.36, 39.84, 60.86],
     [52.49, 48.03, 54.42],
     [53.73, 46.20, 41.43],
     [68.91, 50.42, 5.15],
     [72.23, 51.44, 0.41],
     [63.93, 52.89, -4.72],
     [66.06, 45.97, -29.22],
     [59.06, 46.25, -49.06],
     [55.01, 46.25, -54.50],
     [49.75, 47.21, -51.56],
     [22.00, 45.77, -74.37],
     [19.07, 49.89, -74.13],
     [11.93, 46.30, -72.26],
     [4.65, 44.35, -50.09],
     [3.95, 41.26, -48.30],
     [11.08, 27.23, -22.11],
     [14.53, 27.23, -33.32],
     [-49.46, 40.04, -64.62],
     [-52.56, 47.18, -54.09],
     [-52.76, 44.20, -45.84],
     [-46.63, 38.36, -28.28],
     [-51.54, 25.88, -36.36],
     [-17.68, 27.99, -17.83],
     [-10.15, 28.33, -14.19],
     [-46.29, 31.03, 42.59],
     [-69.40, 33.47, 16.71],
     [-76.76, 51.17, -14.47],
     [-47.82, 50.75, -48.91],
     [-16.91, 34.44, 78.92],
     [-9.92, 42.13, 85.61],
     [-12.94, 47.94, 71.51],
     [-12.23, 55.09, 77.11],
     [-18.24, 57.24, 67.08],
     [-35.44, 64.95, 66.04],
     [-37.70, 51.81, 63.60],
     [-49.18, 45.63, 52.53],
     [-60.84, 44.83, 52.87],
     [-67.16, 55.72, 50.78],
     [-15.05, 69.20, 73.06],
     [-41.73, 50.46, 33.96],
     [-50.37, 51.51, 28.12],
     [-7.65, 33.00, -27.73],
     [-3.00, 34.19, -31.01],
     [29.26, 33.29, -46.09],
     [32.28, 27.57, -39.55],
     [26.65, 27.49, -6.62],
     [63.25, 31.60, -2.80],
     [23.69, 27.06, 64.11],
     [31.28, 25.85, 73.01],
     [0.48, 52.59, 102.71],
     [-28.29, 55.43, 117.64],
     [-42.52, 61.59, 121.17],
     [2.67, 71.14, 140.62],
     [-120.00, 53.21, -20.47],
     [-118.46, 56.60, -49.63],
     [-114.60, 59.90, -53.72],
     [-87.57, 57.58, -68.64],
     [-77.94, 57.26, -67.66],
     [-72.94, 57.44, -77.78],
     [-80.01, 57.45, -83.71],
     [-87.62, 57.66, -82.57],
     [-82.42, 57.52, -76.89],
     [-27.11, 53.48, -132.26],
     [48.77, 50.88, -106.69],
     [88.38, 51.06, -52.26],
     [112.77, 63.84, -25.90],
     [138.39, 60.30, -12.04],
     [64.83, 52.10, 76.19],
     [-70.70, 30.91, -8.39],
     [-72.44, 45.17, -1.09],
     [-70.44, 56.97, 96.67],
     [-49.84, 58.46, 57.95],
     [-51.55, 53.09, 56.63],
     [-148.43, 52.01, -0.91],
     [-132.23, 53.00, -14.11],
     [32.75, 55.27, -121.43],
     [31.79, 46.29, -123.42],
     [157.86, 67.17, 21.59],
     [155.55, 65.90, 26.24],
     [142.82, 53.59, 34.81],
     [118.44, 48.84, 45.17],
     [119.26, 49.16, 49.36],
     [109.26, 58.82, 59.19],
     [72.05, 66.05, -2.98],
     [70.25, 61.33, -1.53],
     [-0.46, 25.71, 0.51],
     [16.91, 34.65, -48.74],
     [50.90, 35.48, -52.92],
     [-24.96, 66.22, 56.38],
      ]
      if self.sjyl_t1.isChecked():
        self.sjyl_t1.setChecked(False)
      if self.sjyl_t2.isChecked():
        self.sjyl_t2.setChecked(False)
      if self.sjyl_t3.isChecked():
        self.sjyl_t3.setChecked(False)
      if self.sjyl_t4.isChecked():
        self.sjyl_t4.setChecked(False)
      if self.sjyl_dlc_2.isChecked():
        self.sjyl_dlc_2.setChecked(False)
      def write_loop():
        for coord in coordinates:
          if getattr(self, "tpt_stop", False):
            break
          try:
            base_addr = self.wjzbx1()
            self.pm.write_float(base_addr + 0x108, coord[0])
            self.pm.write_float(base_addr + 0x10C, coord[1])
            self.pm.write_float(base_addr + 0x110, coord[2])
          except Exception as e:
            print(f"写入异常: {e}")
          time.sleep(float(self.sjyltxt2.text()) / 1000)
      if self.sjyl_dlc_1.isChecked():
        self.tpt_stop = False
        threading.Thread(target=write_loop, daemon=True).start()
      else:
        self.tpt_stop = True
#手机月亮dlc2
  def sjyl_dlc_2_1(self):
      coordinates = [
     [-23.31, 21.08, -25.75],
     [-9.27, 20.61, -27.48],
     [8.44, 17.82, -25.62],
     [44.73, 44.31, -8.98],
     [38.51, 43.18, 2.59],
     [43.80, 44.36, 20.67],
     [33.71, 52.24, 6.38],
     [33.67, 60.92, 7.07],
     [33.47, 72.15, -31.12],
     [11.21, 57.56, -46.35],
     [-11.85, 65.81, -34.98],
     [-22.10, 61.33, -8.70],
     [-25.41, 56.80, -1.68],
     [-26.10, 54.86, 5.52],
     [-15.01, 57.26, 9.52],
     [-11.73, 61.39, 17.20],
     [-1.52, 54.07, 13.67],
     [11.74, 38.60, 35.17],
     [25.36, 46.41, 43.12],
     [23.50, 63.40, -13.63],
     [-45.86, 19.13, -16.16],
     [-46.48, 17.97, -19.01],
     [-35.52, 20.57, 10.21],
     [-42.78, 22.33, 5.13],
     [-41.55, 17.41, 20.27],
     [-40.06, 16.45, 26.98],
     [-29.91, 16.90, 28.13],
     [-21.22, 17.27, 30.07],
     [-14.66, 14.71, 44.31],
     [11.26, 14.93, 43.78],
     [21.31, 14.48, 34.82],
     [33.34, 15.35, 1.76],
     [32.39, 15.35, 10.47],
     [37.92, 20.04, 10.56],
     [34.73, 24.87, -2.71],
     [34.02, 24.87, 15.22],
     [39.46, 15.06, -11.46],
     [19.77, 18.65, -41.82],
     [19.75, 18.65, -41.83],
     [15.75, 21.45, -42.62],
     [-13.31, 33.58, -37.12],
     [-21.37, 23.33, -39.57],
     [7.53, 24.84, -0.06],
     [2.01, 22.34, -5.49],
     [-25.61, 35.05, -1.14],
     [32.22, 34.89, 20.77],
     [32.57, 31.09, 39.56],
     [-5.40, 39.83, 23.04],
     [-5.05, 48.69, 15.62],
     [-3.26, 46.69, 16.88],
      ]
      if self.sjyl_t1.isChecked():
        self.sjyl_t1.setChecked(False)
      if self.sjyl_t2.isChecked():
        self.sjyl_t2.setChecked(False)
      if self.sjyl_t3.isChecked():
        self.sjyl_t3.setChecked(False)
      if self.sjyl_t4.isChecked():
        self.sjyl_t4.setChecked(False)
      if self.sjyl_dlc_1.isChecked():
        self.sjyl_dlc_1.setChecked(False)
      def write_loop():
        for coord in coordinates:
          if getattr(self, "tpt_stop", False):
            break
          try:
            base_addr = self.wjzbx1()
            self.pm.write_float(base_addr + 0x108, coord[0])
            self.pm.write_float(base_addr + 0x10C, coord[1])
            self.pm.write_float(base_addr + 0x110, coord[2])
          except Exception as e:
            print(f"写入异常: {e}")
          time.sleep(float(self.sjyltxt2.text()) / 1000)
      if self.sjyl_dlc_2.isChecked():
        self.tpt_stop = False
        threading.Thread(target=write_loop, daemon=True).start()
      else:
        self.tpt_stop = True

#——————————————————————————————————————————————————————————————————————————————
if __name__ == "__main__":
  app = QApplication(sys.argv)
  ex = MemoryModifierApp()
  ex.show()
  sys.exit(app.exec())