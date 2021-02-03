#coding: utf8
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt,RGBColor

p1 = "    为落实全省公共安全视频智能化建设应用专项治理工作调度会精神，提升我市视频监控前端在线率， 促进我市视频智能化建设应用工作提档升级，按照中心领导要求，从即日起每日对各县（市、区）各类视频监控前端在线、数据质量情况进行通报。\n    一、视频监控前端在线率情况\n"

p2_civic = "    市内五区\n    长安：     %，桥西：    %，新华：    %，裕华：     %，高新：    %\n    二、统计全市智能前端数据质量情况\n    1.人脸智能前端无数据上传数量\n    市内五区\n"
p2_county = "    18个县（市、区）\n    无极：  藁城：  栾城：  鹿泉：  正定：  高邑： 新乐：  赞皇：  元氏：  \n    行唐：  循环化工：  井陉：   矿区：  平山：  晋州：  赵县：  灵寿：  深泽： \n    二、统计全市智能前端数据质量情况\n    1.人脸智能前端无数据上传数量\n    18个县（市、区）\n"

p4_civic = "    2.	车辆智能前端无数据上传数量\n    市内五区\n"
p4_county = "2.	车辆智能前端无数据上传数量\n    18个县（市、区）\n"

p6 = "    四、录像可用性\n    不可调用的有"

doc = Document()
doc.styles['Normal'].font.name = u'宋体'
doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
doc.styles['Normal'].font.size = Pt(10.5)
doc.styles['Normal'].font.color.rgb = RGBColor(0,0,0)

doc.add_paragraph(p1 + p2_civic + '    桥西：189 新华：43 裕华：40 长安：178 高新：55\n' + p4_civic + '    桥西：80 新华：27 裕华：15 长安：57 高新：13\n' + p6)

doc.add_page_break()
# 保存.docx文档
doc.save(r'C:\Users\bench\Desktop\模板.docx')