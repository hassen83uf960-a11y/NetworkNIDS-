from flask import Flask, render_template
from detector import load_and_score_flows
app=Flask(__name__)
MENU=[('dashboard','Dashboard','لوحة المعلومات'),('alerts','Alerts','التنبيهات الأمنية'),('traffic','Traffic Monitor','مراقبة حركة الشبكة'),('topology','Network Topology','مخطط الشبكة · 4 Routers'),('analysis','Analysis','تحليل السلوك'),('reports','Reports','التقارير'),('rules','Rules','قواعد التنبيه'),('system','System','حالة النظام'),('settings','Settings','الإعدادات')]
@app.route('/')
@app.route('/<page>')
def pages(page='dashboard'):
    valid={x[0] for x in MENU}
    if page not in valid: page='dashboard'
    flows=load_and_score_flows(); alerts=[x for x in flows if x['is_anomaly']]
    routers=[{'name':'Router 1','id':'R1','asn':'AS 65001','ip':'10.0.1.1','role':'Core Router','status':'Online','color':'green'}, {'name':'Router 2','id':'R2','asn':'AS 65002','ip':'10.0.2.1','role':'Edge Router','status':'Online','color':'green'}, {'name':'Router 3','id':'R3','asn':'AS 65003','ip':'10.0.3.1','role':'Distribution','status':'Online','color':'green'}, {'name':'Router 4','id':'R4','asn':'AS 65004','ip':'10.0.4.1','role':'Branch Router','status':'Standby','color':'amber'}]
    return render_template('index.html',menu=MENU,active=page,page=page,flows=flows,alerts=alerts,routers=routers,total=len(flows),alert_count=len(alerts),normal_count=len(flows)-len(alerts),high_count=sum(x['severity']=='High' for x in alerts))
if __name__=='__main__': app.run(host='127.0.0.1',port=5000,debug=True)
